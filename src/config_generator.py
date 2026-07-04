#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动配置检测工具
自动检测游戏窗口、分辨率和最优参数
"""

import cv2
import numpy as np
import pyautogui
import yaml
import os
from src.logger import BotLogger
from src.utils import GameUtils

class AutoConfigGenerator:
    """自动配置生成器"""
    
    def __init__(self):
        self.logger = BotLogger('AutoConfigGenerator', 'logs/config_generator.log')
        self.utils = GameUtils(self.logger)
    
    def detect_game_window(self):
        """检测游戏窗口"""
        self.logger.info("正在检测游戏窗口...")
        
        try:
            import win32gui
            hwnd = win32gui.FindWindow(None, "World of Warcraft")
            
            if hwnd:
                rect = win32gui.GetWindowRect(hwnd)
                width = rect[2] - rect[0]
                height = rect[3] - rect[1]
                
                self.logger.info(f"检测���游戏窗口: {width}x{height}")
                return {
                    'window_title': 'World of Warcraft',
                    'resolution': {
                        'width': width,
                        'height': height
                    },
                    'position': {
                        'x': rect[0],
                        'y': rect[1]
                    }
                }
            else:
                self.logger.warning("未找到魔兽世界窗口，使用默认分辨率")
                return {
                    'window_title': 'World of Warcraft',
                    'resolution': {
                        'width': 1920,
                        'height': 1080
                    }
                }
        except Exception as e:
            self.logger.error(f"检测游戏窗口失败: {e}")
            return None
    
    def analyze_colors(self, sample_region=None):
        """分析游戏内的颜色范围"""
        self.logger.info("正在分析颜色范围...")
        
        try:
            screenshot = self.utils.screenshot(region=sample_region)
            if screenshot is None:
                return None
            
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
            
            # 分析不同颜色的范围
            colors = {}
            
            # 黄色范围（采矿点）
            lower_yellow = np.array([15, 100, 100])
            upper_yellow = np.array([35, 255, 255])
            mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
            if np.count_nonzero(mask_yellow) > 0:
                colors['mining'] = {
                    'h': [15, 35],
                    's': [100, 255],
                    'v': [100, 255]
                }
            
            # 绿色范围（草药点）
            lower_green = np.array([80, 100, 100])
            upper_green = np.array([100, 255, 255])
            mask_green = cv2.inRange(hsv, lower_green, upper_green)
            if np.count_nonzero(mask_green) > 0:
                colors['herbalism'] = {
                    'h': [80, 100],
                    's': [100, 255],
                    'v': [100, 255]
                }
            
            self.logger.info(f"检测到 {len(colors)} 种颜色范围")
            return colors
        except Exception as e:
            self.logger.error(f"分析颜色失败: {e}")
            return None
    
    def generate_config(self, output_file='config/config.auto.yaml'):
        """生成自动配置"""
        self.logger.info("正在生成配置文件...")
        
        try:
            # 检测游戏窗口
            game_config = self.detect_game_window()
            if not game_config:
                return False
            
            # 加载模板配置
            template_file = 'config/config.template.yaml'
            with open(template_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # 更新游戏配置
            config['game'] = game_config
            
            # 分析颜色范围
            colors = self.analyze_colors()
            if colors:
                if 'mining' in colors:
                    config['vision']['mining_color'] = colors['mining']
                if 'herbalism' in colors:
                    config['vision']['herbalism_color'] = colors['herbalism']
            
            # 保存配置
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
            
            self.logger.info(f"配置已保存到: {output_file}")
            return True
        except Exception as e:
            self.logger.error(f"生成配置失败: {e}")
            return False

def main():
    generator = AutoConfigGenerator()
    generator.generate_config()

if __name__ == '__main__':
    main()
