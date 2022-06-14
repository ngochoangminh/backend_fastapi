from sqlalchemy import Column, text
from sqlalchemy import MetaData
from sqlalchemy.dialects import postgresql as psql
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class BaseEntity(object):
    __name__: str
    metadata: MetaData

    @declared_attr
    def __tablename__(cls):  # noqa: N805
        return cls.__name__.lower()

    id = Column(
        psql.UUID(as_uuid=True),
        server_default= text('gen_random_uuid()'),
        primary_key=True,
        index=True,
    )
