from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.tables.base import BaseModel


class File(BaseModel):
    """File model."""

    __tablename__ = "files"

    name = Column(String, nullable=False, comment="File name")
    path = Column(String, nullable=False, unique=True, comment="Path to file")
    size = Column(Integer, nullable=False, comment="File size")
    is_downloadable = Column(Boolean, default=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
        comment="User",
    )
    user = relationship("User", back_populates="files", remote_side="User.id")

    def __repr__(self):
        return (
            f"<File(id={self.id}, name={self.name}, "
            f"path={self.path}, user={self.user})>"
        )
