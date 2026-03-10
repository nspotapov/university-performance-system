"""Add OTP fields to users table

Revision ID: 2026_03_10_1200
Revises: bdff415e2569
Create Date: 2026-03-10 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '2026_03_10_1200'
down_revision: Union[str, None] = 'bdff415e2569'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем новые поля в таблицу users
    op.add_column('users', sa.Column('otp_code', sa.String(length=10), nullable=True))
    op.add_column('users', sa.Column('otp_expires_at', sa.DateTime(), nullable=True))
    
    # Делаем email уникальным (если еще не сделано)
    op.create_unique_constraint('uq_users_email', 'users', ['email'])
    op.create_index('ix_users_email', 'users', ['email'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_users_email', table_name='users')
    op.drop_constraint('uq_users_email', 'users', type_='unique')
    op.drop_column('users', 'otp_expires_at')
    op.drop_column('users', 'otp_code')
