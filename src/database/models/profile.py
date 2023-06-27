from datetime import date
from pydantic import BaseModel, Field


class Profile(BaseModel):
    """
        **Profile**
            allows users to create personalized settings
            such us - deposit multiplier

    """
    deposit_multiplier: float = Field(..., description="Multiplier for calculating deposit amount")

