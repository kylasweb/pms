from src.database.models.users import User
from src.database.sql import Session
from src.database.sql.user import UserORM


class UserView:

    def __init__(self):
        pass

    @staticmethod
    async def get(user_id: str) -> User | None:
        """

        :param user_id:
        :return:
        """
        if not user_id:
            return None

        with Session() as session:
            user_data: UserORM = session.query(UserORM).filter(UserORM.user_id == user_id).first()
            return User(**user_data.to_dict())

    @staticmethod
    async def post(user: User) -> User:
        """

        :param user:
        :return:
        """
        with Session() as session:
            user_data: UserORM = session.query(UserORM).filter(UserORM.user_id == user.user_id).first()
            if user_data:
                return None
            new_user: UserORM = UserORM(user.dict(exclude={"password"}))
            session.add(new_user)
            session.commit()
            return user

    @staticmethod
    async def put(user: User) -> User:
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

            return User.from_orm(user_data)

    @staticmethod
    async def login(username: str, password: str) -> User:
        with Session() as session:
            user_data: UserORM = session.query(UserORM).filter_by(username=username).first()
            if not user_data:
                return None

            # Perform password validation here (e.g., compare hashes)

            # If password is valid, return the user as a User object
            return User.from_orm(user_data)
