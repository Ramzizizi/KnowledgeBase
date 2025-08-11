from pydantic_settings import BaseSettings


class SettingsApp(BaseSettings):
    DB_HOST: str = "localhost"
    DB_NAME: str = "db"
    DB_USER: str = "user"
    DB_PASSWORD: str = "password"
    DB_PORT: int = 5432

    @property
    def DB_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


def get_settings_app() -> SettingsApp:
    return SettingsApp()


settings_app = get_settings_app()
