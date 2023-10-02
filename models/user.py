import sqlalchemy as sa

from db import metadata
from models.enums import RoleType


user = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("email", sa.String(120), unique=True),
    sa.Column("password", sa.String(255)),
    sa.Column("first_name", sa.String(200)),
    sa.Column("last_name", sa.String(200)),
    sa.Column("phone", sa.String(20)),
    sa.Column("role", sa.Enum(RoleType), nullable=False, server_default=RoleType.complainer.name),
    sa.Column("iban", sa.String(200))
)