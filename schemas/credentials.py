from pydantic import BaseModel, EmailStr, ConfigDict


class ImapSettings(BaseModel):

    model_config = ConfigDict(extra="ignore")

    imap_server: str
    email: EmailStr
    password: str
