#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第一个版本发布脚本
"""

import os
import json
from datetime import datetime
from pathlib import Path

class VersionRelease:
    """版本发布管理器"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.release_date = datetime.now().strftime("%Y-%m-%d")
        self.project_root = Path(__file__).parent.parent
    
    def create_changelog(self):
        """创建更新日志"""
        changelog = f"""
# 更新日志 (Changelog)

## [1.0.0] - {self.release_date}

### 🎬 第一个正式版本！

感谢你的支持！WoW 双采自动化脚本第一个正式版本正式发布。

### �️ 新墟特性

#### 自动化校減集
- 🤖 晾妙的采矿点检测
- 🤖 晾妙的草药点检测
- 🤖 整个区域自动遵事
- 🤖 晾妙战斗自动逃脱
- 🤖 多角色自动切换

#### GUI 界面
- 🕐 PyQt5 专业级 GUI 界面
- 🕐 实时统计信息显示
- 🕐 批收箱后台上佐
- 🕐 整个界面機輑

#### 高级功能
- 🚠 自动配置检测
- 🚠 互动路线编辑器
- 🚠 全局快捷键 (F9/F10/F11)
- 🚠 自动更新检查
- 🚠 性能监控系统
- 🚠 错误恢复機制
- 🚠 系统通知提示

#### 打包发布
- 📆 PyInstaller 一键打包
- 📆 Windows EXE 文件
- 📆 安装程序生成
- 📆 无需 Python 依赖

#### 文档
- 📚 详细中文指南
- 📚 快速开始指南
- 📚 EXE 打包指南
- 📚 应用预設值
- 📚 完整的 LICENSE

### 🛠️ 改进

- ✅ 优化编码结构
- ✅ 改進错误处理
- ✅ 增强性能监控
- ✅ 优化 GUI 响应速度
- ✅ 改進日志系统

### 🐠 已知问题

- ⚠️ 光事检测需要手动优化颜色配置
- ⚠️ GUI 在超低分辨率下会有辐附

### 🚀 安装

#### 方式 1: 下载 EXE （推荐）

1. 下载 `wow-farming-bot.exe`
2. 直接双击运行
3. 配置并启动

#### 方式 2: 下载源代码

```bash
git clone https://github.com/qq398577139/wow-dual-farming-bot.git
cd wow-dual-farming-bot
pip install -r requirements.txt
python main_gui.py
```

### 📄 文档

- [README.md](README.md) - 项目概述
- [GUIDE.md](GUIDE.md) - 详细中文指南
- [QUICKSTART.md](QUICKSTART.md) - 快速开始
- [BUILD_EXE.md](BUILD_EXE.md) - EXE 打包指南

### 📑 特別感谢

感谢以下开源项目的支持:
- OpenCV - 计算机视觉
- PyQt5 - GUI 框架
- PyAutoGUI - 鼠标键盘控制
- PyInstaller - EXE 打包

### 🌟 下一个版本

计划中的特性:
- 🇨🇳 中文 <-> 英文 分齐切换
- 👋 Discord 机器人集成
- 📊 推荐采集路线数据库
- 🚀 GPU 加速支持

### 📧 联系方式

- GitHub Issues: https://github.com/qq398577139/wow-dual-farming-bot/issues
- GitHub Discussions: https://github.com/qq398577139/wow-dual-farming-bot/discussions

### ⚠️ 免责声明

本脚本仅供学习和研究使用。

使用本脚本可能违反魔兽世界的服务条款。

使用者需自行承担所有后果。

---

**感谢你的使用！🉏**

"""
        return changelog
    
    def create_release_notes(self):
        """创建发布说明"""
        release_notes = f"""
# WoW 双采自动化脚本 v1.0.0 发布

🎉 **第一个正式版本正式发布！**

## 📦 发布事项

### 下载文件

| 文件 | 描述 | 大小 |
|--------|--------|----------|
| `wow-farming-bot.exe` | 单个可执行文件（推荐） | ~200MB |
| `wow-farming-bot-setup.exe` | Windows 安装程序 | ~150MB |
| `wow-farming-bot-source.zip` | 源代码 | ~10MB |

### ✅ 安装简为

1. **下载** `wow-farming-bot.exe`
2. **直接双击** 运行
3. **那就是它！** 无需其他程序

### 🛠️ 第一次运行

1. 程序会自动检测魔兽世界窗口
2. 会自动扣描上优化配置
3. 点击“启动”一切都会流结！

### 🌱 系统要求

- 🖥 Windows 7/8/10/11
- 🖥 4GB+ RAM
- 🖥 互联网 (第一次下载依赖)

### 🌟 主要特性

✅ **自动化校減**
- 采矿点自动检测
- 草药点自动检测
- 整个区域自动遵事
- 战斗自动逃脱

✅ **可一键 EXE 打包**
- 无需 Python 不介
- 不需安装依赖
- 直接运行

✅ **专业 GUI 界面**
- 批收箱后台上佐
- 全局快捷键
- 实时统计信息

✅ **自动更新系统**
- 自动检查新版本
- 一键更新

## 📚 文档

- **[README.md](README.md)** - 完整项目概述
- **[GUIDE.md](GUIDE.md)** - 详细中文指南
- **[QUICKSTART.md](QUICKSTART.md)** - 快速开始指南
- **[BUILD_EXE.md](BUILD_EXE.md)** - EXE 打包指南

## 🤣 常见问题

**Q: EXE 文件很大昨?**
A: 这是正常的，包含了整个 Python 运行时和所有依赖。

**Q: 需要安装 Python 吗?**
A: 不需要！EXE 文件包含了一切。

**Q: 能不能修改配置?**
A: 完全可以！所有配置都能在 GUI 中修改。

**Q: 安全吗?**
A: 本脚本仅供学习使用。使用者需自行承担拉轴拉。

## 🛠 故障排除

**问题: 找不到游戏窗口**
- 保证魔兽世界客户端已打开
- 检查窗口标题
- 较低分辨率可能有下转

**问题: 未检测到采集点**
- 运行自动配置检测
- 手动调整颜色范围

**问题: 运行缓慢**
- 降低游戏图形设置
- 关闭OBS/直播等

## 📇 更改日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解更多信息。

## 🚀 下一步

1. 下载安装 EXE
2. 阅读 [QUICKSTART.md](QUICKSTART.md)
3. 客慣了再谈初级不介
4. 提交沟阻疏开发

## 📧 帮助与重控

- 🌐 [GitHub Issues](https://github.com/qq398577139/wow-dual-farming-bot/issues)
- 💬 [GitHub Discussions](https://github.com/qq398577139/wow-dual-farming-bot/discussions)

---

**感谢你选择 WoW 双采自动化脚本！🉋**
"""
        return release_notes
    
    def create_github_release(self):
        """创建 GitHub Release 配置文件"""
        release_config = {
            "tag_name": f"v{self.version}",
            "target_commitish": "main",
            "name": f"v{self.version} 正式发布",
            "draft": False,
            "prerelease": False,
            "generate_release_notes": True
        }
        
        return release_config
    
    def create_release_files(self):
        """创建发布文件"""
        # 创建 CHANGELOG.md
        changelog_path = self.project_root / 'CHANGELOG.md'
        with open(changelog_path, 'w', encoding='utf-8') as f:
            f.write(self.create_changelog())
        print(f"✓ CHANGELOG.md 已创建")
        
        # 创建 RELEASE_NOTES.md
        release_notes_path = self.project_root / 'RELEASE_NOTES.md'
        with open(release_notes_path, 'w', encoding='utf-8') as f:
            f.write(self.create_release_notes())
        print(f"✓ RELEASE_NOTES.md 已创建")
        
        # 创建版本信息文件
        version_info = {
            "version": self.version,
            "release_date": self.release_date,
            "status": "stable",
            "build_number": "001",
            "repository": "https://github.com/qq398577139/wow-dual-farming-bot"
        }
        
        version_path = self.project_root / 'VERSION.json'
        with open(version_path, 'w', encoding='utf-8') as f:
            json.dump(version_info, f, ensure_ascii=False, indent=2)
        print(f"✓ VERSION.json 已创建")
    
    def print_release_info(self):
        """打印发布信息"""
        print("\n" + "="*70)
        print(f"WoW 双采自动化脚本 - v{self.version} 正式发布")
        print("="*70)
        print(f"\n📅 发布日期: {self.release_date}")
        print(f"\n🌟 发布文件:")
        print("  ✓ CHANGELOG.md - 更新日志")
        print("  ✓ RELEASE_NOTES.md - 发布说明")
        print("  ✓ VERSION.json - 版本信息")
        print(f"\n📖 下一步操作:")
        print("  1. 检查 CHANGELOG.md 和 RELEASE_NOTES.md")
        print("  2. 提交中云 (git push)")
        print("  3. 发表 GitHub Release")
        print(f"\n💉 GitHub Release URL:")
        print("  https://github.com/qq398577139/wow-dual-farming-bot/releases/new")
        print(f"\n📑 发布配置:")
        release_config = self.create_github_release()
        for key, value in release_config.items():
            print(f"  {key}: {value}")
        print("\n" + "="*70)

def main():
    release = VersionRelease()
    release.create_release_files()
    release.print_release_info()

if __name__ == '__main__':
    main()
