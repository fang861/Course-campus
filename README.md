# 校园课程智能助手
基于 Vue3 + FastAPI + LangChain + MCP 实现的多用户AI课程助手，支持课表查询、文档知识库问答、AI生成学习计划，基于RAG与ReAct Agent实现工具调用，严格用户数据隔离。

## 技术栈
- 前端：Vue3、Vite、Element Plus、Pinia、SSE、marked + DOMPurify
- 后端：FastAPI、SQLAlchemy、MySQL、JWT
- AI 能力：LangChain、LangGraph、FastMCP、Chroma、BGE-M3 Embedding、RAG
- 大模型：兼容OpenAI接口，默认对接DeepSeek
- IDE:vscode

## 角色说明
| 角色 | 入口 | 说明 |
| ---- | ---- | ---- |
| 学生 | /login → /user/home | 查看课表、检索课程文档、让AI生成并保存学习计划，用户数据隔离 |
| 管理员 | /login → /admin/home | 课程元数据管理、文档上传&向量入库、用户管理、知识库维护 |

## 演示账号
| 账号 | 密码 | 角色 |
| ---- | ---- | ---- |
| aaa | 123 | 学生（自带课表，用于演示查询课表、生成计划） |
| bbb | 123 | 学生（无课表，验证数据隔离） |
| admin | admin | 管理员，可上传文档、管理知识库与用户 |

## 启动步骤
1. 初始化数据库
```bash
# 导入初始化SQL
mysql -uroot -p密码 --default-character-set=utf8mb4 < backend/init-course.sql
```
2. 启动后端服务
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
服务地址：`[http://127.0.0.1:8000](http://127.0.0.1:8000)`
3. 启动FastMCP工具服务
```bash
cd mcp_server
python mcp_server.py
```
MCP地址：`[http://127.0.0.1:8001/mcp](http://127.0.0.1:8001/mcp)`
4. 启动Chroma向量库
```bash
chroma run --path ./chroma_db --port 8002
```
向量库地址：`[http://127.0.0.1:8002](http://127.0.0.1:8002)`
5. 启动前端
```bash
cd frontend
npm install
npm run dev
```
访问地址：`[http://127.0.0.1:5173](http://127.0.0.1:5173)`

> 注意：MCP服务未启动时Agent无法调用工具；Chroma未启动，文档检索、RAG问答不可用，演示前保证4个进程正常运行。

## 核心功能
- 学生端
  - 课表查询：查询个人课表，Agent可直接调用工具获取课表真实数据
  - 学习计划：支持手动新增，也可通过AI根据课程资料生成、保存学习计划
  - 知识库问答：基于已上传文档RAG检索，模型禁止编造知识库不存在内容
  - 数据隔离：不同学生之间课表、学习计划互相不可见
- 管理员端
  - 课程管理：维护课程名称、课程编码等元数据，与向量库解耦
  - 文档管理：支持 `.txt/.md/.pdf/.docx` 文档上传、批量入库；文档删除同步清理向量；支持入库预览、重新向量化；批量上传支持事务回滚
  - 用户管理：新增、管理系统账号
- AI Agent能力
  - ReAct模式编排，自动判断调用课表查询、文档检索、保存学习计划工具
  - SSE流式推送，前端实时展示工具调用过程与模型输出
  - RAG检索增强：文档分块、Embedding入库，回答附带原文来源

## AI配置（DeepSeek）
在 `.env` 或者系统配置页面填入：
```
ai_api_key=你的DeepSeek Key
ai_api_url=[https://api.deepseek.com/chat/completions](https://api.deepseek.com/chat/completions)
ai_model=deepseek-chat
embedding_model=bge-m3
embedding_base_url=硅基流动Embedding接口地址
```
未配置API Key时，AI问答与工具调用功能不可用；配置后学生端对话入口 `/user/ai-guide`，接口 `POST /api/agent/chat`

### RAG说明
检索增强生成分为写入、检索两段：
1. 写入（文档上传）：文档上传 → 文本提取 → 文本分块（单块500字，重叠50字）→ Embedding向量化 → 存入Chroma
2. 检索（用户提问）：问题向量化 → 相似度检索，返回Top3相关片段 → 交给大模型组织答案
> 区分异常：服务异常=检索失败；检索正常无匹配片段=知识库无相关内容，两种场景均禁止模型编造信息

### MCP说明
MCP把**查询课表、检索文档、保存学习计划**封装成标准工具，Agent通过MCP协议调用业务能力，实现大模型和业务逻辑解耦。

## 项目亮点
1. 基于MCP协议实现Agent工具化，业务能力和AI编排解耦，方便扩展新工具
2. 严格用户数据隔离，保证学生课表、学习计划私有，知识库文档全局共享
3. RAG做文档问答，做幻觉约束，有据可依
4. SSE流式输出，实时展示Agent思考与工具调用链路，面试可讲
5. 文档上传事务机制，批量上传失败支持回滚，保证向量库一致性
