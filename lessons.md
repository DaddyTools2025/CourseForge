# Project Wisdom & Lessons Learned
*此文件由 Claude 自动维护。记录所有“血泪教训”和“最佳实践”。*

## 🚧 Anti-Patterns (避坑指南 - 绝对不要做的事)
- [Streamlit] Avoid modifying `st.session_state` directly inside render loops without checks.
- [Streamlit] Do not perform heavy computations in the main thread without `@st.cache_data`.
- [PyInstaller] **Critical**: Do not use absolute sibling imports (e.g., `from prompts import x`) inside packages (`modules/`). Always use relative imports (`from .prompts import x`). PyInstaller isolates sub-packages rigidly.
- [Environment] **Critical**: Never assume a library is installed just because it's in the code. Always verify with `pip list` or `python -c "import x"` before debugging PyInstaller spec files.

## ✅ Solved Mysteries (已解决的疑难杂症)
- [2026-03-10] LMS Pipeline Freezes & Broken Quotas:
  - **Symptom**: User complains app hangs during PPT processing, and generated Excel fails to associate with chapters or lacks the mandated 10 questions per section. Local logs show errors calling multimodal APIs with `image_data`.
  - **Cause**: 
    1. Multimodal payload structure was missing `image_data` kwargs in `_call_ai`.
    2. Prompt contradictory constraints: "Generate 20 questions" vs "Generate 10 per section".
    3. PPT texts explicitly contained "1.1" or "Part 1" strings which polluted JSON `chapter`/`section` keys, causing mismatched Excel headers.
    4. Heavy LLM processing took 2-5 minutes synchronously without UI feedback, appearing hung.
  - **Fix**: 
    1. Explicitly appended `image_data: str = None` and passed via Base64 to both Google/Anthropic payload assemblers.
    2. Replaced soft constraints with "Rigid Quota Enforcement" & "Name Purification" (banning numeric prefixes) in prompts.
    3. Added `st.progress` callbacks bridged tightly into `enrich_pptx_in_place` loops for granular UI reporting.
  - **Lesson**: Soft prompting (e.g., "rather fewer questions than make things up") leads to lazy AI logic. Enforce strict numerical logic loops, and always show explicit progress bars for heavy AI operations to avoid perceived hangs.

- [2026-02-10] ModuleNotFoundError: No module named 'anthropic' in EXE:
  - **Fix**: `pip install anthropic`. (Always check environment first!)

- [2026-02-10] ModuleNotFoundError for Sibling Modules:
  - **Symptom**: `ModuleNotFoundError: No module named 'prompts'` inside `modules/ai_generator.py` when running EXE.
  - **Cause**: Absolute imports `from prompts import ...` fail in frozen environments where package paths are different.
  - **Fix**: Changed to relative import `from .prompts import ...`.

- [2026-02-10] OpenAI Client 502 Bad Gateway (Local Server):
  - **Symptom**: `openai` Python client returns 502 errors connecting to local inference server, while `curl` works.
  - **Cause**: Specific header/connection handling in `openai` SDK was incompatible with the local server implementation.
  - **Fix**: Switched to `anthropic` SDK, which handled the connection correctly.

- [2026-02-10] Streamlit EXE Hangs on Startup:
  - **Symptom**: Executable opens, shows "Welcome", asks for Email, and hangs.
  - **Fix**: Add `--browser.gatherUsageStats=false` to `sys.argv` in launcher.

- [2026-02-10] Invisible Logs in Packaged App (The "Red Box" Mystery):
  - **Symptom**: User got a "502 Error" but couldn't see why (e.g., "Model not found") because the console window was hidden or ignored.
  - **Fix**: Modified `ai_generator.py` to catch `anthropic.APIStatusError` and explicitly include `e.body` in the exception message raised to the UI.
  - **Lesson**: For desktop apps, **surface critical error details to the GUI**, do not rely on stdout/console logs.

- [2026-02-10] Streamlit CSS Over-Optimization (The "Missing Sidebar" Case):
  - **Symptom**: Hiding `header {visibility: hidden}` to remove the "Deploy" button accidentally hid the Sidebar Toggle (>), locking users out of settings.
  - **Fix**: Removed global `header` hiding; targeted specific elements (`#MainMenu`, `.stDeployButton`) instead. Added a backup "Settings" button in the main view.
  - **Lesson**: Use precise CSS selectors > global hiding. Always have a fallback navigation path.

- [2026-02-10] Hybrid SDK Strategy (The "Best of Both Worlds" Pattern):
  - **Symptom**: Local OneAPI/NewAPI proxies may not perfectly emulate Anthropic's headers for Google models, causing 502s or protocol errors.
  - **Fix**: Implemented a router in `AIGenerator`. If `model_name` contains "gemini", use native `google.generativeai` SDK; otherwise use `anthropic` SDK.
  - **Lesson**: Don't fight the proxy. If a native SDK works better for a specific provider, support both.

- [2026-02-10] Transient API Errors (429/503):
  - **Symptom**: "Resource has been exhausted" (Google 429) or "Capacity unavailable" (503).
  - **Fix**: Added exponential backoff retry loop (up to 3 retries) in `_call_ai`.
  - **Lesson**: Network programming 101: Always assume the network/API will fail. Retry logic is not optional.

- [2026-02-10] AttributeError in Error Handling (The "Crash during Crash"):
  - **Symptom**: Program crashed with `type object 'VibeLogger' has no attribute 'warn'` while trying to log a retryable error.
  - **Cause**: Typo in method name (`warn` vs `warning`).
  - **Fix**: Corrected to `VibeLogger.warning`.
  - **Lesson**: Error handling code paths are rarely executed; verify them specifically (or use static analysis).

- [2026-02-12] Internal Network Deployment (The "Offline" Reality):
  - **Symptom**: `pip install` hangs or fails in Xinchuang/Linux environments.
  - **Cause**: No direct internet access.
  - **Fix**: Updated `start.sh` to try Tsinghua mirror first, then fallback to default. Documented `pip download` offline installation strategy in `DEPLOY_LINUX.md`.
  - **Lesson**: Deployment scripts must assume zero internet access. Always provide offline alternatives.

- [2026-02-12] Linux Desktop Shortcuts (The "One-Click" Illusion):
  - **Symptom**: Users struggle to run `.sh` files from GUI file managers (often opens text editor).
  - **Fix**: Created `install_shortcut.sh` to generate a standard XDG `.desktop` file.
  - **Lesson**: For Linux desktop users, a `.desktop` file is the only "true" executable experience.

- [2026-02-12] JSON Parsing Failure with Chatty Models (The "Thinking" Trap):
  - **Symptom**: `Expecting value: line 1 column 1` when parsing JSON from advanced models (Gemini 1.5 Pro, DeepSeek R1/COT).
  - **Cause**: These models output "thinking process" or conversational filler (e.g., "Here is the JSON...") *before* the actual code block.
  - **Fix**: 
    1. **Robust Extraction**: Updated `PPTBuilder.build_from_json` to extract substring between outer `{}`.
    2. **Prompt Engineering**: Hardened `get_ppt_outline_prompt` with negative constraints ("No conversational text", "JSON ONLY").
  - **Lesson**: Relying on prompt engineering alone is insufficient for chatty models; robust parsing logic is mandatory.

- [2026-02-12] Prompt Leakage (The "Parrot" Effect):
  - **Symptom**: Generated content includes prompt instructions (e.g., "Based on the content...", "Here is the table...").
  - **Cause**: Chat models often treat the prompt as a conversation starter rather than a strict command.
  - **Fix**:
    1. **Negative Constraints**: Add "Do not repeat instructions" / "Direct output only" to `DEFAULT_SYSTEM_PROMPT`.
    2. **Zero-Shot Enforcing**: In specific prompts, add "Start directly with [Title]" or "Zero-Shot Output".
  - **Lesson**: Explicitly tell the model what *not* to do, especially regarding "conversational filler".

## 🧩 Reusable Snippets (高频代码片段)
- **Defensive Logging**:
  ```python
  from datetime import datetime
  print(f"[VIBE-DEBUG-{datetime.now().isoformat()}]", *args)
  ```

## 📝 Current Context (当前上下文快照)
- **Status**: v2.9.1 Release (LMS Engine Upgrade). 
  - **Feature 1**: 数据血缘（Data Lineage）— 强化版 PPT 备注中的 `[章节名][知识点名]` 标签精准穿透，并彻底移除了导致降级幻觉的 `doc_extractor` 依赖。
  - **Feature 2**: 无限出题引擎 (For-Loop Chunking Strategy) — 在 `app.py` 内部依靠正则自动切割 PPT 章节块，按章节维度向模型循环发送 Prompt，彻底杜绝了大模型在一次性长上下文出题时的偷懒少题、以及长文本截断问题（10题配额刚性 100% 达成）。
  - **Scope**: 修改了 `app.py` 的解析与重组逻辑、清除了已废弃的幽灵模块。
- **Next**: 等待新的业务需求和功能迭代。

## ⚡ Key Reminder (重要提醒)
- [2026-02-12] **EXE 不会自动同步源码变更**:
  - **Symptom**: 修改了 `app.py` / `ai_generator.py` / `prompts.py`，但 `dist/CourseForge.exe` 打开后界面没有变化。
  - **Cause**: PyInstaller 打包的 EXE 是静态快照，修改源码后必须重新构建。
  - **Fix**: 每次修改源码后执行 `pyinstaller CourseForge.spec --clean --noconfirm` 重新生成 EXE。
  - **Alternative**: 开发调试时直接用 `streamlit run app.py` 或 `python run_app.py` 运行源码，避免反复打包。

- [2026-02-12] Command Not Found: pyinstaller (PATH Issue):
  - **Symptom**: `pyinstaller : The term 'pyinstaller' is not recognized...` even after installing requirements.
  - **Cause**: The `Scripts` directory of the Python environment is not in the system PATH.
  - **Fix**: content
    1. **Immediate**: Use `python -m PyInstaller ...` instead of `pyinstaller ...`. This invokes the module directly via the active Python interpreter.
    2. **Doc Update**: Updated `CLAUDE.md` and `agents.md` to prioritize `python -m` syntax.
  - **Lesson**: `python -m <module>` is always safer than relying on PATH for CLI tools.

- [2026-02-12] Frontend Checkboxes Ignored (The "All or Nothing" Bug):
  - **Symptom**: User selected only "Standard PPT", but the system generated all materials.
  - **Cause**: The `app.py` frontend had checkboxes but didn't pass their state to `ai_generator.py`, which defaulted to running all steps.
  - **Fix**: Refactored `generate_all_materials` to accept an `options` dictionary and implemented conditional logic for each step + dynamic progress calculation.
  - **Lesson**: UI controls must be explicitly wired to backend logic; never assume "it just works".

  - **Lesson**: UI controls must be explicitly wired to backend logic; never assume "it just works".

- [2026-02-13] Output Folder Naming (The "Untitled" Fallback):
  - **Symptom**: User didn't enter a course name, so output folder was `outputs/未命名课程_...`, losing context.
  - **Fix**: Use uploaded file's basename (`os.path.splitext(uploaded_file.name)[0]`) as default course name.
  - **Lesson**: Don't default to generic names; context is already available in the input filename.

- [2026-02-13] Reasoning Models Pollution (The "Thinking Out Loud" Issue):
  - **Symptom**: CoT models (Cot-Deep, Cot-Max) include English reasoning process in `content` field.
  - **Fix**:
    1. **Prompt Constraint**: Added "Direct Output", "No Thinking Chain" to `get_content_extraction_prompt`.
    2. **Post-Processing**: Implemented `_strip_thinking_content` to regex-match `## ` Chinese heading and strip preceding text.
  - **Lesson**: Never trust prompt engineering alone for CoT models; always implement a deterministic cleaning layer.

- [2026-02-13] PPT Template Styles Lost (The "Manual Override" Bug - RESTORED):
  - **Symptom**: PPT generated with template didn't use template fonts/colors.
  - **Initial Fix**: Skipped manual styling to inherit template.
  - **Regression**: Caused vertical text and layout breakage.
  - **Final Resolution**: Restored original "Mixed Mode" logic (Force font size, inherit color if present). This balances readability with partial template aesthetics.
  - **Lesson**: Don't fix what isn't fully broken without understanding the template's master slide quirks. Partial inheritance is sometimes safer.

- [2026-02-13] PPT Layout Reversion (The "Mine-sweeping" Style):
  - **Request**: User demanded the "Feb 12th" version layout (Blue Sidebars/Underlines).
  - **Action**: Disabled `_use_template` logic in `ppt_builder.py` and forced `_get_layout` to select a blank slide (Index 6) to trigger manual shape drawing.
  - **Result**: Restored the code-generated visual style completely, bypassing any template placeholders.

- [2026-02-14] Zombie Build (The "Silent Failure" Incident):
  - **Symptom**: User updated code and ran build, but the resulting EXE still had old bugs.
  - **Cause**: The previous `CourseForge.exe` process was still running/hung in the background. Windows file locking prevented `pyinstaller` from overwriting it, but the error was missed or swallowed.
  - **Fix**: Always run `taskkill /F /IM CourseForge.exe` and `rm dist/CourseForge.exe` BEFORE starting a new build.
  - **Lesson**: Never trust a build command to overwrite a running binary. Kill it first.

## 🔑 Key Commands (核心口令)
- **开发环境运行 (Dev Mode)**:
  ```bash
  streamlit run app.py
  ```
  *(注：这是源码运行模式，修改代码后刷新浏览器即生效)*

- **打包发布 (Build EXE)**:
  ```bash
  # 1. 强制结束旧进程 (必做!)
  taskkill /F /IM CourseForge.exe
  
  # 2. 清理旧文件 (必做!)
  if (Test-Path dist\CourseForge.exe) { rm dist\CourseForge.exe }
  
  # 3. 执行构建
  python -m PyInstaller CourseForge.spec --clean --noconfirm
  ```
  *(注：构建完成后，新文件在 `dist/` 目录下)*

## 2026-03-03: 打通线上 LMS “最后一公里” (PPT强化、场景化试题、Excel无损多行导出)
- **依赖选型警告**：在处理客户严格格式的 Excel 模板时，必须弃用 `pandas`。`pandas` 在读写时容易丢失数据验证、复杂表头及下拉框格式，必须采用 `openpyxl` 逐单元格定点写入。
- **Excel垂直多行装填**：遇到“一题多选项占多行”的需求，要精算 `start_row` 的游标下移逻辑（`start_row += 1 + len(options)`），并保持上下文列（A/B/C/D列）的空白或继承。
- **多模态提炼兜底**：当课件 PPT 单页文本不足（<50字）但存在图片资源 (`MSO_SHAPE_TYPE.PICTURE`) 时，可以直接提取 `shape.image.blob` 转接拥有视觉能力的模型 (Cot-VL/Gemini Pro Vision) 进行兜底萃取，大幅提升少字多图页面的知识点捕捉率。
- **PPT无损强化**：使用 `python-pptx` 对原始课件做强化时，尽量不动 `shapes` 的排版，通过向 `slide.notes_slide.notes_text_frame.text` 注入结构化打点数据，实现排版零破坏的强化。

### 2026-03-04: LMS 级联强化闭环 (PPT就地强化+Excel生成) 修复
- **表现**：用户勾选了相应的任务却未能看到 "就地强化带备注的PPT" 以及 "导出的题库Excel"，且无相关产物。
- **根本原因**：`process_course_pipeline` 函数只是被定义在了 `app.py` 的尾部，**从来没有在主应用的执行流 (`if st.button("🚀 一键生成全套教学材料"...`) 中被调用过**。同时依赖的基础类库没有被严格导入，模板库也缺失。
- **解决方案**：
  1. 在 UI 核心系列后注入 `st.checkbox("启用 LMS 闭环处理")`，绑定收集进入 `options` 变量。
  2. 在 `app.py` 常规生成步骤完成后注入判定逻辑，抓取 `options.get('enable_lms')` 状态及限定 `.pptx` 扩展名。
  3. 通过 `PPTBuilder.enrich_pptx_in_place(temp_pptx, lms_pptx_path, generator)` 调用保证了原模版的保留、并抽提页面内容打入备注中。
  4. 利用生成器的结构及原 `ExcelExporter` 补充生成相关题库并直接写入 `template.xlsx`。
  5. 最末端，根据上下文产生的输出路径，在前端注入原版加强版和题库 Excel 的专属 `st.download_button` 供用户验收。
- **Anti-Pattern (避坑指南)**：不要在主 UI 流之外把代码写在文件最底部然后指望 Streamlit 魔法般地执行它。要在主运行事件中显式集成代码流！

### 2026-03-04: LMS 级联强化闭环 (PPT就地强化+Excel生成) 修复
- **表现**：用户勾选了相应的任务却未能看到 "就地强化带备注的PPT" 以及 "导出的题库Excel"，且无相关产物。
- **根本原因**：`process_course_pipeline` 函数只是被定义在了 `app.py` 的尾部，**从来没有在主应用的执行流 (`if st.button("🚀 一键生成全套教学材料"...`) 中被调用过**。同时依赖的基础类库（如 `openpyxl` 不存在、空Excel模板文件未提供）没有被严格校验。
- **解决方案**：
  1. 在 UI 核心系列后注入 `st.checkbox("启用 LMS 闭环处理")`，绑定收集进入 `options` 变量。
  2. 在 `app.py` 常规生成步骤完成后注入判定逻辑，只要开启了选项并满足是 `.pptx` 扩展名，就原地截获文件流进行强化。
  3. 执行 `PPTBuilder.enrich_pptx_in_place(temp_pptx, lms_pptx_path, generator)` 保证原 PPT 视觉排板无损保留，并将页面分析产生的 `[章节][知识点] 补充说明` 植入到原页卡的备注中（Notes_Slide）。
  4. 利用相同的 generator 分析生成结构化考点（基于 OCR 或文本），生成 JSON。
  5. 防御性创建一个空白 `static/template.xlsx` 作为初始模板，引入 `openpyxl` 包（使用 `python -m pip install openpyxl`）。并将抽取的 JSON 提供给原 `ExcelExporter`。
  6. 最末端由于增加了 `lms_pptx_path` 和 `lms_excel_path` 路径引用，我们在原结果预览下方，单独提供了「🚀 下载 LMS强化版(保留原排版及修饰)」与「📊 下载 LMS混合题库(Excel)」两个独立下载按钮供用户验收。
- **Anti-Pattern (避坑指南)**：对于 Streamlit 的脚本流应用（Top-Down Script），把函数定义在文件最末端不会自动被按键事件调用。必须要明确把调用栈注入在 `st.button` 下游。

### 2026-03-04: Google AI Studio 直连 + Antigravity 代理双模路由重构
- **表现**：用户使用 Google AI Studio API Key 通过 Antigravity 本地代理（`127.0.0.1:8045`）连接时，持续报 502 Bad Gateway 或 404 Not Found。
- **根本原因**：之前 `ai_generator.py` 的外网模式根据模型名称自动选择 SDK（Google GenAI / Anthropic / OpenAI），但 Antigravity 代理**只接受 Anthropic 协议格式**，向其发送 Gemini REST 请求会被拒绝。而直连 Google 官方 API 又必须使用 Gemini REST 格式。
- **解决方案**：彻底重构为**双模路由**：
  1. **Antigravity 代理模式**：当 `base_url` 为自定义地址时，使用 `Anthropic` SDK 透传任意模型名。
  2. **Google 直连模式**：当 `base_url` 为空或含 `googleapis.com` 时，用 `requests.post` 发送 Gemini REST 请求。
  3. **前端动态切换**：模型下拉列表根据 Base URL 自动切换可选模型。
- **Anti-Pattern**：不要试图用单一 SDK/协议兼容所有 API 网关。识别代理协议特征后精确匹配才是正解。

### 2026-03-04: f-string 中的 JSON 花括号转义崩溃
- **表现**：LMS 题库生成时崩溃，报 `Invalid format specifier ' "A. 选项一", "is_correct": false'`。
- **根本原因**：`prompts.py` 的 `get_lms_content_prompt` 使用 `f"""..."""`，其中嵌入的 JSON 示例包含未转义的 `{` `}`，Python 将其误解为格式化占位符。
- **解决方案**：将 JSON 示例中的 `{` → `{{`，`}` → `}}`。
- **Anti-Pattern**：在 f-string 中嵌入 JSON 示例时，**必须**双写花括号。

### 2026-03-04: PyInstaller 静态资源打包遗漏
- **表现**：EXE 运行时报 `Excel 模板文件丢失`。
- **根本原因**：`.spec` 的 `datas` 列表未包含 `assets` 目录；`app.py` 未使用 `sys._MEIPASS` 定位冻结后的资源路径。
- **解决方案**：`.spec` 添加 `('assets', 'assets')`，`app.py` 使用 `sys._MEIPASS` 动态寻址。
- **Anti-Pattern**：PyInstaller **不会**自动打包静态文件。每新增资源目录都必须显式声明并用 `_MEIPASS` 寻址。

### 2026-03-04: LMS 题库生成空白导出
- **表现**：outputs 目录出现与模板一模一样的空白 Excel，无任何题目数据。
- **根本原因**：`extract_json_from_response` 返回空列表，`ExcelExporter` 的 for 循环不执行，直接 `wb.save()` 等同于复制空模板。
- **解决方案**：在调用 `ExcelExporter` 前增加 `if not questions` 防御性检查，跳过导出并显示 AI 原始响应供调试。
- **Anti-Pattern**：对"读取模板→填充→导出"流程，必须验证数据源非空，否则等于无意义复制模板。

### 2026-03-04: 独立转换工具 + 场景化测试元数据增强
- **需求**：LMS 闭环一键生成时 AI 回复经常被截断（token 上限），导致 JSON 解析失败。用户需要一个独立工具，直接上传已生成的 `scenario_quiz.md` 转换为 Excel 题库。
- **方案**：
  1. 新增 `modules/quiz_converter.py`，支持 Markdown 解析（`### 题目 N` 格式）+ 截断 JSON 修复 + 双轨回退。
  2. `app.py` 底部新增独立转换区块，上传 `.md` → 预览解析 → 一键导出 Excel。
  3. `prompts.py` 的 `get_scenario_quiz_prompt` 新增 `**课程名称**`、`**章节**`、`**小节**` 元数据标签。
  4. `excel_exporter.py` 优先使用题目内嵌元数据填充 A/B/C 列。
- **Anti-Pattern**：在 f-string prompt 中新增参数后，必须确保**调用链上所有函数**都传递该参数。本次 `generate_all_materials` 遗漏了 `course_name` 参数导致 `NameError`。

### 2026-03-05: 数据血缘（Data Lineage）— PPT 标签 → Excel 章节/知识点穿透
- **表现**：生成的 Excel 题库中，B 列（章节名称）和 C 列（知识点名称）为空或与 PPT 备注中的 `[章节名][知识点名]` 标签不匹配。
- **误判**：初始怀疑 `excel_exporter.py` 硬编码或 `app.py` 传递了固定 `chapter_name` 参数。
- **真正根因**：经代码审查，`excel_exporter.py` 已用 `q.get('chapter', '')` 动态读取，`app.py` 无硬编码。问题仅出在 **Prompt 层** —— `get_lms_content_prompt` 和 `get_scenario_quiz_prompt` 未明确告知 AI 内容中存在 `[章节名][知识点名]` 格式的层级标签，AI 因此自行编造或留空。
- **解决方案**：
  1. `get_lms_content_prompt` 新增约束 #4「标签血缘」，明确标签格式并禁止编造。
  2. `get_lms_content_prompt` JSON schema 中 `chapter`/`section` 描述更新为"精准提取，禁止编造"。
  3. `get_scenario_quiz_prompt` 规则 #6 强化为完整的标签提取指令。
- **Anti-Pattern**：当 AI 输出不符合预期时，不要急于修改下游（导出器/UI），先检查上游 Prompt 是否给了足够明确的指令。**Prompt 是数据血缘链路的源头**。

### 2026-03-11: LMS 题库截断与章节匹配失效 (The "Ghost Module" Bug)
- **表现一**：PPT 超过 30 页时，LMS 题库生成在第三小节左右突然截断，只剩一道题。
  - **原因**：AI _call_ai 请求默认 `max_tokens=4000`，对超长 PPT（10题/小节的配额）会遭遇硬截断，系统自带的 Json 修复机制 `_repair_truncated_json` 只能挽回被截断前的数据。
  - **修复**：在 `app.py` 中显式传递 `max_tokens=8192` 给 `generator._call_ai`。
- **表现二**：生成的 Excel 题库和 PPT 备注中的章节/小节完全对应不上，AI 自己在盲猜生成。
  - **原因**：代码依赖了一个不存在的 `doc_extractor` 模块来读取强化后的 PPT 备注。因为 `ModuleNotFoundError` 被宽泛的 `except Exception` 捕获，程序默默执行了降级逻辑：`ppt_full_text = cleaned_content`（即上传时的无标签原始文本），导致 AI 根本没有看到 `[Chapter][Section]` 标签。
  - **修复**：彻底移除了 `doc_extractor` 的相关引用。在 `app.py` 内部手写了基于 `python-pptx` 的强制备注提取代码，只有在确信读取到 `slide.notes_slide.notes_text_frame.text` 及正文后才组装为 prompt 上下文。
- **Anti-Pattern**：**永远不要使用过于宽泛的 `except Exception:` 来静默处理非预期的环境缺失！** 这会掩盖类似于 `ModuleNotFoundError` 的致命错误，并将系统拖入不可预知的降级分支。

### 2026-03-11: 大小节配额失效问题 (The "Lazy AI vs Token Quota" Problem)
- **表现**：即便把 `max_tokens` 加大到 8192，具有几十个小节的超大 PPT 在实际跑的时候，AI 还是不肯按要求每个小节输出满 10 道题，经常严重缩水（只出 2-3 题）或者在到达 8192 限额时依然被截断。
- **本质分析**：在单次会话中要求 AI 针对几十个小节，每个都必须绞尽脑汁出 10 道题，极度违反现在生成式模型的注意力机制（Attention 稀释与偷懒倾向），也极容易触顶最大物理上限。
- **终极解决方案 (Chunking Strategy)**：将单次整体的 Prompt 调用替换为按 `[章节][小节]` 为维度的分块循环（For Loop Chunking）。
  1. 通过 Regex 在 `app.py` 中截取切割不同 `[章节]` 标签之间的内容块。
  2. 把“出 10 题”的指令按每一块的粒度分批次发送给 AI（每次只要在 4000 个 tokens 内搞定 10 题足矣）。
  3. 通过循环合并生成的 JSON 数组给下游 Excel 渲染器。
- **Lesson**：对于刚性的、与文本长度成正比的生成量要求（“每页/每节必须输出 N 个单元”），千万不要尝试用“全局发一次Prompt”来解决。**分块循环、化整为零才是克服 AI 注意力涣散和 Token 壁垒的唯一解。**
