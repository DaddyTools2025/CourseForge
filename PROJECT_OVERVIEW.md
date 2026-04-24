# CourseForge 项目总览

## 📁 项目结构

```
courseforge/
│
├── 📱 app.py                          # Streamlit 主应用（入口文件）
│
├── 📦 modules/                        # 核心功能模块
│   ├── __init__.py                    # 模块导出
│   ├── prompts.py                     # Prompt 模板库
│   ├── file_parser.py                 # 文件解析器（PDF/DOCX/PPTX）
│   ├── ai_generator.py                # AI 内容生成引擎
│   └── ppt_builder.py                 # PPT 构建器
│
├── ⚙️ .streamlit/                     # Streamlit 配置
│   ├── secrets.toml                   # API 配置（需自行创建）
│   └── secrets.toml.example           # 配置模板
│
├── 📤 outputs/                        # 生成文件输出目录（自动创建）
│
├── 📋 requirements.txt                # Python 依赖清单
├── 📖 README.md                       # 完整使用文档
├── 📝 PROJECT_OVERVIEW.md             # 本文件
├── 🧪 test_system.py                  # 系统测试脚本
├── 🚀 start.sh                        # Linux/Mac 启动脚本
├── 🚀 start.bat                       # Windows 启动脚本
└── 🔒 .gitignore                      # Git 忽略规则
```

## 🔄 工作流程

```
用户上传课件 (PDF/DOCX/PPTX)
        ↓
[FileParser] 提取文本内容
        ↓
[AIGenerator] 调用 Gemini API
        ↓
生成 6 类教学材料:
  ├─ 核心内容 (Markdown)
  ├─ 视频脚本 (Markdown)
  ├─ 课堂互动 (Markdown)
  ├─ 回岗实践 (Markdown)
  ├─ 调研问卷 (Markdown)
  └─ PPT 大纲 (JSON)
        ↓
[PPTBuilder] 将 JSON 转为 PPTX
        ↓
保存到 outputs/ 目录并展示
```

## 🛠️ 技术细节

### 1. 文件解析 (file_parser.py)

**支持格式:**
- PDF: 使用 PyPDF2 逐页提取文本
- DOCX: 使用 python-docx 提取段落和表格
- PPTX: 使用 python-pptx 提取幻灯片内容

**核心方法:**
- `parse_pdf()`: PDF 解析
- `parse_docx()`: Word 文档解析
- `parse_pptx()`: PPT 解析
- `clean_content()`: 去除 LOGO、公司名等敏感信息

### 2. AI 生成 (ai_generator.py)

**API 配置:**
- 使用 OpenAI Compatible Client
- 支持任何兼容 OpenAI API 的服务（如 Gemini）
- 配置在 `.streamlit/secrets.toml`

**生成策略:**
- 不同任务使用不同的 `temperature`:
  - 提取内容: 0.3（准确性优先）
  - 问卷设计: 0.5（规范性）
  - 视频脚本: 0.8（创意性）
  
**核心方法:**
- `extract_core_content()`: 提取核心知识点
- `generate_video_script()`: 生成视频脚本
- `generate_interactions()`: 设计互动方案
- `generate_action_plan()`: 制定实践计划
- `generate_surveys()`: 设计问卷
- `generate_ppt_outline()`: 生成 PPT 大纲

### 3. PPT 构建 (ppt_builder.py)

**设计原则:**
- 极简商务风格
- 无 LOGO、无装饰元素
- 配色方案可自定义

**幻灯片类型:**
- `title`: 标题页
- `section`: 章节分隔页
- `content`: 内容页（带要点列表）
- `end`: 结束页

**核心方法:**
- `build_from_json()`: 从 JSON 大纲构建 PPT
- `_add_title_slide()`: 添加标题页
- `_add_section_slide()`: 添加章节页
- `_add_content_slide()`: 添加内容页
- `_add_end_slide()`: 添加结束页

### 4. Prompt 模板 (prompts.py)

**模板设计原则:**
- 明确任务目标
- 提供输出格式示例
- 强调去除机构信息
- 适配受众级别

**所有模板:**
- `get_content_extraction_prompt()`: 内容提取
- `get_video_script_prompt()`: 视频脚本
- `get_interaction_prompt()`: 互动设计
- `get_action_plan_prompt()`: 实践计划
- `get_survey_prompt()`: 问卷设计
- `get_ppt_outline_prompt()`: PPT 大纲

## 🔐 安全与隐私

### 数据流向

```
本地文件
   ↓
[Streamlit Server] 
   ↓ (仅文本内容)
[AI API] (Gemini)
   ↓ (生成结果)
[Streamlit Server]
   ↓
本地保存
```

### 隐私保护措施

1. **文件不上传到云端**: 文件仅在内存中处理
2. **API 调用最小化**: 仅发送提取的文本内容
3. **自动清洗敏感信息**: `clean_content()` 过滤公司名、LOGO 等
4. **本地配置管理**: API Key 存储在本地 `secrets.toml`

### 推荐部署方式

- **最安全**: 企业内网 + 自建 AI 服务
- **次选**: 本地 + 可信 API 服务商
- **避免**: 公有云部署（除非有严格的安全审计）

## 📊 性能指标

### 处理能力

| 指标 | 数值 |
|------|------|
| 支持文件大小 | < 10MB（推荐）|
| 单次生成时间 | 2-5 分钟 |
| 并发支持 | 取决于 API 限制 |
| PPT 生成速度 | < 5 秒 |

### AI Token 消耗（估算）

| 任务 | Input Tokens | Output Tokens |
|------|-------------|---------------|
| 提取核心内容 | ~2,000 | ~1,000 |
| 视频脚本 | ~1,500 | ~2,000 |
| 课堂互动 | ~1,500 | ~1,500 |
| 回岗实践 | ~1,500 | ~1,500 |
| 调研问卷 | ~1,500 | ~1,500 |
| PPT 大纲 | ~1,500 | ~2,000 |
| **总计** | **~10,000** | **~10,000** |

💡 **成本控制建议**: 使用 Gemini Flash 可降低 80% 成本（质量略降）

## 🚧 已知限制

### 文件解析

- ❌ 扫描版 PDF 无法提取文字
- ⚠️  复杂排版的 PPT 可能遗漏部分内容
- ⚠️  表格内容提取质量依赖原文件结构

### AI 生成

- ⚠️  生成内容需人工审核
- ⚠️  可能出现幻觉（虚构信息）
- ⚠️  风格一致性需多次调整

### PPT 生成

- ❌ 不支持图片、图表自动生成
- ❌ 不支持动画效果
- ⚠️  样式较为简单（需手动美化）

## 🔮 未来规划

### v1.1 计划

- [ ] 支持 Markdown 文件直接导入
- [ ] 增加课件模板库（通用主题）
- [ ] 支持批量处理（多文件）
- [ ] 优化 PPT 样式（增加预设主题）

### v2.0 愿景

- [ ] 协作功能（多人编辑）
- [ ] 版本管理
- [ ] 在线编辑器（所见即所得）
- [ ] 知识库集成（课件检索）

## 🤝 贡献方式

欢迎提交 Issue 和 Pull Request！

**优先领域:**
1. 文件解析准确性提升
2. Prompt 模板优化
3. PPT 样式美化
4. 新功能建议

## 📞 联系方式

- **问题反馈**: 提交 GitHub Issue
- **功能建议**: 提交 Feature Request
- **安全漏洞**: 私密邮件联系

---

**CourseForge v1.0** - 让备课更高效 🚀
