#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能监控系统
实时监控和优化脚本性能
"""

import time
import psutil
import os
from src.logger import BotLogger

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.logger = BotLogger('PerformanceMonitor', 'logs/performance.log')
        self.stats = {
            'start_time': time.time(),
            'frame_count': 0,
            'total_runtime': 0,
            'cpu_usage': [],
            'memory_usage': [],
        }
    
    def get_cpu_usage(self):
        """获取CPU使用率"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.stats['cpu_usage'].append(cpu_percent)
            return cpu_percent
        except Exception as e:
            self.logger.error(f"获取CPU使用率失败: {e}")
            return 0
    
    def get_memory_usage(self):
        """获取内存使用情况"""
        try:
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            memory_percent = process.memory_percent()
            self.stats['memory_usage'].append(memory_percent)
            return {
                'rss': memory_info.rss / 1024 / 1024,  # MB
                'vms': memory_info.vms / 1024 / 1024,  # MB
                'percent': memory_percent
            }
        except Exception as e:
            self.logger.error(f"获取内存使用情况失败: {e}")
            return None
    
    def log_frame(self):
        """记录一帧"""
        self.stats['frame_count'] += 1
        self.stats['total_runtime'] = time.time() - self.stats['start_time']
    
    def get_fps(self):
        """获取帧率"""
        if self.stats['total_runtime'] > 0:
            return self.stats['frame_count'] / self.stats['total_runtime']
        return 0
    
    def get_average_cpu(self):
        """获取平均CPU使用率"""
        if self.stats['cpu_usage']:
            return sum(self.stats['cpu_usage']) / len(self.stats['cpu_usage'])
        return 0
    
    def get_average_memory(self):
        """获取平均内存使用率"""
        if self.stats['memory_usage']:
            return sum(self.stats['memory_usage']) / len(self.stats['memory_usage'])
        return 0
    
    def report(self):
        """输出性能报告"""
        cpu_avg = self.get_average_cpu()
        mem_avg = self.get_average_memory()
        fps = self.get_fps()
        
        report = f"""
        === 性能报告 ===
        运行时间: {self.stats['total_runtime']:.1f}秒
        总帧数: {self.stats['frame_count']}
        平均FPS: {fps:.1f}
        平均CPU: {cpu_avg:.1f}%
        平均内存: {mem_avg:.1f}%
        """
        
        self.logger.info(report)
        return report
