"""init

Revision ID: a058d0b2a495
Revises: 
Create Date: 2024-11-13 11:57:09.367000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a058d0b2a495'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file_base_info',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='主键id'),
    sa.Column('uuid', sa.String(length=32), nullable=False, comment='文件hash'),
    sa.Column('file_name', sa.String(length=50), nullable=False, comment='文件名称'),
    sa.Column('file_type', sa.String(length=8), nullable=False, comment='文件类型'),
    sa.Column('file_size', sa.Numeric(precision=10, scale=2), nullable=False, comment='文件大小'),
    sa.Column('is_deleted', sa.SmallInteger(), nullable=False, comment='是否删除'),
    sa.Column('created_time', sa.DateTime(), nullable=False, comment='创建时间'),
    sa.Column('updated_time', sa.DateTime(), nullable=True, comment='更新时间'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_file_base_info_id'), 'file_base_info', ['id'], unique=False)
    op.create_index('ix_file_unique', 'file_base_info', ['uuid'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_file_unique', table_name='file_base_info')
    op.drop_index(op.f('ix_file_base_info_id'), table_name='file_base_info')
    op.drop_table('file_base_info')
    # ### end Alembic commands ###
