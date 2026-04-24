# 🚀 CourseForge (铸课工坊)

> **将专业的企业业务知识，一键转化为高质量、可落地的标准化培训课程。**

CourseForge 是一个专为企业内训师、业务专家设计的 **AI 赋能教案生成系统**。它能够深度解析你上传的枯燥文档（PDF、Word、PPT），并通过内置的资深课程设计师 Prompt 架构，将晦涩难懂的业务制度一键转化为生动、专业的系统化培训材料。

---

## ✨ 核心特性 (Core Features)

### 1. 🎯 多模态课件拆解与知识重组
不仅仅是文字摘要。CourseForge 内置深度文档解析引擎：
- **无损提取**：支持解析 `PDF`、`DOCX`、`PPTX` 格式，自动过滤页眉页脚与干扰字符。
- **知识点映射**：精准识别文档层级结构，将内容映射为教学目标（基于 Bloom 认知分类法）。
- **全方位输出**：支持一键生成「视频旁白脚本」、「先导微课大纲」、「课堂互动方案」、「回岗实践计划」和「双向调研问卷」。

### 2. 🔌 LMS 系统无缝对接 (LMS Integration)
彻底解放出题人的双手，打通从学习到考核的“最后一公里”：
- **场景化通关测试**：拒绝死记硬背的客观题。基于上下文智能生成带时间、地点、人物的真实业务场景题。
- **动态出题配额**：严格遵循内部考试系统的标准要求，按知识点结构自动输出精确数量的（单选、多选、判断、填空）。
- **JSON / Excel 导出**：自动打包生成包含题干、选项、解析、章节映射的结构化数据，直接导入主流学习管理系统 (LMS)。

### 3. 🏢 动态行业场景适配 (Dynamic Industry Profile)
一处部署，多行业适用。前端内置 **“行业场景”** 快速切换选项：
- **银行业**：自动切换“国有银行资深内训师”视角，题目聚焦柜面操作、信贷合规、风险研判。
- **互联网**：自动切换“大厂敏捷教练”视角，情景偏向系统架构、产品迭代、敏捷冲刺。
- **通用企业**：聚焦跨部门协作、管理决策与标准化作业流程。

### 4. 🔒 内/外网双模安全架构 (Dual API Routing)
绝不牺牲企业数据安全：
- **外网模式**：支持调用 Google Gemini / Anthropic Claude 等强大的商业大模型，适合通用知识处理。
- **内网模式 (Enterprise Ready)**：支持纯本地网络调用，对接企业内部自建/私有化部署的大模型 API。数据不出域，满足金融级安全合规要求。

---

## 🛠️ 技术栈 (Tech Stack)

- **Frontend / UI**: `Streamlit` (快速构建数据交互 Web UI)
- **AI Integration**: `google-generativeai`, `anthropic`, `requests` (针对内网 REST)
- **Document Parsing**: `PyMuPDF` (PDF), `python-docx` (Word), `python-pptx` (PPT)
- **Data Export**: `openpyxl` (Excel 无损装填)

---

## 🚀 安装与运行 (Installation)

### 环境要求
- Python 3.9 或以上版本
- 建议使用虚拟环境（venv 或 conda）

### 本地启动步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/your-username/CourseForge.git
   cd CourseForge
   ```

2. **创建并激活虚拟环境**
   ```bash
   python -m venv venv
   
   # Windows:
   venv\\Scripts\\activate
   
   # Linux/macOS:
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行应用**
   ```bash
   streamlit run app.py
   ```
   > 运行后会自动在浏览器中打开 Web 界面。请在 UI 界面的“API 配置”页中填写你的模型接口信息。

---

## 📦 独立打包 (Build for Production)

如果你希望将系统打包为无需 Python 环境的独立执行程序 `.exe` 分发给业务部门，可以使用 `PyInstaller`：

```bash
# 清理旧的构建
# Windows
rmdir /s /q build dist
# 运行打包
python -m PyInstaller --clean --noconfirm CourseForge.spec
```
打包成功后，可在 `dist/` 目录下找到可执行程序。

*(注：Linux 信创环境的离线部署请参考 [DEPLOY_LINUX.md](DEPLOY_LINUX.md))*

---

## 🤝 参与贡献 (Contributing)
如果你对本项目有任何建议，欢迎提交 Issue 或 Pull Request！我们非常欢迎一起完善各类行业的提示词模板与导出兼容性。

## 📄 开源协议 (License)
[MIT License](LICENSE) (或替换为您选择的开源协议)
