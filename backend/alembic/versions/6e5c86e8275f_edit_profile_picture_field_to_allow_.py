"""edit profile_picture field to allow nullable values

Revision ID: 6e5c86e8275f
Revises: 37f277560330
Create Date: 2024-11-15 15:09:23.296877

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e5c86e8275f'
down_revision: Union[str, None] = '37f277560330'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_picture', sa.String(), nullable=True))
    op.drop_column('users', 'logo_path')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('logo_path', sa.VARCHAR(), server_default=sa.text("'/logos/default.png'::character varying"), autoincrement=False, nullable=False))
    op.drop_column('users', 'profile_picture')
    # ### end Alembic commands ###