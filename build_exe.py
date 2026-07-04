#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyInstaller 打包配置
一键生成 Windows EXE 文件
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

class Packager:
    """打包器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / 'dist'
        self.build_dir = self.project_root / 'build'
    
    def clean(self):
        """清理之前的构建"""
        print("清理旧文件...")
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        
        build_spec = self.project_root / 'wow_farming_bot.spec'
        if build_spec.exists():
            build_spec.unlink()
        
        print("✓ 清理完成")
    
    def create_spec_file(self):
        """创建 PyInstaller spec 文件"""
        spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/gui_main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('routes', 'routes'),
        ('logs', 'logs'),
    ],
    hiddenimports=[
        'PyQt5',
        'cv2',
        'numpy',
        'yaml',
        'pyautogui',
        'pynput',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='wow-farming-bot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)
'''
        spec_file = self.project_root / 'wow_farming_bot.spec'
        with open(spec_file, 'w') as f:
            f.write(spec_content)
        print("✓ Spec 文件已创建")
    
    def build_exe(self):
        """构建 EXE 文件"""
        print("正在构建 EXE 文件...")
        try:
            subprocess.run([
                sys.executable, '-m', 'PyInstaller',
                'wow_farming_bot.spec',
                '--distpath', 'dist',
                '--buildpath', 'build'
            ], check=True)
            print("✓ EXE 构建完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ 构建失败: {e}")
            return False
    
    def create_installer(self):
        """创建 Windows 安装程序"""
        print("正在创建 Windows 安装程序...")
        
        nsis_script = '''!include "MUI2.nsh"

; 基本设置
Name "WoW 双采自动化脚本"
OutFile "dist/WoW-Farming-Bot-Setup.exe"
InstallDir "$PROGRAMFILES\\WoW-Farming-Bot"

; 界面设置
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "SimpChinese"

Section "Install"
  SetOutPath "$INSTDIR"
  File /r "dist\\wow-farming-bot\\*.*"
  
  ; 创建开始菜单快捷方式
  CreateDirectory "$SMPROGRAMS\\WoW Farming Bot"
  CreateShortCut "$SMPROGRAMS\\WoW Farming Bot\\WoW Farming Bot.lnk" "$INSTDIR\\wow-farming-bot.exe"
  CreateShortCut "$DESKTOP\\WoW Farming Bot.lnk" "$INSTDIR\\wow-farming-bot.exe"
SectionEnd

Section "Uninstall"
  RMDir /r "$INSTDIR"
  RMDir /r "$SMPROGRAMS\\WoW Farming Bot"
  Delete "$DESKTOP\\WoW Farming Bot.lnk"
SectionEnd
'''
        
        nsis_file = self.project_root / 'installer.nsi'
        with open(nsis_file, 'w', encoding='utf-8') as f:
            f.write(nsis_script)
        
        print("✓ 安装程序脚本已创建")
        print("提示: 需要安装 NSIS 来编译安装程序")
        print("下载地址: https://nsis.sourceforge.io/")
    
    def package(self):
        """完整打包流程"""
        print("="*50)
        print("WoW 双采自动化脚本 - EXE 打包工具")
        print("="*50)
        
        # 1. 清理
        self.clean()
        
        # 2. 创建 spec 文件
        self.create_spec_file()
        
        # 3. 构建 EXE
        if not self.build_exe():
            return False
        
        # 4. 创建安装程序
        self.create_installer()
        
        print("\n" + "="*50)
        print("✓ 打包完成!")
        print("="*50)
        print(f"EXE 文件位置: {self.dist_dir / 'wow-farming-bot.exe'}")
        print(f"配置文件位置: {self.project_root / 'config'}")
        print("\n提示:")
        print("1. 双击 EXE 文件即可运行")
        print("2. 无需安装 Python")
        print("3. 第一次运行可能较慢(加载库)")
        return True

if __name__ == '__main__':
    packager = Packager()
    packager.package()
