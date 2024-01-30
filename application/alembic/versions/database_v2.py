"""Add support for access tokens

Revision ID: database_v2
Revises:
Create Date: 2023-10-08 14:10:31.088339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "database_v2"
down_revision = "database_v1"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tokens",
        sa.Column("token_id", sa.Integer(), nullable=False),
        sa.Column("token_active", sa.Boolean(), nullable=False),
        sa.Column("token_name", sa.String(length=256), nullable=False),
        sa.Column("token_value", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("token_id"),
        sa.UniqueConstraint("token_value"),
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tokens")
    # ### end Alembic commands ###
