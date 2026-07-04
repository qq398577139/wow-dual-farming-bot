# EXE 打包和发布

## 前置要求

```bash
pip install PyInstaller
```

## 一键构建 EXE

```bash
python build_exe.py
```

生成的 EXE 文件位置: `dist/wow-farming-bot.exe`

## 生成的文件说明

- `wow-farming-bot.exe` - 主程序（可直接运行）
- `WoW-Farming-Bot-Setup.exe` - Windows 安装程序

## 创建 Windows 安装程序（可选）

需要安装 NSIS:
1. 下载: https://nsis.sourceforge.io/
2. 安装后运行: `makensis installer.nsi`
3. 生成 `WoW-Farming-Bot-Setup.exe`

## 使用 EXE

1. 直接双击运行 EXE 文件
2. 或将 EXE 文件放在任何位置运行
3. 无需安装 Python
4. 无需依赖环境

## 文件大小

- 单个 EXE: ~150-200MB (包含所有依赖)
- 可以使用 UPX 压缩减小到 ~50-80MB

## 常见问题

### Q: EXE 文件很大
A: 这是正常的,包含了所有 Python 依赖和库

### Q: 首次运行很慢
A: 首次运行需要加载库,后续会快速启动

### Q: 能否进一步压缩
A: 可以安装 UPX 工具进一步压缩

### Q: 如何隐藏控制台窗口
A: 已在打包配置中设置 `console=False`
