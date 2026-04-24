# 🚀 CourseForge 快速入门指南

## 第一次使用？看这里！

### 步骤 1: 安装 Python

确保你的电脑已安装 **Python 3.9** 或更高版本。

**检查方法:**

```bash
python --version
# 或
python3 --version
```

如果没有安装，请访问: https://www.python.org/downloads/

### 步骤 2: 解压项目

将下载的 `courseforge.zip` 解压到任意目录，例如：

- Windows: `C:\Users\你的用户名\courseforge`
- Mac: `/Users/你的用户名/courseforge`
- Linux: `/home/你的用户名/courseforge`

### 步骤 3: 安装依赖

打开终端（Windows 用 CMD 或 PowerShell），进入项目目录：

```bash
cd courseforge

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 步骤 4: 配置 API

1. **复制配置模板:**

```bash
# Windows:
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
# Mac/Linux:
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

2. **编辑配置文件:**

用记事本或任意文本编辑器打开 `.streamlit/secrets.toml`，填入你的 API 信息：

```toml
[ai_config]
api_key = "sk-你的真实APIKey"  # 替换这里
base_url = "https://你的API地址/v1"  # 替换这里
model_name = "gemini-2.5-pro"  # 推荐使用 Pro
```

### 步骤 5: 启动应用

**方式一: 使用启动脚本（推荐）**

- Windows: 双击 `start.bat`
- Mac/Linux: 在终端运行 `./start.sh`

**方式二: 手动启动**

```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`

### 步骤 6: 开始使用

1. 上传课件（PDF/DOCX/PPTX）
2. 选择受众级别
3. 勾选需要的内容
4. 点击"一键生成"
5. 等待 2-5 分钟
6. 下载生成的文件

## 常见问题速查

### Q: pip install 很慢怎么办？

**A**: 使用国内镜像源：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: 如何获取 API Key？

**A**: 
1. 向你的 API 服务商申请（例如 Google AI Studio）
2. 或咨询企业 IT 部门获取内部 API
3. 推荐服务商: Google Gemini API / OpenAI Compatible 平台

### Q: 生成的内容质量不高？

**A**: 
- 确保使用 `gemini-2.5-pro` 而非 `flash`
- 上传的课件内容要完整、结构清晰
- 尝试调整"受众级别"重新生成
- AI 生成仅供参考，务必人工审核

### Q: 如何测试系统是否正常？

**A**: 运行测试脚本：

```bash
python test_system.py
```

### Q: 我不会用命令行怎么办？

**A**: 
1. Windows 用户可以双击 `start.bat` 自动完成大部分配置
2. 遇到问题截图并咨询技术人员
3. 或使用已配置好的企业版本

## 下一步

✅ 已成功运行？查看完整文档：`README.md`
✅ 想了解技术细节？查看：`PROJECT_OVERVIEW.md`
✅ 需要高级配置？编辑：`modules/` 下的代码文件

## 需要帮助？

- 📧 提交 Issue 到 GitHub
- 💬 咨询企业 IT 支持
- 📖 阅读完整文档

---

**祝你备课愉快！🎉**
