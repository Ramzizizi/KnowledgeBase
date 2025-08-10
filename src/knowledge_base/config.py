from pydantic_settings import BaseSettings


class SettingsApp(BaseSettings):
    DB_HOST: str = "localhost"
    DB_NAME: str = "db"
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_PORT: int = 5432
    DB_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_settings_app() -> SettingsApp:
    return SettingsApp()


settings_app = get_settings_app()
