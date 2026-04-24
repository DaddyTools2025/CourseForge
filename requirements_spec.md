# 业务与技术需求说明书 (BRD & TRD)

## 1. 文档概述
*   **项目名称**：CourseForge 铸课工坊
*   **版本号**：v2.4
*   **文档密级**：内部公开

## 2. 业务需求 (Business Requirements)

### 2.1 用户旅程 (User Journey)
1.  **启动与配置**：用户打开桌面应用，首次使用时输入 API Key 和 Base URL（支持私有化地址），并通过“连接测试”。
2.  **导入素材**：用户拖拽上传原始课件（支持 PDF/DOCX/PPTX）。
3.  **定义参数**：
    *   输入课程名称。
    *   选择受众画像（初级/中级）。
    *   勾选输出物清单（视频脚本、互动方案、PPT大纲等）。
4.  **一键生成**：点击生成按钮，系统实时显示各模块生成进度。
5.  **结果预览与导出**：
    *   在界面 Tab 页签中预览 Markdown 格式的内容。
    *   下载 `.md` 源文件或自动渲染好的 `.pptx` 文件。
    *   所有文件自动归档至本地 `outputs/` 目录。

### 2.2 功能列表 (Functional Requirements)

| 模块 | 功能点 | 描述 | 优先级 |
| :--- | :--- | :--- | :--- |
| **配置管理** | API 设置 | 支持自定义 Base URL（兼容 OpenAI 接口规范）及 Key | P0 |
| | 模型选择 | 下拉选择模型（Gemini-Pro, Claude-Sonnet 等） | P0 |
| | 连通性测试 | 提供“测试连接”按钮，验证配置有效性 | P1 |
| **文件解析** | 多格式支持 | 集成 PyPDF2, python-docx, python-pptx 解析库 | P0 |
| | 文本清洗 | 自动去除干扰字符、空白行，提取纯文本 | P1 |
| **AI 生成** | 核心提取 | 提炼课程 3-5 个核心知识点 (ADDIE - Analysis) | P0 |
| | 脚本生成 | 生成带分镜、画面的视频旁白脚本 (ADDIE - Develop) | P0 |
| | 互动设计 | 生成课堂互动游戏与话术 (ADDIE - Implement) | P1 |
| | PPT 自动化 | 生成 JSON 大纲并调用引擎渲染为 PPTX 文件 | P1 |
| **UI 交互** | 进度反馈 | 实时进度条与状态文字提示 | P1 |
| | 异常提示 | 红色警示框展示具体错误原因（如 429 限流） | P0 |

## 3. 技术需求 (Technical Requirements)

### 3.1 总体架构
采用 **C/S (Client/Server)** 架构，但在逻辑上通过 API 实现了 **Model-View-Controller (MVC)** 分层。

*   **View (表现层)**: `Streamlit` 框架。负责 UI 渲染、状态管理 (`st.session_state`)、文件流处理。
*   **Controller (控制层)**: `app.py` 主逻辑。负责参数校验、任务调度、进度回调。
*   **Model (业务逻辑层)**: `modules/` 包。
    *   `AIGenerator`: 核心 AI 引擎，封装了 Prompt 工程与 LLM 交互。
    *   `PromptTemplates`: 结构化提示词库。
    *   `ConfigManager`: 本地 JSON 配置文件读写。

### 3.2 关键技术实现

#### 3.2.1 混合 AI 引擎 (Hybrid SDK Router)
为解决本地代理环境下的协议兼容性问题，系统实现了 SDK 动态路由：
```python
if "gemini" in model_name.lower():
    # 使用 Google GenAI Native SDK (REST Transport)
    import google.generativeai as genai
    genai.configure(transport='rest', client_options={'api_endpoint': base_url})
else:
    # 使用 Anthropic SDK (OpenAI Compatible)
    from anthropic import Anthropic
    client = Anthropic(base_url=base_url)
```

#### 3.2.2 鲁棒性设计 (Resilience)
针对 LLM API 常见的限流问题，实现了指数退避重试算法：
*   **触发条件**：HTTP 429 (Too Many Requests), 503 (Service Unavailable), "ResourceExhausted"。
*   **策略**：`sleep_time = (2 ^ attempt) + random_jitter`。
*   **最大重试**：3次。

#### 3.2.3 桌面化封装 (Packaging)
使用 `PyInstaller` 进行单文件封装，确保在无 Python 环境的办公电脑上直接运行。
*   **Spec配置**：显式声明 `hiddenimports`（包括 `streamlit`, `anthropic`, `google.generativeai`），并处理 `collect_all` 以解决依赖缺失问题。
*   **运行参数**：注入 `--browser.gatherUsageStats=false` 防止启动卡死。

### 3.3 非功能性需求 (NFR)
1.  **安全性**：API Key 仅存储于用户本地 `~/.courseforge/config.json`，不上传任何云端服务器。
2.  **兼容性**：支持 Windows 10/11 64位操作系统。
3.  **响应性**：长文本生成任务（>30s）需保持 UI 活跃，不出现假死（通过 Streamlit 异步刷新机制实现）。

## 4. 交付物清单
1.  `CourseForge.exe`：绿色版可执行文件。
2.  `CLAUDE.md`：二次开发指南与代码规范。
3.  `lessons.md`：项目最佳实践与避坑文档。
