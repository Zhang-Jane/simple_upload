from urllib.parse import urlparse
from uuid import uuid4

from backend.utils.encrypt import Md5Cipher


def uuid4_str() -> str:
    """数据库引擎 UUID 类型兼容性解决方案"""
    return str(uuid4())


def md5_file(file_bytes: bytes):
    """
    :description: 获取文件的md5
    :param file_bytes: 文件路径
    :return: 文件的md5值
    """
    return Md5Cipher.encrypt(file_bytes)


def get_url_suffix(url):
    # 解析URL并获取路径部分
    path = urlparse(url).path
    # 提取文件的扩展名
    url_suffix = path.rsplit(".", 1)[-1].lower() if "." in path else None
    return url_suffix


def clean_file_name(file_name: str) -> str:
    # 去除前导和尾随空格
    cleaned_name = file_name.strip()
    # 替换中间的多个空格为单个空格
    cleaned_name = ''.join(cleaned_name.split())
    return cleaned_name
