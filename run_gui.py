#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键启动 GUI 应用
"""

import sys
import subprocess

if __name__ == '__main__':
    try:
        # 尝试启动 GUI 应用
        subprocess.run([sys.executable, 'src/gui_main.py'])
    except Exception as e:
        print(f"启动失败: {e}")
        print("\n请确保已安装所有依赖:")
        print("pip install -r requirements.txt")
