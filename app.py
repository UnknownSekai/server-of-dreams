from contextlib import asynccontextmanager

from fastapi import Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException

from core import YumeApp
from helpers.auth import decode_jwt
from helpers.cache import load_master_data
from helpers.config import config, database
from helpers.master_data import master_data_db
from helpers.msgpack import common_response, fault
from helpers.things import repair_dual_cards
from realtime.dispatcher import RealtimeRouter, build_service
from routes import live_modes, routers

_PRESERVATION_TABLES = (
    "CREATE TABLE IF NOT EXISTS preservation_live_context ("
    '"userId" bigint PRIMARY KEY REFERENCES accounts("userId") ON DELETE CASCADE, '
    'mode text NOT NULL, "masterId" integer NOT NULL, '
    "extra jsonb NOT NULL DEFAULT '{}'::jsonb)",
    "CREATE TABLE IF NOT EXISTS preservation_course_run ("
    '"userId" bigint PRIMARY KEY REFERENCES accounts("userId") ON DELETE CASCADE, '
    "data jsonb NOT NULL)",
    # auto-play flag added to the transient active-live row (see db.user.create_active_live);
    # kept here too so existing databases gain the column without re-running database_setup.
    'ALTER TABLE active_live ADD COLUMN IF NOT EXISTS "isAutoPlay" '
    "boolean NOT NULL DEFAULT false",
)

# The realtime StreamingHub channel is a second listener (HTTP/2 + gRPC) that the
# game connects to separately from the REST API. It is built here so both can share
# one process, but started only when `realtime.auto_start` is set in config.yml --
# running it standalone with realtime_main.py is also supported.
realtime_service = build_service(config, decode_jwt)
_realtime_cfg = config.get("realtime")
if hasattr(_realtime_cfg, "model_dump"):
    _realtime_cfg = _realtime_cfg.model_dump()
_realtime_cfg = _realtime_cfg or {}


@asynccontextmanager
async def lifespan(app: "YumeApp"):
    load_master_data()  # master data JSON -> models (helpers.cache.cache)
    if app.config is not None:
        await app.yume_setup()
        async with app.acquire_db() as conn:  # live/course progression bookkeeping tables
            for _sql in _PRESERVATION_TABLES:
                await conn.conn.execute(_sql)
            # link the second idol on any dual-idol cards saved before that was handled
            async with conn.transaction():
                repaired = await repair_dual_cards(conn)
            if repaired:
                print(
                    f"Linked the second idol on {repaired} dual-idol card(s)",
                    flush=True,
                )
            # drop empty live records (clearLamp None_ + achievementRate 0): a real clear always
            # has a lamp and a scored fail keeps its own rate, so such a row is only an all-miss
            # fail or an artifact of the earlier over-correction -- removing it lets the song read
            # "not played" instead of a bogus 0.0%.
            cleared = await conn.conn.execute(
                'DELETE FROM "live" WHERE "clearLamp" = 0 AND "achievementRate" = 0'
            )
            if cleared and cleared != "DELETE 0":
                print(f"Removed empty live records ({cleared})", flush=True)
    if _realtime_cfg.get("auto_start"):
        await realtime_service.start()
    yield
    if _realtime_cfg.get("auto_start"):
        await realtime_service.stop()
    await app.close()


app = YumeApp(
    config=database,
    title="Server of Dreams (夢のサーバー) API",
    version=str(config["server_version"]),
    lifespan=lifespan,
)
app.realtime_service = realtime_service

for _r in routers:
    app.include_router(_r)
app.include_router(RealtimeRouter(realtime_service).router)
# prepend the live/lesson/course overrides so they take precedence over the base handlers
live_modes.install(app)


# master-data blob the client fetches from assets-e (redirected here): repacked from
# the masterdata/*.json tables. 404s (-> redirect falls back) until they're unpacked.
@app.get("/master-data/production/{path:path}", include_in_schema=False)
async def _master_data_blob(path: str) -> Response:
    db = master_data_db()
    if db is None:
        raise HTTPException(status_code=404)
    return Response(content=db, media_type="application/octet-stream")


@app.exception_handler(RequestValidationError)
async def _on_validation_error(request: Request, exc: RequestValidationError):
    return common_response(None, faults=[fault("validation_error", str(exc.errors()))])


@app.exception_handler(HTTPException)
async def _on_http_error(request: Request, exc: HTTPException):
    if not request.url.path.startswith("/api/"):
        return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
    return common_response(None, faults=[fault(str(exc.status_code), str(exc.detail))])
