import uuid

from flask import Flask
from pydantic import ValidationError
from sqlalchemy import or_

from src.database.models.users import User, CreateUser
from src.database.sql import Session
from src.database.sql.user import UserORM
from src.controller import error_handler, UnauthorizedError
from src.main import send_mail
from src.emailer import EmailModel


class UserController:

    def __init__(self):
        self._password_reset_tokens: list[dict[str, int]] = []

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

    @error_handler
    async def send_password_reset(self, email: str) -> dict[str, str] | None:
        """
        Sends a password reset email to the specified email address.

        :param email: The email address to send the password reset email to.
        :return: A dictionary containing the result of the email sending operation, or None if an error occurred.
        """
        # TODO please complete the method to send the password reset email
        password_reset_subject: str = "Rental-Manager.site Password Reset Request"
        # Assuming you have a function to generate the password reset link
        password_reset_link: str = self.generate_password_reset_link(email)

        html = f"""
        <html>
        <body>
            <h2>Rental-Manager.site Password Reset</h2>
            <p>Hello,</p>
            <p>We received a password reset request for your Rental Manager account. Please click the link below to reset your password:</p>
            <a href="{password_reset_link}">{password_reset_link}</a>
            <p>If you didn't request a password reset, you can ignore this email.</p>
            <p>Thank you,</p>
            <p>The Rental Manager Team</p>
        </body>
        </html>
        """

        email_template = dict(to_=email, subject=password_reset_subject, html_=html)

        # Code to send the email using an email service/library goes here

        # Placeholder return statement for demonstration purposes
        return email_template

    @staticmethod
    def generate_password_reset_link(email: str) -> str:
        """
        Generates a password reset link for the specified email.

        :param email: The email address for which to generate the password reset link.
        :return: The password reset link.
        """
        token = str(uuid.uuid4())  # Assuming you have a function to generate a random token
        password_reset_link = f"https://rental-manager.site/reset-password?token={token}&email={email}"

        return password_reset_link

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
