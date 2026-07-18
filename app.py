from contextlib import asynccontextmanager

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from core import YumeApp
from helpers.config import config, database
from helpers.msgpack import common_response, fault
from routes import routers


@asynccontextmanager
async def lifespan(app: "YumeApp"):
    if app.config is not None:
        try:
            await app.yume_setup()
        except Exception as exc:
            print(f"[db] setup failed, continuing without database: {exc}")
    yield
    await app.close()


app = YumeApp(
    config=database,
    title=str(config.get("title", "Server of Dreams (夢のサーバー) API")),
    version=str(config.get("server_version", "2.31.0")),
    lifespan=lifespan,
)

for _r in routers:
    app.include_router(_r)


@app.exception_handler(RequestValidationError)
async def _on_validation_error(request: Request, exc: RequestValidationError):
    return common_response(None, faults=[fault("validation_error", str(exc.errors()))])


@app.exception_handler(HTTPException)
async def _on_http_error(request: Request, exc: HTTPException):
    return common_response(None, faults=[fault(str(exc.status_code), str(exc.detail))])
