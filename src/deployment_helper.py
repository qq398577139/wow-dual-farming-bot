#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布懈并脚本
"""

import subprocess
import sys
import os
from pathlib import Path

class DeploymentHelper:
    """部署辅助器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
    
    def step_1_build_exe(self):
        """步骤 1: 构建 EXE"""
        print("\n" + "="*70)
        print("步骤 1: 构建 EXE 文件")
        print("="*70)
        print("正在构建 EXE...")
        result = subprocess.run([sys.executable, 'build_exe.py'], cwd=self.project_root)
        return result.returncode == 0
    
    def step_2_create_release_files(self):
        """步骤 2: 创建发布文件"""
        print("\n" + "="*70)
        print("步骤 2: 创建发布文件")
        print("="*70)
        print("正在创建发布文件...")
        result = subprocess.run([sys.executable, 'src/version_release.py'], cwd=self.project_root)
        return result.returncode == 0
    
    def step_3_git_commit(self):
        """步骤 3: Git 提交"""
        print("\n" + "="*70)
        print("步骤 3: Git 提交")
        print("="*70)
        print("需要手动执行以下命令:")
        print("\n  # 编辑所有并转文件")
        print("  git add -A")
        print("\n  # 提交更改")
        print("  git commit -m \"release: v1.0.0 正式发布\"")
        print("\n  # 推送到 GitHub")
        print("  git push origin main")
        print("\n  # 创建标签")
        print("  git tag v1.0.0")
        print("  git push origin v1.0.0")
        return True
    
    def step_4_create_github_release(self):
        """步骤 4: 创建 GitHub Release"""
        print("\n" + "="*70)
        print("步骤 4: 创建 GitHub Release")
        print("="*70)
        print("访问以下采垧创建 Release:")
        print("\n  https://github.com/qq398577139/wow-dual-farming-bot/releases/new")
        print("\n配置信息:")
        print("  - 标签名称: v1.0.0")
        print("  - 目标分支: main")
        print("  - 发布主题: v1.0.0 正式发布")
        print("  - 描述: 查看 RELEASE_NOTES.md")
        print("  - 上传 dist/wow-farming-bot.exe")
        return True
    
    def step_5_publish_announcement(self):
        """步骤 5: 发布告示"""
        print("\n" + "="*70)
        print("步骤 5: 发布告示")
        print("="*70)
        print("你可以還6.0运作日宗常见的社交介质上发布:")
        print("\n  1. GitHub Issues")
        print("  2. GitHub Discussions")
        print("  3. QQ 群")
        print("  4. 微信粖群")
        print("  5. Reddit r/gaming")
        print("\n发布文案模板:")
        print("""
🎉 WoW 双采自动化脚本 v1.0.0 正式发布！

📄 特性：
- ✅ PyQt5 GUI 界面
- ✅ 一键 EXE 打包
- ✅ 全局快捷键
- ✅ 自动更新系统

💉 下载：
https://github.com/qq398577139/wow-dual-farming-bot/releases/v1.0.0

🃑 文档：
https://github.com/qq398577139/wow-dual-farming-bot
        """)
        return True
    
    def deploy(self):
        """完整的发布流程"""
        print("\n" + "#"*70)
        print("# WoW 双采自动化脚本 - v1.0.0 发布流程")
        print("#"*70)
        
        steps = [
            ("步骤 1", self.step_1_build_exe),
            ("步骤 2", self.step_2_create_release_files),
            ("步骤 3", self.step_3_git_commit),
            ("步骤 4", self.step_4_create_github_release),
            ("步骤 5", self.step_5_publish_announcement),
        ]
        
        for step_name, step_func in steps:
            try:
                if not step_func():
                    print(f"\n⚠ {step_name} 失败")
                    return False
            except Exception as e:
                print(f"\n❌ {step_name} 出错: {e}")
                return False
        
        print("\n" + "="*70)
        print("✅ 发布流程完成！")
        print("="*70)
        print("下一步：按照上述步骤手动执行")
        return True

def main():
    deployer = DeploymentHelper()
    deployer.deploy()

if __name__ == '__main__':
    main()
