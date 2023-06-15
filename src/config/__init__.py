from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    SECRET_KEY: str = Field(default="abs")


def config_instance() -> Settings:
    """

    :return:
    """
    return Settings()
