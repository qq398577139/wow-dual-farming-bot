#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异常处理和恢复系统
"""

import time
from src.logger import BotLogger

class ErrorRecovery:
    """错误恢复系统"""
    
    def __init__(self, logger):
        self.logger = logger
        self.error_count = 0
        self.max_errors = 10
        self.recovery_strategies = {
            'screenshot_failed': self._recovery_screenshot,
            'no_nodes_found': self._recovery_no_nodes,
            'in_combat': self._recovery_combat,
            'stuck': self._recovery_stuck,
        }
    
    def handle_error(self, error_type, utils=None):
        """处理错误"""
        self.error_count += 1
        self.logger.warning(f"错误 #{self.error_count}: {error_type}")
        
        if self.error_count > self.max_errors:
            self.logger.critical(f"错误次数超过最大限制 {self.max_errors}")
            return False
        
        if error_type in self.recovery_strategies:
            strategy = self.recovery_strategies[error_type]
            return strategy(utils)
        
        return True
    
    def _recovery_screenshot(self, utils):
        """截图失败恢复"""
        self.logger.info("尝试恢复截图...")
        time.sleep(1)
        return True
    
    def _recovery_no_nodes(self, utils):
        """未找到采集点恢复"""
        self.logger.info("未找到采集点，移动位置后重试")
        if utils:
            utils.press_key('w')
            time.sleep(0.5)
        return True
    
    def _recovery_combat(self, utils):
        """战斗中恢复"""
        self.logger.warning("处于战斗状态，等待...")
        time.sleep(3)
        return True
    
    def _recovery_stuck(self, utils):
        """卡住恢复"""
        self.logger.warning("可能卡住，尝试重新启动")
        if utils:
            utils.press_key('escape')
            time.sleep(1)
        return True
    
    def reset_error_count(self):
        """重置错误计数"""
        self.error_count = 0
