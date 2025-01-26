"""rename description field to category

Revision ID: 7e171eba4463
Revises: d3940e3a77a3
Create Date: 2025-01-26 15:27:30.338270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e171eba4463'
down_revision: Union[str, None] = 'd3940e3a77a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('category', sa.String(), nullable=False))
    op.drop_column('transactions', 'description')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('description', sa.VARCHAR(), autoincrement=False))
    op.drop_column('transactions', 'category')
    # ### end Alembic commands ###
