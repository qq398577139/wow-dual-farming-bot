#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路线编辑器
交互式工具用于编辑和测试采集路线
"""

import os
import json
import pyautogui
from src.logger import BotLogger

class RouteEditor:
    """路线编辑器"""
    
    def __init__(self):
        self.logger = BotLogger('RouteEditor', 'logs/route_editor.log')
        self.route = []
        self.recording = False
    
    def start_recording(self):
        """开始记录路线"""
        self.logger.info("开始记录路线，按 F6 添加点，按 F7 停止")
        self.recording = True
        self.route = []
        
        try:
            from pynput import keyboard
            
            def on_press(key):
                try:
                    if key == keyboard.Key.f6:
                        x, y = pyautogui.position()
                        self.route.append((x, y))
                        self.logger.info(f"已添加点: ({x}, {y})，总计 {len(self.route)} 个点")
                    elif key == keyboard.Key.f7:
                        self.recording = False
                        self.logger.info("停止记录")
                        return False
                except Exception as e:
                    self.logger.error(f"记录出错: {e}")
            
            with keyboard.Listener(on_press=on_press) as listener:
                listener.join()
        
        except Exception as e:
            self.logger.error(f"记录路线失败: {e}")
    
    def save_route(self, output_file='routes/custom_route.json'):
        """保存路线"""
        try:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(self.route, f, indent=2)
            self.logger.info(f"路线已保存到: {output_file}")
            return True
        except Exception as e:
            self.logger.error(f"保存路线失败: {e}")
            return False
    
    def load_route(self, input_file):
        """加载路线"""
        try:
            with open(input_file, 'r') as f:
                self.route = json.load(f)
            self.logger.info(f"已加载 {len(self.route)} 个路线点")
            return True
        except Exception as e:
            self.logger.error(f"加载路线失败: {e}")
            return False
    
    def preview_route(self):
        """预览路线"""
        if not self.route:
            self.logger.warning("没有路线数据")
            return False
        
        self.logger.info(f"预览 {len(self.route)} 个路线点")
        for i, (x, y) in enumerate(self.route):
            self.logger.info(f"点 {i+1}: ({x}, {y})")
        return True

def main():
    editor = RouteEditor()
    print("\n=== WoW 双采路线编辑器 ===")
    print("1. 记录新路线")
    print("2. 预览路线")
    print("3. 保存路线")
    print("4. 加载路线")
    
    choice = input("请选择: ").strip()
    
    if choice == '1':
        editor.start_recording()
        editor.preview_route()
        save = input("是否保存路线？(y/n): ").strip().lower()
        if save == 'y':
            output = input("输入文件名 (默认: routes/custom_route.json): ").strip()
            editor.save_route(output if output else 'routes/custom_route.json')
    elif choice == '2':
        input_file = input("输入路线文件路径: ").strip()
        editor.load_route(input_file)
        editor.preview_route()
    elif choice == '3':
        output = input("输入文件名 (默认: routes/custom_route.json): ").strip()
        editor.save_route(output if output else 'routes/custom_route.json')
    elif choice == '4':
        input_file = input("输入路线文件路径: ").strip()
        editor.load_route(input_file)

if __name__ == '__main__':
    main()
