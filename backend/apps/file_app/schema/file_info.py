from pydantic import Field
from backend.common.schema import SchemaBase


class FileInfoSchema(SchemaBase):
    id: int = Field(..., description="文件ID")
    uuid: str = Field(..., description="文件唯一标识符")
    file_name: str = Field(..., description="文件名称")
    file_type: str = Field(..., description="文件类型")
    file_size: float = Field(..., description="文件大小（单位：字节）")
    is_deleted: int = Field(0, description="是否删除，0表示未删除，1表示已删除")

