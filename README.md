# 智扫通机器人智能客服系统

## 项目概述

智扫通机器人智能客服系统是基于大语言模型（LLM）的智能问答系统，结合RAG（检索增强生成）和Agent（智能体）技术，为用户提供扫地机器人相关的实时问答、故障排查、使用建议和个性化报告生成服务。

## 技术栈

- **核心语言**：Python 3.10+
- **AI框架**：LangChain（智能体构建、工具集成）
- **模型服务**：通义千问（ChatTongyi、DashScopeEmbeddings）
- **向量存储**：Chroma DB（文档向量化、相似性检索）
- **前端交互**：Streamlit（实时聊天界面、流式输出）
- **工具库**：Pandas（数据处理）、PDF/TXT解析器（文档处理）

## 项目结构

```
├── agent/             # 智能体相关代码
│   ├── tools/         # 智能体工具集
│   │   ├── agent_tools.py   # 工具函数实现
│   │   └── middleware.py    # 中间件实现
│   └── react_agent.py # 核心智能体实现
├── rag/               # RAG相关代码
│   ├── rag_service.py # RAG服务实现
│   └── vector_store.py # 向量存储服务
├── model/             # 模型相关代码
│   └── factory.py     # 模型工厂实现
├── config/            # 配置文件
│   ├── agent.yml      # 智能体配置
│   ├── chroma.yml     # Chroma配置
│   ├── prompts.yml    # 提示词配置
│   └── rag.yml        # RAG配置
├── data/              # 数据文件
│   ├── external/      # 外部数据
│   └── *.pdf/*.txt     # 产品文档
├── prompts/           # 提示词模板
├── utils/             # 工具类
│   ├── config_handler.py    # 配置处理
│   ├── file_handler.py      # 文件处理
│   ├── logger_handler.py    # 日志处理
│   ├── path_tool.py         # 路径工具
│   └── prompt_loader.py     # 提示词加载
├── app.py             # 应用入口
└── README.md          # 项目文档
```

## 核心组件

### 1. 智能体系统 (ReactAgent)

**文件路径**：`agent/react_agent.py`

**功能描述**：基于LangChain的Agent框架实现的智能体系统，能够根据用户问题自主决策调用工具。

**核心方法**：

| 方法名 | 功能描述 | 参数 | 返回值 |
|-------|---------|------|--------|
| `__init__` | 初始化智能体 | 无 | 无 |
| `execute_stream` | 执行流式响应 | query: str (用户查询) | 生成器 (流式输出) |

**使用示例**：

```python
from agent.react_agent import ReactAgent

agent = ReactAgent()
for chunk in agent.execute_stream("如何清洁扫地机器人"):
    print(chunk, end="", flush=True)
```

### 2. 智能体工具集

**文件路径**：`agent/tools/agent_tools.py`

**功能描述**：智能体可使用的工具集合，支持多种功能操作。

**核心工具**：

| 工具名 | 功能描述 | 参数 | 返回值 |
|-------|---------|------|--------|
| `rag_summarize` | 从向量存储中检索参考资料 | query: str | 总结结果 |
| `get_weather` | 获取指定城市的天气 | city: str | 天气信息 |
| `get_user_location` | 获取用户所在城市 | 无 | 城市名称 |
| `get_user_id` | 获取用户ID | 无 | 用户ID |
| `get_current_month` | 获取当前月份 | 无 | 月份字符串 |
| `fetch_external_data` | 获取用户使用记录 | user_id: str, month: str | 使用记录 |
| `fill_context_for_report` | 触发报告生成上下文 | 无 | 确认消息 |

### 3. RAG服务 (RagSummarizeService)

**文件路径**：`rag/rag_service.py`

**功能描述**：实现检索增强生成功能，从向量库中检索相关文档并生成回答。

**核心方法**：

| 方法名 | 功能描述 | 参数 | 返回值 |
|-------|---------|------|--------|
| `__init__` | 初始化RAG服务 | 无 | 无 |
| `retriever_docs` | 检索相关文档 | query: str | 文档列表 |
| `rag_summarize` | 生成增强回答 | query: str | 总结结果 |

### 4. 向量存储服务 (VectorStoreService)

**文件路径**：`rag/vector_store.py`

**功能描述**：基于Chroma实现向量存储，处理文档加载、分块和向量化。

**核心方法**：

| 方法名 | 功能描述 | 参数 | 返回值 |
|-------|---------|------|--------|
| `__init__` | 初始化向量存储服务 | 无 | 无 |
| `get_retriever` | 获取检索器 | 无 | 检索器实例 |
| `load_document` | 加载文档到向量库 | 无 | 无 |

### 5. 模型工厂 (ModelFactory)

**文件路径**：`model/factory.py`

**功能描述**：采用工厂模式管理模型实例，提供聊天模型和嵌入模型。

**核心类**：

| 类名 | 功能描述 | 核心方法 |
|-----|---------|----------|
| `BaseModelFactory` | 基础模型工厂抽象类 | `generator()` |
| `ChatModelFactory` | 聊天模型工厂 | `generator()` |
| `EmbeddingsFactory` | 嵌入模型工厂 | `generator()` |

**全局实例**：
- `chat_model`：聊天模型实例
- `embed_model`：嵌入模型实例

## 配置系统

项目使用YAML格式的配置文件，存放在`config/`目录下：

### 1. agent.yml

智能体相关配置，包括外部数据路径等。

### 2. chroma.yml

Chroma向量存储相关配置，包括：
- collection_name：集合名称
- persist_directory：持久化目录
- chunk_size：文档分块大小
- chunk_overlap：分块重叠大小
- separators：分块分隔符
- k：检索文档数量
- md5_hex_store：MD5存储文件
- data_path：数据文件路径
- allow_knowledge_file_type：允许的文件类型

### 3. rag.yml

RAG相关配置，包括模型名称等。

### 4. prompts.yml

提示词相关配置，包括提示词文件路径等。

## 数据流

### 1. 文档处理流程

1. 从`data/`目录读取文档文件
2. 计算文件MD5值，检查是否已处理
3. 解析文档内容（PDF/TXT）
4. 文档分块处理
5. 向量化存储到Chroma DB
6. 记录已处理文件的MD5值

### 2. 问答处理流程

1. 用户输入问题
2. 智能体分析问题类型
3. 根据需要调用相应工具：
   - 产品信息：调用`rag_summarize`检索文档
   - 天气查询：调用`get_weather`获取天气
   - 使用报告：调用`fetch_external_data`获取数据
4. 工具返回结果
5. 智能体整合信息生成回答
6. 流式输出回答给用户

## 前端界面

**文件路径**：`app.py`

基于Streamlit实现的实时聊天界面，具有以下特点：

- 橙色白色主题风格
- 流式输出响应
- 维护对话历史
- 响应式布局
- 欢迎消息提示

## 部署与运行

### 环境要求

- Python 3.10+
- 安装依赖：
  ```bash
  pip install streamlit langchain langchain_chroma langchain_community pandas pypdf
  ```

### 运行方式

1. 启动应用：
   ```bash
   python -m streamlit run app.py
   ```

2. 访问地址：
   - 本地：http://localhost:8501
   - 网络：http://[IP地址]:8501

### 首次运行

首次运行时，系统会自动：
1. 加载`data/`目录下的文档
2. 处理文档并存储到向量库
3. 初始化智能体和相关服务

## 日志系统

项目使用Python标准日志模块，日志文件存储在`logs/`目录下，按日期命名（如`agent_20260125.log`）。

## 扩展与维护

### 1. 添加新工具

在`agent/tools/agent_tools.py`中添加新的工具函数，使用`@tool`装饰器标记。

### 2. 添加新文档

将新文档放入`data/`目录，系统会自动处理并添加到向量库。

### 3. 修改配置

根据需要修改`config/`目录下的配置文件。

### 4. 更换模型

修改`model/factory.py`中的模型初始化代码，或修改`config/rag.yml`中的模型配置。

## 技术亮点

1. **模块化架构**：清晰分离智能体、RAG服务、向量存储、模型工厂等核心组件
2. **工具集成**：丰富的工具集，增强智能体能力
3. **RAG技术**：结合文档知识，提高回答准确性
4. **流式输出**：提供实时响应体验
5. **提示词切换**：根据场景动态调整提示词
6. **向量存储优化**：实现文档去重，提高存储效率
7. **外部数据集成**：可获取用户使用记录等外部数据

## 优化内容

### 1. 性能优化

- **向量存储性能**：调整分块策略（chunk_size从200增加到800，chunk_overlap从20增加到80），添加缓存机制
- **模型调用性能**：为ChatTongyi模型添加参数调优（temperature=0.3, max_tokens=2000, top_p=0.9），添加查询结果缓存
- **代码执行性能**：优化文档加载和处理流程，使用批量处理提高效率

### 2. 功能扩展

- **新增工具**：
  - `compare_robots`：比较不同型号扫地机器人的功能和价格
  - `get_robot_price`：获取扫地机器人的价格信息
  - `generate_purchase_link`：生成扫地机器人的购买链接

### 3. 配置管理优化

- **环境变量支持**：允许通过环境变量覆盖配置文件中的设置
- **配置验证**：添加配置验证机制，确保配置文件包含必要的键

### 4. 数据处理优化

- **文档处理优化**：优化PDF和TXT文档加载函数，添加错误处理和元数据
- **批量处理**：添加批量加载文档的功能，提高处理效率
- **向量化优化**：使用批量向量化和存储，减少API调用次数

### 5. 错误处理和安全性

- **统一错误处理**：为所有工具函数添加输入验证和错误处理
- **异常捕获**：完善异常捕获和处理，避免系统崩溃
- **安全措施**：加强用户输入验证，防止注入攻击

### 6. 用户体验优化

- **界面设计**：添加侧边栏设置、主题选择、常见问题快捷按钮
- **交互体验**：添加欢迎消息，优化流式输出速度
- **响应速度**：减少延迟，提高响应速度

### 7. 部署和扩展性

- **配置灵活性**：支持通过环境变量配置，便于不同环境部署
- **模块化设计**：清晰的模块划分，便于扩展和维护
- **错误处理**：完善的错误处理机制，提高系统稳定性

## 应用场景

1. **智能客服**：回答用户关于扫地机器人的各种问题
2. **产品咨询**：基于产品文档提供详细信息
3. **故障排查**：根据故障排除文档提供解决方案
4. **使用报告**：生成用户使用情况报告
5. **个性化建议**：基于用户使用记录提供个性化建议


