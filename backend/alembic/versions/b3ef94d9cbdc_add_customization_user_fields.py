"""add customization user fields

Revision ID: b3ef94d9cbdc
Revises: 5cccf3a4b881
Create Date: 2024-11-19 18:04:23.334909

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b3ef94d9cbdc"
down_revision: Union[str, None] = "5cccf3a4b881"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("profession", sa.String(), nullable=True))
    op.add_column("users", sa.Column("country", sa.String(), nullable=True))
    op.add_column("users", sa.Column("city", sa.String(), nullable=True))
    op.add_column("users", sa.Column("birthdate", sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "birthdate")
    op.drop_column("users", "city")
    op.drop_column("users", "country")
    op.drop_column("users", "profession")
    # ### end Alembic commands ###