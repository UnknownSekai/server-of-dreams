import uvicorn

from app import app
from helpers.config import config

if __name__ == "__main__":
    uvicorn.run(app, host=str(config["host"]), port=int(config["port"]))
