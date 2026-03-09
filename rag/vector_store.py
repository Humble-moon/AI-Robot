from langchain_chroma import Chroma
from langchain_core.documents import Document
from utils.config_handler import chroma_conf
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.path_tool import get_abs_path
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex, batch_load_documents
from utils.logger_handler import logger
import os


class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embed_model,
            persist_directory=chroma_conf["persist_directory"]
        )
        self.spliter = None
        self.cache = {}  # 添加缓存字典

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            separators=chroma_conf["separators"],
            length_function=len,
        )

    def get_retriever(self):
        # 缓存检索器实例
        if "retriever" not in self.cache:
            self.cache["retriever"] = self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})
        return self.cache["retriever"]

    def load_document(self):
        """
        从数据文件夹内读取数据文件，转为向量存入向量库
        要计算文件的MD5做去重
        :return: None
        """

        def check_md5_hex(md5_for_check: str):
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                open(get_abs_path(chroma_conf["md5_hex_store"]), "w", encoding="utf-8").close()
                return False
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True
                return False

        def save_md5_hex(md5_for_save: str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_for_save + "\n")

        def get_file_documents(read_path: str):
            if read_path.endswith("txt"):
                return txt_loader(read_path)

            if read_path.endswith("pdf"):
                return pdf_loader(read_path)

            return []

        allowed_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allow_knowledge_file_type"]),
        )

        # 过滤出未处理的文件
        unprocessed_files = []
        for path in allowed_files_path:
            md5_hex = get_file_md5_hex(path)
            if not check_md5_hex(md5_hex):
                unprocessed_files.append((path, md5_hex))
            else:
                logger.info(f"[加载知识库]文件 {path} 已存在知识库内")

        if unprocessed_files:
            try:
                # 批量加载文档
                file_paths = [path for path, _ in unprocessed_files]
                documents = batch_load_documents(file_paths)
                
                if documents:
                    # 批量分块
                    split_documents = self.spliter.split_documents(documents)
                    
                    if split_documents:
                        # 批量向量化并存储
                        self.vector_store.add_documents(split_documents)
                        
                        # 批量记录MD5
                        for path, md5_hex in unprocessed_files:
                            save_md5_hex(md5_hex)
                            logger.info(f"[加载知识库]{path} 内容加载成功")
                    else:
                        logger.warning("[加载知识库]分片后没有有效文本内容，跳过")
                else:
                    logger.warning("[加载知识库]没有有效文本内容，跳过")
            except Exception as e:
                # exc_info为True会记录详细的报错堆栈，如果为False仅记录报错信息本身
                logger.error(f"[加载知识库]批量处理失败: {str(e)}", exc_info=True)


if __name__ == '__main__':
    vs = VectorStoreService()

    vs.load_document()

    retriever = vs.get_retriever()

    res = retriever.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("-" * 20)
