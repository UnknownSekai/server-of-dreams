from helpers.config import config
from models import EnvironmentResult


def environment() -> EnvironmentResult:
    return EnvironmentResult(
        application_version=str(config["server_version"]),
        asset_version=str(config["asset_version"]),
        api_endpoint=str(config["api_endpoint"]),
        maintenance_api_endpoint=None,
        news_api_endpoint=None,
        is_maintenance=bool(config["maintenance"]),
        master_data_url=str(config["master_data_url"]),
        static_content_url=str(config["static_content_url"]),
        asset_url=str(config["asset_url"]),
        is_app_review=False,
        photo_content_url=str(config["photo_content_url"]),
        multi_real_time_server_url=str(config["multi_real_time_server_url"]),
        external_payment_url=str(config["external_payment_url"]),
    )
