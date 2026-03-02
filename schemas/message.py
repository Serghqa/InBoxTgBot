from datetime import date
from pydantic import BaseModel, Field, field_validator


class MessageHeader(BaseModel):

    date: str
    sender: str = Field(default="Без имени")
    address: str = Field(default="Неизвестный адрес")
    subject: str = Field(default="Без темы")

    @field_validator("date", mode="before")
    @classmethod
    def date_to_string(cls, d):

        if isinstance(d, date):
            return d.isoformat()
