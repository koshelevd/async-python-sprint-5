import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, func

from db.utils.db_session import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True,
        nullable=False,
        comment="ID",
    )

    created_at = Column(
        DateTime,
        nullable=False,
        comment="Date and time of creation",
        default=datetime.datetime.now,
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        comment="Date and time of last update",
        default=datetime.datetime.now,
        server_default=func.now(),
        onupdate=func.now(),
    )
    deleted_at = Column(
        DateTime, nullable=True, comment="Date and time of logic deletion"
    )
    is_deleted = Column(
        Boolean,
        nullable=False,
        comment="Is object marked as deleted",
        default=False,
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_dict_lower(self):
        return {
            str.lower(c.name): getattr(self, c.name)
            for c in self.__table__.columns
        }
