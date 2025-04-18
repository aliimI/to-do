"""re-add repeat field properly inshallah

Revision ID: c355e3e7d9c2
Revises: ca624dc89883
Create Date: 2025-04-14 16:58:29.970248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c355e3e7d9c2'
down_revision: Union[str, None] = 'ca624dc89883'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('repeat', sa.String(), server_default=sa.text("'None'"), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'repeat')
    # ### end Alembic commands ###
