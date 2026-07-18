import secrets

from helpers.config import config
from models import (
    AccountRegistResult,
    AuthenticateResult,
    EnvironmentResult,
    LoginResult,
)


def make_token() -> str:
    return secrets.token_urlsafe(32)


def authenticate(payload) -> AuthenticateResult:
    return AuthenticateResult(token=make_token(), ban_level=0, warned_until=None)


def register(payload) -> AccountRegistResult:
    return AccountRegistResult(token=make_token(), error_type=0)


def login(payload=None) -> LoginResult:
    return LoginResult(
        invalided_star_passes=[],
        login_pass_notification=0,
        is_approaching_login_pass_invalided=False,
        invalided_item_master_ids=[],
        approaching_item_master_ids=[],
        story_event_point_exchange_result=[],
        invalided_buff_item_master_ids=[],
    )


def environment() -> EnvironmentResult:
    base = str(config.get("public_url", "https://lb-api.wds-stellarium.com"))
    return EnvironmentResult(
        application_version=str(config.get("server_version", "2.31.0")),
        asset_version=str(config.get("asset_version", "2.31.0")),
        api_endpoint=base,
        maintenance_api_endpoint=base,
        news_api_endpoint=base,
        is_maintenance=bool(config.get("maintenance", False)),
        master_data_url=str(config.get("master_data_url", "")),
        static_content_url=str(config.get("static_content_url", "")),
        asset_url=str(config.get("asset_url", "")),
        is_app_review=False,
        photo_content_url=str(config.get("photo_content_url", "")),
        multi_real_time_server_url=str(config.get("multi_real_time_server_url", "")),
        external_payment_url=str(config.get("external_payment_url", "")),
    )
