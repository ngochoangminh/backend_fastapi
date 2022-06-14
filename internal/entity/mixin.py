from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class TimestampMixin(object):

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    deleted_at = Column(DateTime)
