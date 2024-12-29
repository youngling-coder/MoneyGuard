"""add gender field to User

Revision ID: d3940e3a77a3
Revises: f0ddbd49ae3e
Create Date: 2024-12-29 16:46:16.556317

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d3940e3a77a3"
down_revision: Union[str, None] = "f0ddbd49ae3e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

gender_enum = sa.Enum("MALE", "FEMALE", name="gender")


def upgrade() -> None:
    gender_enum.create(op.get_bind(), checkfirst=True)
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("gender", gender_enum, nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "gender")
    gender_enum.drop(op.get_bind(), checkfirst=True)
    # ### end Alembic commands ###
