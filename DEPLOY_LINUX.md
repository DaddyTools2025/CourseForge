# CourseForge 信创/Linux 部署指南

本指南用于指导在企业信创终端（UOS/Kylin/Ubuntu 等 Linux 环境）部署 CourseForge。

## 1. 环境准备 (Prerequisites)

在运行程序前，请确保终端满足以下条件：

### 基础环境
- **操作系统**: UOS / Kylin / Ubuntu 20.04+ / CentOS 7+
- **Python**: 3.9 或更高版本
  - 验证命令: `python3 --version`
- **venv 模块**: 必须安装（部分精简版系统可能缺失）
  - 验证命令: `python3 -m venv --help`
  - 安装命令 (如缺失): `sudo apt install python3-venv` 或联系管理员

### 网络要求
- **内部大模型 API**: 需确保本机能访问 API 接口地址（如 `http://215.2.199.198...`）
- **依赖安装**:
  - **方案 A (推荐)**: 配置内网 pip 镜像源（如企业内部 PyPI 镜像）
  - **方案 B (离线)**: 使用 `pip download` 在外网下载 whl 包，拷贝至内网安装

## 2. 部署步骤 (Deployment)

### 第一步：解压程序
将程序包解压至任意目录（建议放在用户主目录，如 `/home/user/CourseForge`）。

### 第二步：一键生成启动图标
在终端中运行以下命令（仅需运行一次）：

```bash
cd /path/to/CourseForge  # 进入程序目录
bash install_shortcut.sh
```

> **提示**: 运行后，您的桌面上会出现一个 "CourseForge" 图标。

### 第三步：启动程序
1. **双击桌面图标**即可启动。
2. 程序会自动检查环境、创建虚拟环境并安装依赖（首次启动可能需要几分钟）。
3. 启动成功后，默认浏览器会自动打开应用界面。

## 3. 常见问题 (FAQ)

### Q: 双击图标无反应？
- **A**: 请右键图标 -> 允许运行 (Allow Launching)。或者尝试在终端运行 `./start.sh` 查看具体报错信息。

### Q: 依赖安装失败？
- **A**: 请检查网络配置。如果是纯内网环境，请配置 pip 镜像源：
  ```bash
  mkdir ~/.pip
  echo "[global]" > ~/.pip/pip.conf
  echo "index-url = http://your-internal-pypi-mirror/simple" >> ~/.pip/pip.conf
  echo "trusted-host = your-internal-pypi-mirror" >> ~/.pip/pip.conf
  ```

### Q: 提示 "Missing venv module"？
- **A**: 请安装 Python venv 模块：`sudo apt install python3-venv`。

## 4. 验证清单
- [ ] Python 3.9+ 已安装
- [ ] python3-venv 已安装/可用
- [ ] 内部大模型 API 网络连通
- [ ] 桌面快捷方式已生成
