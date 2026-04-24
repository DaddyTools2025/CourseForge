# CourseForge 文件清单

## 📋 完整文件列表及说明

### 📱 主程序文件

| 文件名 | 说明 | 必需 |
|--------|------|------|
| `app.py` | Streamlit 主应用程序入口 | ✅ 必需 |

### 📦 核心模块 (modules/)

| 文件名 | 说明 | 必需 |
|--------|------|------|
| `__init__.py` | 模块导出配置 | ✅ 必需 |
| `prompts.py` | AI Prompt 模板库 | ✅ 必需 |
| `file_parser.py` | 文件解析器（PDF/DOCX/PPTX） | ✅ 必需 |
| `ai_generator.py` | AI 内容生成引擎 | ✅ 必需 |
| `ppt_builder.py` | PPT 构建器 | ✅ 必需 |

### ⚙️ 配置文件 (.streamlit/)

| 文件名 | 说明 | 必需 |
|--------|------|------|
| `secrets.toml` | API 配置（需自行创建） | ✅ 必需 |
| `secrets.toml.example` | 配置模板 | 📝 参考 |

### 📖 文档文件

| 文件名 | 说明 | 必需 |
|--------|------|------|
| `README.md` | 完整使用文档 | 📖 推荐阅读 |
| `QUICKSTART.md` | 快速入门指南 | 📖 新手必读 |
| `PROJECT_OVERVIEW.md` | 技术架构文档 | 📖 深入了解 |
| `FILE_MANIFEST.md` | 本文件清单 | 📋 参考 |

### 🔧 配置与脚本

| 文件名 | 说明 | 必需 |
|--------|------|------|
| `requirements.txt` | Python 依赖清单 | ✅ 必需 |
| `start.sh` | Linux/Mac 启动脚本 | 🚀 推荐使用 |
| `start.bat` | Windows 启动脚本 | 🚀 推荐使用 |
| `test_system.py` | 系统测试脚本 | 🧪 测试用 |
| `.gitignore` | Git 忽略规则 | 🔒 可选 |

### 📂 目录说明

| 目录名 | 说明 | 自动创建 |
|--------|------|----------|
| `outputs/` | 生成文件输出目录 | ✅ 运行时创建 |
| `venv/` | Python 虚拟环境 | ✅ 安装时创建 |

## 🎯 核心文件依赖关系

```
app.py
├── modules/__init__.py
├── modules/file_parser.py
├── modules/ai_generator.py
│   └── modules/prompts.py
└── modules/ppt_builder.py

.streamlit/secrets.toml (必需配置)
```

## 📏 文件大小（约）

| 文件 | 大小 |
|------|------|
| `app.py` | ~8 KB |
| `modules/prompts.py` | ~12 KB |
| `modules/file_parser.py` | ~5 KB |
| `modules/ai_generator.py` | ~6 KB |
| `modules/ppt_builder.py` | ~7 KB |
| `README.md` | ~10 KB |
| **总计（不含依赖）** | **~50 KB** |

## ✅ 安装检查清单

### 必需完成

- [ ] Python 3.9+ 已安装
- [ ] 依赖包已安装 (`pip install -r requirements.txt`)
- [ ] 配置文件已创建 (`.streamlit/secrets.toml`)
- [ ] API Key 已填写

### 可选完成

- [ ] 虚拟环境已创建
- [ ] 启动脚本可执行权限已设置（Mac/Linux）
- [ ] 系统测试已通过 (`python test_system.py`)

## 🔄 版本历史

### v1.0 (2024)

**包含文件:**
- ✅ 所有核心模块
- ✅ Streamlit 界面
- ✅ 完整文档
- ✅ 测试脚本

**核心功能:**
- ✅ 多格式课件解析
- ✅ 6 类教学材料生成
- ✅ PPT 自动构建
- ✅ 白标输出

## 📮 文件修改建议

### 可以自定义

- ✅ `modules/prompts.py` - 调整 Prompt 模板
- ✅ `modules/ppt_builder.py` - 修改 PPT 样式
- ✅ `app.py` - 调整界面布局

### 不建议修改

- ⚠️  `modules/file_parser.py` - 除非了解文件解析原理
- ⚠️  `modules/ai_generator.py` - 除非了解 API 调用机制

### 禁止修改

- ❌ `requirements.txt` - 可能导致依赖冲突
- ❌ `.streamlit/secrets.toml` - 仅编辑配置值，不改结构

## 💾 备份建议

**重要文件（建议备份）:**

1. `.streamlit/secrets.toml` - API 配置
2. `modules/prompts.py` - 自定义 Prompt
3. `outputs/` - 生成的历史文件

**恢复方法:**

如果误删除文件，重新下载项目压缩包即可恢复。
配置文件需要手动重建。

---

**CourseForge v1.0** - 完整文件清单 ✅
