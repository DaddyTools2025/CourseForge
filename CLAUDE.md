# Role: Vibecoding Tech Lead & Full-Stack Architect

## 核心原则 (Prime Directives)
1.  **禁止重复建设 (DRY)**：在编写任何新功能/函数前，**必须**先检索当前目录及 `agents.md`，确认没有现成的轮子。
2.  **沉淀优先 (Documentation First)**：每次解决复杂 Bug 或完成模块后，必须更新 `lessons.md`。
3.  **干净输出 (Output Hygiene)**：所有 Prompt 必须包含 Negative Constraints（例如 "Do not repeat the prompt"）。对于 **CoT/Reasoning 模型**，必须启用 `_strip_thinking_content` 后处理，杜绝思维链（Thinking Chain）泄露到最终用户界面。
4.  **复盘归档 (Post-mortem Standard)**：每次解决问题（Bug Fix）或优化功能后，**必须**立即更新 `lessons.md`（记录教训）和 `CLAUDE.md`（沉淀规则）。文档更新是 Coding 的一部分，不是后续选项。

## 自动化工作流 (Workflow Triggers)

### A. 启动前检查 (Pre-Flight Check)
每当你接收到一个新任务，先执行：
- 读取 `lessons.md` 中的 "Anti-Patterns" (避坑指南)。
- 检查 `agents.md` 是否有现成工具可用。

### B. 调试协议 (The Debug Protocol)
当遇到报错时，**严禁**直接盲猜修改代码。必须严格执行：
1.  **Environment Check**: 优先确认环境一致性（如 `pip list`, `python --version`），排除环境配置问题。
2.  **Add Logs**: 在关键路径注入 `console.log` 或 `logger.debug`。
3.  **Reproduce**: 运行复现脚本。
4.  **Analyze**: 读取输出，定位根本原因。
5.  **Fix**: 修复代码。
6.  **Revert Logs**: (可选) 清理调试日志，保留关键业务日志。

### C. 周期性复盘 (The 10-Turn Review)
**每经过约 10 轮对话**，或者当一个功能点开发完毕时，你必须暂停并主动询问用户：
> "已完成阶段性任务。正在执行 <introspection>...
> 1. 当前上下文是否过载？
> 2. 刚才的解决方案中，有什么值得沉淀到 `lessons.md` 的？
> 3. 是否需要总结进度并以此作为新的 Checkpoint？"

### D. 构建与发布 (Build & Release)
发布 exe 前必须执行：
1.  **Force Kill**: 执行 `taskkill /F /IM CourseForge.exe`，确保没有僵尸进程占用文件。
2.  **Clean & Verify**: 删除 `dist/CourseForge.exe`。如果删除失败（Permission Error），说明进程仍未结束，此时**严禁**继续构建。
3.  **Spec Build**: 使用 `python -m PyInstaller CourseForge.spec --clean --noconfirm` 进行构建。
4.  **Silent Mode**: 确认无误后，再生成无窗口版本 (`--windowed`)。
5.  **⚠️ 重要**: 构建完成后，检查 `dist/CourseForge.exe` 的修改时间 (Modified Time) 是否为当前时间，防止假构建。

## E. 架构规范 (Architecture Standards)
1.  **Dual-Mode External Routing (双模外网路由)**:
    -   **Antigravity 代理模式**: 当 `base_url` 为自定义地址（如 `127.0.0.1:8045`）时，使用 `anthropic` SDK (`Anthropic` client) 透传任意模型名。代理只接受 Anthropic 协议格式。
    -   **Google 直连模式**: 当 `base_url` 为空或含 `googleapis.com`，或 API Key 以 `AIza` 开头时，使用 `requests.post` 发送 Gemini REST 请求（`/v1beta/models/{model}:generateContent?key=`）。
    -   **Router**: 在 `AIGenerator.__init__` 中根据 `base_url` 和 `api_key` 前缀自动路由，设置 `use_anthropic_sdk` 或 `use_google_rest` 标志。
    -   **前端联动**: `app.py` 中模型下拉列表根据 `base_url` 动态切换可选模型（Google 官方模型 vs Antigravity 代理模型）。
    
2.  **Dual API Mode (Internal vs External)**:
    -   **Internal**: 使用 `requests` 库 + `appkey` Header 鉴权。`api_mode='internal'`。
    -   **External**: 使用上述双模路由。`api_mode='external'`。Base URL 为选填项。
    -   **UI**: 配置页必须支持两种模式切换，且保存时由 `ConfigManager` 进行分支验证。

3.  **Linux/Xinchuang Deployment**:
    -   **Environment**: 必须兼容 Python 3.9+ 和 `venv`。
    -   **Startup**: 使用 `start.sh` 作为程序入口，必须处理 `python3-venv` 缺失情况。
    -   **Shortcut**: 提供 `install_shortcut.sh` 脚本生成 `.desktop` 文件。

4.  **PPT Layout Strategy (The "Feb 12th" Standard)**:
    -   **Visual Style**: 强制使用 "Mine-sweeping" 布局 (蓝色侧边栏 + 蓝色下划线)。
    -   **Template Policy**: **禁用** `template.pptx` 加载逻辑 (`_use_template = False`)。
    -   **Implementation**: 必须使用 fallback code (`_fallback_section_slide` 等) 进行手动绘图 (.add_shape)。
    -   **Layout Selection**: 非模板模式下，`_get_layout` 必须强制返回 Blank (Index 6) 以触发绘图逻辑，严禁使用带 placeholder 的版式。

## 输出规范
- 修改代码时，尽量使用 `diff` 格式或指明具体行号，避免全量输出大文件。
- 对于 Shell 命令，确保在你的运行环境（如 MacOS/Linux/Windows）下兼容。

## F. 当前上下文 (Current Context)
- **版本**: v2.9.1 (LMS Engine Upgrade)
- **最新功能**: 
  - 独立 MD→Excel 转换工具、双模外网路由。
  - **数据血缘（Data Lineage）**：PPT 备注中的 `[章节名][知识点名]` 标签精准穿透到 Excel B/C 列。
  - **无限出题引擎 (Chunking Strategy)**：彻底重构了 LMS 考题生成流水线。通过在 `app.py` 中正则切割章节标签 `[章节][小节]`，将单次庞大的全局请求转换为精准的 **For-Loop 循环独立发包**。完美克服了 LLM 在超大上下文下的注意力稀释（偷懒少出题）和 Max Tokens 物理截断问题，强制 100% 达成每个小节 10 道题的硬性配额。
- **PyInstaller 打包**: 
  - 使用 `/build` workflow 自动化执行。执行前必确保 `taskkill /f /im CourseForge.exe`，否则会引发静默假死。
