from sqlalchemy import BigInteger, ForeignKey, Integer,  String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):

    pass


class User(Base):

    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    imap_credentials: Mapped[list["ImapCredentials"]] = relationship(
        "ImapCredentials",
        back_populates="user",
        uselist=True,
        cascade="all, delete-orphan"
    )


class ImapCredentials(Base):

    __tablename__ = "imap_credentials"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    imap_server: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.user_id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="imap_credentials",
    )

    def get_data(self) -> dict:

        return {
            "email": self.email,
            "password": self.password,
            "imap_server": self.imap_server,
        }
