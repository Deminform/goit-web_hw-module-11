"""Second revision

Revision ID: e275b8baaf6a
Revises: 5f3d0fbd0b19
Create Date: 2024-11-09 11:14:43.864529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e275b8baaf6a'
down_revision: Union[str, None] = '5f3d0fbd0b19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('first_name', sa.String(length=50), nullable=False))
    op.add_column('contacts', sa.Column('last_name', sa.String(length=50), nullable=False))
    op.drop_column('contacts', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.drop_column('contacts', 'last_name')
    op.drop_column('contacts', 'first_name')
    # ### end Alembic commands ###
