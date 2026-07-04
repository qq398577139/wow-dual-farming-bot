#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单元测试
"""

import unittest
from src.logger import BotLogger
from src.utils import GameUtils
from src.navigation import Navigation
from src.character import CharacterManager

class TestGameUtils(unittest.TestCase):
    """测试游戏工具"""
    
    def setUp(self):
        self.logger = BotLogger('TestGameUtils', 'logs/test.log')
        self.utils = GameUtils(self.logger)
    
    def test_get_mouse_position(self):
        """测试获取鼠标位置"""
        pos = self.utils.get_mouse_position()
        self.assertIsInstance(pos, tuple)
        self.assertEqual(len(pos), 2)

class TestNavigation(unittest.TestCase):
    """测试导航系统"""
    
    def setUp(self):
        self.logger = BotLogger('TestNavigation', 'logs/test.log')
        self.config = {'routes': {}}
        self.navigation = Navigation(self.logger, self.config)
    
    def test_calculate_distance(self):
        """测试距离计算"""
        distance = self.navigation.calculate_distance((0, 0), (3, 4))
        self.assertEqual(distance, 5)
    
    def test_set_waypoints(self):
        """测试设置路线点"""
        waypoints = [(0, 0), (100, 100), (200, 200)]
        self.navigation.set_waypoints(waypoints)
        self.assertEqual(len(self.navigation.waypoints), 3)

class TestCharacterManager(unittest.TestCase):
    """测试角色管理器"""
    
    def setUp(self):
        self.logger = BotLogger('TestCharacterManager', 'logs/test.log')
        self.config = {
            'characters': {
                'char1': {'name': '主号', 'enabled': True},
                'char2': {'name': '副号', 'enabled': False}
            }
        }
        self.manager = CharacterManager(self.logger, self.config)
    
    def test_get_enabled_characters(self):
        """测试获取启用的角色"""
        enabled = self.manager.get_enabled_characters()
        self.assertEqual(len(enabled), 1)
        self.assertIn('char1', enabled)

if __name__ == '__main__':
    unittest.main()
