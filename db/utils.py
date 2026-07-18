def create_dsn(
    host: str, port: int, database: str, username: str, password: str
) -> str:
    return f"postgresql://{username}:{password}@{host}:{port}/{database}"
