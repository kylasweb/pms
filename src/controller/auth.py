from flask import Flask
from pydantic import ValidationError
from sqlalchemy import or_

from src.database.models.users import User, CreateUser
from src.database.sql import Session
from src.database.sql.user import UserORM
from src.controller import error_handler, UnauthorizedError


class UserController:

    def __init__(self):
        pass

    def init_app(self, app: Flask):
        pass

    @staticmethod
    @error_handler
    async def get(user_id: str) -> dict[str, str] | None:
        """

        :param user_id:
        :return:
        """
        if not user_id:
            return None

        with Session() as session:
            user_data: UserORM = session.query(UserORM).filter(UserORM.user_id == user_id).first()
            return user_data.to_dict()

    @staticmethod
    @error_handler
    async def get_by_email(email: str) -> User | None:
        """

        :param email:
        :return:
        """
        if not email:
            return None

        with Session() as session:
            user_data: UserORM = session.query(UserORM).filter(UserORM.email == email.casefold()).first()

            return User(**user_data.to_dict()) if user_data else None

    @staticmethod
    @error_handler
    async def send_password_reset(email: str) -> dict[str, str] | None:
        """

        :param email:
        :return:
        """
        # TODO please complete the method to send the password reset email
        pass

    @staticmethod
    @error_handler
    async def post(user: CreateUser) -> User | None:
        """

        :param user:
        :return:
        """
        with Session() as session:
            user_data: UserORM = session.query(UserORM).filter(or_(UserORM.user_id == user.user_id,
                                                                   UserORM.email == user.email)).first()
            if user_data:
                return None

            new_user: UserORM = UserORM(**user.to_dict())
            session.add(new_user)
            session.commit()
            return User(**user_data.to_dict())

    @staticmethod
    @error_handler
    async def put(user: User) -> dict[str, str] | None:
        with Session() as session:
            user_data: UserORM = session.query(UserORM).filter_by(user_id=user.user_id).first()
            if not user_data:
                return None

            # Update user_data with the values from the user Pydantic BaseModel
            for field in user_data.__table__.columns.keys():
                if hasattr(user, field):
                    setattr(user_data, field, getattr(user, field))

            # Save the updated user_data back to the session
            session.add(user_data)
            session.commit()

            return user_data.to_dict()

    @staticmethod
    @error_handler
    async def login(username: str, password: str) -> User | None:
        with Session() as session:
            user_data: UserORM = session.query(UserORM).filter_by(username=username).first()
            try:
                if user_data:
                    user: User = User(**user_data.to_dict())
                else:
                    return None
            except ValidationError as e:
                raise UnauthorizedError(description="Cannot Login User please check your login details")

            return user if user.is_login(password=password) else None
