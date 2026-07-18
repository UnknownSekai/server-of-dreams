from helpers.config import config


def response_headers() -> dict:
    return {
        "X-Server-Version": str(config.get("server_version", "2.31.0")),
        "X-Maintenance": "1" if config.get("maintenance") else "0",
        "X-Maintenance-Message": str(config.get("maintenance_message", "")),
        "X-Token-Expired": "0",
        "X-MasterData-Version": str(config.get("master_data_version", "")),
        "X-MasterData-Uri": str(config.get("master_data_uri", "")),
        "X-MasterData-SasToken": str(config.get("master_data_sas_token", "")),
        "X-MasterData-PublishTimestamp": str(
            config.get("master_data_publish_timestamp", "")
        ),
        "X-FM": str(config.get("feature_maintenance_flags", "")),
    }


def check_client_version(headers) -> bool:
    _ = headers.get("X-Client-Version")
    return True


def check_asset_version(headers) -> bool:
    _ = headers.get("X-Assets-Version")
    return True


def check_masterdata_version(headers) -> bool:
    _ = headers.get("X-MasterData-Version")
    return True
