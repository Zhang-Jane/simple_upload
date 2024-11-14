from sqlalchemy import String, Index, SmallInteger, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class FileInfo(Base):
    """
    文件基本信息表
    """
    # 指定数据库表的名称。
    __tablename__ = 'file_base_info'

    id: Mapped[id_key] = mapped_column(init=False)
    uuid: Mapped[str] = mapped_column(String(32), nullable=False, comment='文件hash')
    file_name: Mapped[str] = mapped_column(String(50), nullable=False, comment='文件名称')
    file_type: Mapped[str] = mapped_column(String(8), nullable=False, comment='文件类型')
    file_size: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, comment='文件大小')
    is_deleted: Mapped[int] = mapped_column(SmallInteger, default=0, comment='是否删除')


# 创建 B-tree 索引
Index('ix_file_unique', FileInfo.uuid, unique=True)
