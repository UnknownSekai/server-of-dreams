import logging
import uvicorn

from app import app
from helpers.config import config

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    uvicorn.run(app, host=str(config["host"]), port=int(config["port"]))
