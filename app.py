from fastapi import FastAPI

from routes import routers

app = FastAPI(title="World Dai Star API", version="2.31.0")

for r in routers:
    app.include_router(r)
