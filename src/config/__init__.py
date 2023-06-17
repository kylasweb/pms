from pydantic import BaseSettings, Field


class MySQLSettings(BaseSettings):

    PRODUCTION_DB: str = Field(..., env="production_sql_db")
    DEVELOPMENT_DB: str = Field(..., env="dev_sql_db")

    class Config:
        env_file = '.env.development'
        env_file_encoding = 'utf-8'


class Settings(BaseSettings):
    SECRET_KEY: str = Field(default="abs")
    MYSQL_SETTINGS: MySQLSettings = MySQLSettings()

    class Config:
        env_file = '.env.development'
        env_file_encoding = 'utf-8'


def config_instance() -> Settings:
    """

    :return:
    """
    return Settings()
