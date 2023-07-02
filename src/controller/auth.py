import uuid
import time
from flask import Flask, render_template
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
        self._time_limit = 360
        self._verification_tokens: dict[str, int | dict[str, str | int]] = {}

    def init_app(self, app: Flask):
        pass

    async def is_token_valid(self, token: str) -> bool:
        """
        Checks if the password reset token is valid based on the elapsed time.

        :param token: The password reset token to validate.
        :return: True if the token is valid, False otherwise.
        """
        if token in set(self._verification_tokens.key()):
            timestamp: int = self._verification_tokens[token]
            current_time: int = int(time.time())
            elapsed_time = current_time - timestamp
            return elapsed_time < self._time_limit

        return False

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

        email_template = dict(to_=email, subject_=password_reset_subject, html_=html)
        await send_mail.send_mail_resend(email=EmailModel(**email_template))

        return email_template

    def generate_password_reset_link(self, email: str) -> str:
        """
        Generates a password reset link for the specified email.

        :param email: The email address for which to generate the password reset link.
        :return: The password reset link.
        """
        token = str(uuid.uuid4())  # Assuming you have a function to generate a random token
        self._verification_tokens[token] = int(time.time())
        return f"https://rental-manager.site/admin/reset-password?token={token}&email={email}"

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

    @error_handler
    async def send_verification_email(self, user: User) -> None:
        """
        Sends a verification email to the specified user.

        :param user: The user to send the verification email to.
        """
        print(f"user passed on : {user}")
        token = str(uuid.uuid4())  # Assuming you have a function to generate a verification token
        verification_link = f"https://rental-manager.site/admin/verify-email?token={token}&email={user.email}"
        self._verification_tokens[token] = dict(email=user.email, timestamp=int(time.time()))
        # Render the email template
        email_html = render_template("email_templates/verification_email.html", user=user,
                                     verification_link=verification_link)

        msg = EmailModel(subject_="Rental-Manager.site Email Verification",
                         to_=user.email,
                         html_=email_html)

        await send_mail.send_mail_resend(email=msg)

    @error_handler
    async def verify_email(self, email: str, token: str):
        """

        :param email:
        :param token:
        :return:
        """
        if token in set(self._verification_tokens.keys()):

            _data: dict[str, str | int] = self._verification_tokens[token]

            current_time: int = int(time.time())
            elapsed_time = current_time - int(_data.get('timestamp', 0))
            # print(f"elapsed time : {elapsed_time} time limit : {self._time_limit}")
            # print(f"condition : {elapsed_time < self._time_limit}")
            return True
            # return (elapsed_time < self._time_limit) and (email.casefold() == _data.get('email'))

        return False
