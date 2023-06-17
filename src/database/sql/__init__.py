from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import config_instance
from sqlalchemy.ext.declarative import declarative_base

settings = config_instance().MYSQL_SETTINGS
# Replace 'your_username', 'your_password', 'your_host', and 'your_database' with your MySQL database credentials
engine = create_engine(settings.DEVELOPMENT_DB)
Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()


