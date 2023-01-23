import datetime
import uuid

from sqlalchemy import TIMESTAMP, Column
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.database.core import Base

NON_TABLE_COLUMNS: set = {'created_at', 'updated_at'}


class BaseModel(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4)  # noqa: VNE003
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<{0.__class__.__name__}(id={0.id!r})>'.format(self)

    def as_dict(self, *, exclude: set[str] | None = None, exclude_non_tabel_columns: bool = False):
        exclude_columns = set() if exclude is None else exclude
        if exclude_non_tabel_columns:
            exclude_columns.update(NON_TABLE_COLUMNS)
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns  # type: ignore
            if column.name not in exclude_columns
        }
