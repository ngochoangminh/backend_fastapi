
from core.base import BaseSqlOrm, get_common_id_column, get_common_columns
from ..entities import User
from sqlalchemy import String, Column, Table, UniqueConstraint

class UserORM(User, BaseSqlOrm):
    __table__ = Table(
        "users",
        BaseSqlOrm.metadata,
        get_common_id_column(),
        Column("first_name", String, nullable=False),
        Column("last_name", String, nullable=False),
        Column("phone", String,index=True, nullable=True, unique=True),
        Column("email", String, index=True, nullable=False),
        Column("username", String, index=True, nullable=True),
        Column("role", String, nullable=True),
        Column("password", String),
        *get_common_columns(),
        UniqueConstraint("username"),
        UniqueConstraint("phone"),
        UniqueConstraint("email")
    )