import os, hashlib
from utils.logger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader


def get_file_md5_hex(filepath: str):
    """
    计算文件的 MD5 哈希值并返回十六进制字符串

    Args:
        filepath: 文件路径字符串

    Returns:
        str: 32位十六进制MD5哈希值
        None: 如果计算失败（文件不存在、不是文件、读取错误等）
    """

    # 1. 检查文件是否存在
    if not os.path.exists(filepath):
        logger.error(f"[md5计算]文件 {filepath}不存在")
        return  # 返回None，表示计算失败

    # 2. 检查路径是否为文件（不是目录）
    if not os.path.isfile(filepath):
        logger.error(f"[md5计算]路径 {filepath} 不是一个文件")
        return  # 返回None，表示计算失败

    # 3. 创建MD5哈希计算对象
    md5_obj = hashlib.md5()
    chunk_size = 4096  # 每次读取4KB的数据块，避免一次性加载大文件导致内存不足

    try:
        # 4. 以二进制读取模式打开文件
        with open(filepath, "rb") as f:
            # 5. 分块读取文件内容
            while chunk := f.read(chunk_size):  # 海象运算符：读取数据块并赋值给chunk
                # 6. 将读取到的数据块更新到MD5计算中
                md5_obj.update(chunk)
            # 7. 计算最终的MD5哈希值（十六进制字符串）
            md5_hex = md5_obj.hexdigest()
            # 8. 返回32位十六进制哈希字符串
            return md5_hex

    except Exception as e:
        # 9. 处理读取文件时可能出现的异常
        logger.error(f"[md5计算]文件 {filepath} 读取失败,{str(e)}")
        return None  # 明确返回None表示计算失败


def listdir_with_allowed_type(path: str, allow_types: tuple[str]):
    files = []
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]{path}不是文件夹")
        return allow_types
    for f in os.listdir(path):
        if f.endswith(allow_types):
            files.append(os.path.join(path, f))
    return tuple(files)


def pdf_loader(filepath: str, password=None) -> list[Document]:
    try:
        loader = PyPDFLoader(filepath, password)
        documents = loader.load()
        # 添加元数据，包含文件路径和类型
        for doc in documents:
            doc.metadata["file_path"] = filepath
            doc.metadata["file_type"] = "pdf"
        return documents
    except Exception as e:
        logger.error(f"[PDF加载]文件 {filepath} 加载失败: {str(e)}")
        return []


def txt_loader(filepath: str) -> list[Document]:
    try:
        loader = TextLoader(filepath, encoding="utf-8")
        documents = loader.load()
        # 添加元数据，包含文件路径和类型
        for doc in documents:
            doc.metadata["file_path"] = filepath
            doc.metadata["file_type"] = "txt"
        return documents
    except Exception as e:
        logger.error(f"[TXT加载]文件 {filepath} 加载失败: {str(e)}")
        return []


def batch_load_documents(filepaths: list[str]) -> list[Document]:
    """
    批量加载文档
    
    Args:
        filepaths: 文件路径列表
    
    Returns:
        list[Document]: 加载的文档列表
    """
    documents = []
    for filepath in filepaths:
        if filepath.endswith(".pdf"):
            documents.extend(pdf_loader(filepath))
        elif filepath.endswith(".txt"):
            documents.extend(txt_loader(filepath))
        else:
            logger.warning(f"[批量加载]不支持的文件类型: {filepath}")
    return documents
