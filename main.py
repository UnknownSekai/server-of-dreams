import uvicorn

from app import app
from helpers.config import config

if __name__ == "__main__":
    uvicorn.run(
        app, host=str(config.get("host", "0.0.0.0")), port=int(config.get("port", 8080))
    )
