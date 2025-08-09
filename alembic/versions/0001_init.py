"""init tables

Revision ID: ea4c9c0bd002
Revises: 
Create Date: 2025-08-08 11:26:17

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "5f975902afec"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'uids',
        sa.Column('uid', sa.String(length=36), primary_key=True),
        sa.Column('status', sa.String(length=16), nullable=False, index=True),
        sa.Column('assigned_user_id', sa.BigInteger(), nullable=True, index=True),
        sa.Column('plan_id', sa.BigInteger(), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

def downgrade():
    op.drop_table('uids')
