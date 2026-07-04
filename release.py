#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键发布脚本 - 第一个版本
"""

import subprocess
import sys

print("""
  ____    _       _
 / __ \  | |     | |
| |  | | | |     | |  🎲
| |  | | | |     | |  WoW 双采自动化脚本
| |  | | | |____ | |__ v1.0.0 正式发布
|_|  |_| |_____| |____|

那好，应归我们正式发布第一个版本！🊉
""")

print("\n正在执行发布流程...\n")

result = subprocess.run([sys.executable, 'src/deployment_helper.py'])
sys.exit(result.returncode)
