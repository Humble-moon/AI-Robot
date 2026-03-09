from utils.path_tool import get_abs_path
import yaml
import os


def load_rag_config(config_path: str = get_abs_path("config/rag.yml"), encoding: str = "utf-8"):
    # 从文件加载配置
    with open(config_path, "r", encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    # 从环境变量覆盖配置
    if os.environ.get("RAG_CHAT_MODEL_NAME"):
        config["chat_model_name"] = os.environ.get("RAG_CHAT_MODEL_NAME")
    if os.environ.get("RAG_EMBEDDING_MODEL_NAME"):
        config["embedding_model_name"] = os.environ.get("RAG_EMBEDDING_MODEL_NAME")
    
    # 配置验证
    required_keys = ["chat_model_name", "embedding_model_name"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"配置文件缺少必要的键: {key}")
    
    return config

def load_chroma_config(config_path: str = get_abs_path("config/chroma.yml"), encoding: str = "utf-8"):
    # 从文件加载配置
    with open(config_path, "r", encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    # 从环境变量覆盖配置
    if os.environ.get("CHROMA_COLLECTION_NAME"):
        config["collection_name"] = os.environ.get("CHROMA_COLLECTION_NAME")
    if os.environ.get("CHROMA_PERSIST_DIRECTORY"):
        config["persist_directory"] = os.environ.get("CHROMA_PERSIST_DIRECTORY")
    if os.environ.get("CHROMA_CHUNK_SIZE"):
        config["chunk_size"] = int(os.environ.get("CHROMA_CHUNK_SIZE"))
    if os.environ.get("CHROMA_CHUNK_OVERLAP"):
        config["chunk_overlap"] = int(os.environ.get("CHROMA_CHUNK_OVERLAP"))
    if os.environ.get("CHROMA_K"):
        config["k"] = int(os.environ.get("CHROMA_K"))
    
    # 配置验证
    required_keys = ["collection_name", "persist_directory", "chunk_size", "chunk_overlap", "k"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"配置文件缺少必要的键: {key}")
    
    return config

def load_prompts_config(config_path: str = get_abs_path("config/prompts.yml"), encoding: str = "utf-8"):
    # 从文件加载配置
    with open(config_path, "r", encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    # 从环境变量覆盖配置
    if os.environ.get("PROMPTS_MAIN_PROMPT"):
        config["main_prompt"] = os.environ.get("PROMPTS_MAIN_PROMPT")
    if os.environ.get("PROMPTS_RAG_SUMMARIZE"):
        config["rag_summarize"] = os.environ.get("PROMPTS_RAG_SUMMARIZE")
    if os.environ.get("PROMPTS_REPORT_PROMPT"):
        config["report_prompt"] = os.environ.get("PROMPTS_REPORT_PROMPT")
    
    return config

def load_agent_config(config_path: str = get_abs_path("config/agent.yml"), encoding: str = "utf-8"):
    # 从文件加载配置
    with open(config_path, "r", encoding=encoding) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    
    # 从环境变量覆盖配置
    if os.environ.get("AGENT_EXTERNAL_DATA_PATH"):
        config["external_data_path"] = os.environ.get("AGENT_EXTERNAL_DATA_PATH")
    
    # 配置验证
    required_keys = ["external_data_path"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"配置文件缺少必要的键: {key}")
    
    return config


rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
agent_conf = load_agent_config()


if __name__ == '__main__':
    print(rag_conf["chat_model_name"])