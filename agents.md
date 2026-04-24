# CourseForge 项目自动化手册
*此文件汇总所有 Agent Skills 和 Workflows，方便快速查阅和调用。*

---

## 📂 文件地图

| 文件 | 用途 | 维护频率 |
|------|------|---------|
| `CLAUDE.md` | 架构规范 + 调试协议 + 构建规则 | 每次架构变更后更新 |
| `lessons.md` | 血泪教训库（Bug 复盘 + Anti-Pattern） | 每次修复 Bug 后追加 |
| `agents.md` | **本文件**，Skill/Workflow 速查 | 新增自动化时更新 |
| `.agents/workflows/*.md` | 可执行的自动化工作流 | 流程变更时更新 |

---

## ⚡ Workflows（自动化工作流）

> 输入斜杠命令即可触发，标记 `// turbo` 的步骤会自动执行。

### `/build` — 打包集成
**文件**: `.agents/workflows/build.md`
**用途**: 编译 EXE 并验证产物
**成本建议**: 💰 切换到低成本模型执行（如 gemini-flash）
**步骤概要**:
1. `taskkill /f /im CourseForge.exe` — 终止旧进程
2. 清理 `dist/CourseForge.exe`
3. `python -m PyInstaller --clean --noconfirm CourseForge.spec` — 构建
4. 验证产物（文件大小 + 时间戳）
5. 通知用户

### `/update_api_models` — 更新 API 模型列表
**文件**: `.agents/workflows/update_api_models.md`
**用途**: 在前端下拉列表中新增或更新可选模型
**步骤概要**:
1. 修改 `app.py` 中 `st.selectbox` 的 `options` 数组
2. `python -m py_compile app.py` — 语法验证
3. 执行 `/build` 重新打包

---

## 🧩 Skills（高级技能）

### `/summarize` — 阶段性总结
**触发**: 任务完成时或用户手动输入
**动作**:
1. 读取最近对话历史
2. 更新 `lessons.md` → "Current Context"
3. 发现新 Bug 模式则追加 "Solved Mysteries"
4. 输出简短报告

### `/debug-mode` — 调试协议
**触发**: 遇到报错或用户说"帮我调试"
**动作**:
1. 分析报错文件（**禁止**直接盲猜修改）
2. 先检查环境 → 插入日志 → 复现 → 定位 → 修复
3. 生成临时调试脚本

### `/refactor` — 代码重构
**触发**: 代码混乱或出现重复逻辑
**动作**:
1. 对照 `CLAUDE.md` 代码规范
2. 识别重复代码
3. 提炼独立函数并记录路径

### `/clean` — 清洗 AI 输出
**触发**: AI 输出包含提示词或废话
**动作**:
1. 读取 `prompts.py` 对应模板
2. 添加 Negative Constraints
3. 检查 CoT 模型是否启用 `_strip_thinking_content`
4. 提示重新生成

---

## 🏗️ 核心模块速查

| 模块 | 文件 | 职责 |
|------|------|------|
| AI 引擎 | `modules/ai_generator.py` | 双模路由（Anthropic SDK / Google REST）、重试、CoT 清洗 |
| Prompt 模板 | `modules/prompts.py` | 所有 AI prompt（含场景测试元数据标签） |
| PPT 构建 | `modules/ppt_builder.py` | "蓝色矿扫"手绘布局、PPT 备注强化 |
| Excel 导出 | `modules/excel_exporter.py` | openpyxl 无损装填、垂直多行写入 |
| 题库转换 | `modules/quiz_converter.py` | MD→JSON 解析、截断 JSON 修复、双轨回退 |
| 配置管理 | `modules/config_manager.py` | 内网/外网双模验证、持久化存储 |
| 文件解析 | `modules/file_parser.py` | PDF/DOCX/PPTX 内容提取 |
| 前端 UI | `app.py` | Streamlit 主界面、独立转换工具 |
| 打包配置 | `CourseForge.spec` | PyInstaller 规格（含 assets 显式引用） |