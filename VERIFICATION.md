# ✅ CourseForge v2.0 快速验证指南

## 验证清单

### 步骤 1: 检查文件完整性

运行以下命令查看所有文件：

**Windows (PowerShell):**
```powershell
Get-ChildItem -Recurse -File | Select-Object FullName
```

**Mac/Linux:**
```bash
find . -type f | sort
```

**应包含的文件（19个）:**
```
./app.py
./modules/__init__.py
./modules/ai_generator.py
./modules/config_manager.py
./modules/file_parser.py
./modules/ppt_builder.py
./modules/prompts.py
./requirements.txt
./start.bat
./start.sh
./test_system.py
./.gitignore
./.streamlit/secrets.toml.example
./README.md
./QUICKSTART.md
./V2.0_UPGRADE.md
./PROJECT_OVERVIEW.md
./FILE_MANIFEST.md
./DELIVERY_NOTES.md
```

### 步骤 2: 测试启动脚本

**Windows:**
```
双击 start.bat
```

**Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**预期结果:**
1. 自动检查 Python 版本 ✅
2. 自动创建虚拟环境 ✅
3. 自动安装依赖包 ✅
4. 自动启动应用 ✅
5. 浏览器打开 http://localhost:8501 ✅

### 步骤 3: 验证配置界面

**首次启动应显示:**
- ⚙️ API 配置页面
- 表单包含：
  - API Key 输入框
  - Base URL 输入框
  - 模型选择下拉菜单
  - 自定义 Prompt 选项
  - 测试连接按钮
  - 保存配置按钮

### 步骤 4: 测试 API 连接（可选）

如果你有可用的 API：

1. 填写 API Key
2. 填写 Base URL
3. 点击"测试连接"
4. 应该看到：✅ API 连接成功！

### 步骤 5: 验证主界面

配置完成后应自动进入主界面，包含：

**侧边栏:**
- 当前模型显示
- 修改配置按钮
- 删除配置按钮
- 受众级别选择
- 生成内容勾选框
- 使用说明

**主内容区:**
- 上传课件区域
- 课程信息输入
- 一键生成按钮

### 步骤 6: 验证系统 Prompt

检查 `modules/ai_generator.py` 应包含：

```python
PROFESSIONAL_SYSTEM_PROMPT = """# Role
你是一位拥有15年经验的国有银行资深课程设计师，精通ADDIE教学模型和Bloom认知分类法。

# Constraints (严格执行)
1. **White Label Only**: 输出的所有内容（脚本、PPT大纲、问卷）必须是通用的、中立的...
```

---

## 常见验证问题

### 问题 1: 启动脚本无法运行

**检查:**
- Python 是否已安装（`python --version`）
- Python 版本 >= 3.9
- 是否有网络连接（用于下载依赖）

### 问题 2: 依赖安装失败

**解决:**
```bash
# 手动安装
pip install -r requirements.txt

# 或使用镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 3: 配置界面不显示

**检查:**
- 配置文件是否存在：`~/.courseforge/courseforge_config.json`
- 如果存在，尝试删除后重启

### 问题 4: API 测试连接失败

**这是正常的！** 因为需要真实的 API Key。
只要界面显示正常，就说明功能工作正常。

---

## 验证通过标准

✅ **基础验证:**
- [ ] 所有 19 个文件存在
- [ ] 启动脚本可以运行
- [ ] 应用成功启动
- [ ] 配置界面正常显示

✅ **功能验证:**
- [ ] 可以填写配置信息
- [ ] 可以保存配置
- [ ] 可以进入主界面
- [ ] 可以上传文件（界面功能）

✅ **代码验证:**
- [ ] `modules/ai_generator.py` 包含专业系统 Prompt
- [ ] `modules/config_manager.py` 存在
- [ ] `app.py` 包含配置界面代码

---

## 快速测试脚本

运行系统测试脚本：

```bash
python test_system.py
```

**预期输出:**
```
==================================================
CourseForge 系统测试
==================================================

测试 1: 检查依赖包...
  ✓ Streamlit
  ✓ OpenAI Client
  ✓ python-pptx
  ✓ PyPDF2
  ✓ python-docx
✅ 所有依赖包安装正确

测试 2: 检查自定义模块...
  ✓ FileParser
  ✓ AIGenerator
  ✓ PPTBuilder
  ✓ PromptTemplates
  ✓ ConfigManager
✅ 所有模块加载成功

... (其他测试)

通过: 4/4
🎉 所有测试通过！
```

---

## 下一步

验证通过后，你可以：

1. **阅读文档**
   - README.md - 完整使用手册
   - QUICKSTART.md - 快速入门
   - V2.0_UPGRADE.md - 新功能说明

2. **配置 API**
   - 获取 API Key
   - 在配置界面填写
   - 测试连接

3. **开始使用**
   - 上传课件
   - 生成教学材料

---

**验证完成！CourseForge v2.0 已就绪！** ✅
