from pydantic import BaseSettings


class Settings(BaseSettings):
    pass


def config_instance() -> Settings:
    """

    :return:
    """
    return Settings()
