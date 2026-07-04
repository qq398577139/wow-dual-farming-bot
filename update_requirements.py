#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 requirements.txt 以支持 GUI 打包
"""

import subprocess
import sys

def update_requirements():
    """更新 requirements.txt"""
    packages = [
        'pyautogui==0.9.53',
        'opencv-python==4.8.1.78',
        'numpy==1.24.3',
        'pyyaml==6.0',
        'Pillow==10.0.0',
        'python-dotenv==1.0.0',
        'requests==2.31.0',
        'pywin32==306',
        'pynput==1.7.6',
        'PyQt5==5.15.9',
        'PyQtWebEngine==5.15.6',
        'PyInstaller==6.0.0',
        'flask==2.3.0',
        'psutil==5.9.0',
    ]
    
    with open('requirements.txt', 'w') as f:
        for package in packages:
            f.write(f"{package}\n")
    
    print("✓ requirements.txt 已更新")
    print("\n现在运行:")
    print("pip install -r requirements.txt")

if __name__ == '__main__':
    update_requirements()
