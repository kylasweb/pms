import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class Notification(BaseModel):
    user_id: str
    title: str
    message: str
    category: str
    time_read: datetime | None
    is_read: bool
    time_created: datetime


class NotificationsModel(BaseModel):

    notifications: list[Notification]


class CreateNotification(BaseModel):
    user_id: str = Field(default_factory=lambda: uuid.uuid4())
    title: str
    message: str
    category: str
    time_read: datetime | None
    is_read: bool = Field(default=False)
    time_created: datetime = Field(default_factory=lambda: datetime.now())

