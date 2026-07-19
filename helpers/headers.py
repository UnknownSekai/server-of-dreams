from helpers.config import config


def response_headers() -> dict:
    # match the official server: it sends almost nothing here. The client only *reads* the
    # X-Server-Version / X-Assets-Version / X-MasterData-* headers when present, so sending
    # them (esp. an empty X-MasterData-Version) makes it run version/masterdata checks and error.
    return {"X-FM": str(config["feature_maintenance_flags"])}
