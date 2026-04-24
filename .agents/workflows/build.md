---
description: CourseForge 打包集成 - 编译 EXE 并验证产物
---

# CourseForge 打包集成 (/build)

> ⚡ **此任务为机械性操作，建议切换到低成本模型执行（如 gemini-flash）。**

## 前置条件
- 所有代码修改已完成并保存
- 当前位于 `c:\Users\lucien\Desktop\CourseForge` 工作目录

## 执行步骤

### 1. 终止旧进程
// turbo
```powershell
taskkill /f /im CourseForge.exe
```
如果返回"没有找到进程"属正常情况，继续下一步。

### 2. 清理旧产物
// turbo
```powershell
if (Test-Path dist\CourseForge.exe) { Remove-Item dist\CourseForge.exe -Force }
```

### 3. 执行 PyInstaller 构建
// turbo
```powershell
python -m PyInstaller --clean --noconfirm CourseForge.spec
```
等待构建完成（约 1-2 分钟）。

### 4. 验证构建产物
// turbo
```powershell
Get-Item dist\CourseForge.exe | Select-Object Name, @{N='SizeMB';E={[math]::Round($_.Length/1MB,1)}}, LastWriteTime
```
检查:
- 文件存在
- 大小合理（通常 >50MB）
- 修改时间为当前时间

### 5. 通知用户
构建完成后，通知用户：
- ✅ 编译成功
- 📦 文件位置：`dist/CourseForge.exe`
- 📏 文件大小
- ⏰ 编译时间

## 常见问题

### PermissionError: [WinError 5]
**原因**: CourseForge.exe 仍在运行
**解决**: 再次执行 `taskkill /f /im CourseForge.exe`，如果仍失败，通知用户手动关闭程序

### Excel 锁文件 (~$*.xlsx)
**原因**: Excel 临时锁文件阻止资源打包
**解决**: `CourseForge.spec` 中应使用显式文件引用而非目录引用
当前配置：`('assets/导入题库模板.xlsx', 'assets')` ← 正确，可避免锁文件干扰

### 假构建（修改时间不对）
**原因**: 进程未完全终止，旧文件被锁定
**解决**: 必须先删除旧文件再构建
