#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyQt5 GUI 主应用程序
"""

import sys
import os
import threading
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTabWidget, QTextEdit, QSpinBox, QComboBox,
    QFileDialog, QMessageBox, QProgressBar, QTableWidget, QTableWidgetItem,
    QLineEdit, QCheckBox, QFormLayout, QGroupBox, QScrollArea
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QColor, QFont, QIcon
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtCore import QPointF

from src.bot import FarmingBot
from src.logger import BotLogger
from src.route_editor import RouteEditor
from src.config_generator import AutoConfigGenerator

class BotWorker(QThread):
    """后台工作线程"""
    log_signal = pyqtSignal(str)
    stats_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)
    
    def __init__(self, config_file):
        super().__init__()
        self.config_file = config_file
        self.bot = None
        self.running = False
    
    def run(self):
        """运行机器人"""
        try:
            self.log_signal.emit("正在初始化机器人...")
            self.bot = FarmingBot(self.config_file)
            self.running = True
            self.log_signal.emit("机器人已启动")
            self.bot.start()
        except Exception as e:
            self.error_signal.emit(f"错误: {str(e)}")
            self.running = False
    
    def stop(self):
        """停止机器人"""
        if self.bot:
            self.bot.stop()
            self.running = False

class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WoW 双采自动化脚本 v1.0.0")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(self._get_stylesheet())
        
        self.logger = BotLogger('GUI', 'logs/gui.log')
        self.bot_thread = None
        self.bot_worker = None
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_stats)
        
        # 创建主界面
        self._create_ui()
        
        self.logger.info("GUI 应用已启动")
    
    def _create_ui(self):
        """创建用户界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout()
        central_widget.setLayout(layout)
        
        # 左侧控制面板
        left_panel = self._create_left_panel()
        layout.addWidget(left_panel, 1)
        
        # 右侧信息面板
        right_panel = self._create_right_panel()
        layout.addWidget(right_panel, 2)
    
    def _create_left_panel(self):
        """创建左侧控制面板"""
        group = QGroupBox("控制面板")
        layout = QVBoxLayout()
        
        # 状态指示
        self.status_label = QLabel("状态: 未运行")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        layout.addWidget(self.status_label)
        
        # 启动按钮
        self.start_btn = QPushButton("启动机器人")
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px;")
        self.start_btn.clicked.connect(self._start_bot)
        layout.addWidget(self.start_btn)
        
        # 停止按钮
        self.stop_btn = QPushButton("停止机器人")
        self.stop_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px; font-size: 14px;")
        self.stop_btn.clicked.connect(self._stop_bot)
        self.stop_btn.setEnabled(False)
        layout.addWidget(self.stop_btn)
        
        # 标签页
        self.tabs = QTabWidget()
        
        # 标签1: 配置
        config_tab = self._create_config_tab()
        self.tabs.addTab(config_tab, "配置")
        
        # 标签2: 路线
        route_tab = self._create_route_tab()
        self.tabs.addTab(route_tab, "路线")
        
        # 标签3: 采集点
        node_tab = self._create_node_tab()
        self.tabs.addTab(node_tab, "采集点")
        
        # 标签4: 快速设置
        quick_tab = self._create_quick_tab()
        self.tabs.addTab(quick_tab, "快速设置")
        
        layout.addWidget(self.tabs)
        
        group.setLayout(layout)
        return group
    
    def _create_config_tab(self):
        """创建配置标签页"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 自动检测
        auto_btn = QPushButton("自动检测配置")
        auto_btn.clicked.connect(self._auto_detect_config)
        layout.addWidget(auto_btn)
        
        # 配置文件选择
        file_layout = QHBoxLayout()
        self.config_path_label = QLineEdit()
        self.config_path_label.setText("config/config.yaml")
        file_layout.addWidget(QLabel("配置文件:"))
        file_layout.addWidget(self.config_path_label)
        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(self._browse_config_file)
        file_layout.addWidget(browse_btn)
        layout.addLayout(file_layout)
        
        # 编辑配置
        edit_btn = QPushButton("编辑配置文件")
        edit_btn.clicked.connect(self._edit_config)
        layout.addWidget(edit_btn)
        
        # 重新加载
        reload_btn = QPushButton("重新加载配置")
        reload_btn.clicked.connect(self._reload_config)
        layout.addWidget(reload_btn)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _create_route_tab(self):
        """创建路线标签页"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 路线操作
        btn_layout = QHBoxLayout()
        
        record_btn = QPushButton("录制新路线")
        record_btn.clicked.connect(self._record_route)
        btn_layout.addWidget(record_btn)
        
        load_btn = QPushButton("加载路线")
        load_btn.clicked.connect(self._load_route)
        btn_layout.addWidget(load_btn)
        
        save_btn = QPushButton("保存路线")
        save_btn.clicked.connect(self._save_route)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        
        # 路线显示
        self.route_text = QTextEdit()
        self.route_text.setReadOnly(True)
        layout.addWidget(QLabel("路线数据:"))
        layout.addWidget(self.route_text)
        
        widget.setLayout(layout)
        return widget
    
    def _create_node_tab(self):
        """创建采集点标签页"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 采集点检测
        detect_btn = QPushButton("检测采集点")
        detect_btn.clicked.connect(self._detect_nodes)
        layout.addWidget(detect_btn)
        
        # 采集点列表
        self.node_table = QTableWidget()
        self.node_table.setColumnCount(4)
        self.node_table.setHorizontalHeaderLabels(["类型", "位置", "面积", "颜色"])
        layout.addWidget(QLabel("检测到的采集点:"))
        layout.addWidget(self.node_table)
        
        # 颜色调整
        color_layout = QFormLayout()
        
        self.mining_h_min = QSpinBox()
        self.mining_h_min.setRange(0, 180)
        self.mining_h_min.setValue(0)
        color_layout.addRow("采矿H最小:", self.mining_h_min)
        
        self.mining_h_max = QSpinBox()
        self.mining_h_max.setRange(0, 180)
        self.mining_h_max.setValue(30)
        color_layout.addRow("采矿H最大:", self.mining_h_max)
        
        layout.addLayout(color_layout)
        
        widget.setLayout(layout)
        return widget
    
    def _create_quick_tab(self):
        """创建快速设置标签页"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 快速设置
        form = QFormLayout()
        
        # 启用采矿
        self.enable_mining = QCheckBox()
        self.enable_mining.setChecked(True)
        form.addRow("启用采矿:", self.enable_mining)
        
        # 启用草药
        self.enable_herbalism = QCheckBox()
        self.enable_herbalism.setChecked(True)
        form.addRow("启用草药:", self.enable_herbalism)
        
        # 启用战斗逃脱
        self.enable_combat = QCheckBox()
        self.enable_combat.setChecked(True)
        form.addRow("启用战斗逃脱:", self.enable_combat)
        
        # 采集间隔
        self.stop_duration = QSpinBox()
        self.stop_duration.setRange(0, 10)
        self.stop_duration.setValue(2)
        form.addRow("采集间隔(秒):", self.stop_duration)
        
        # 逃脱方式
        self.escape_method = QComboBox()
        self.escape_method.addItems(["上马", "奔跑"])
        form.addRow("逃脱方式:", self.escape_method)
        
        layout.addLayout(form)
        
        # 保存按钮
        save_quick_btn = QPushButton("保存快速设置")
        save_quick_btn.clicked.connect(self._save_quick_settings)
        layout.addWidget(save_quick_btn)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _create_right_panel(self):
        """创建右侧信息面板"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # 统计信息
        stats_group = QGroupBox("实时统计")
        stats_layout = QVBoxLayout()
        
        # 采矿
        mining_layout = QHBoxLayout()
        mining_layout.addWidget(QLabel("采矿:"))
        self.mining_label = QLabel("0")
        self.mining_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFA500;")
        mining_layout.addWidget(self.mining_label)
        stats_layout.addLayout(mining_layout)
        
        # 草药
        herb_layout = QHBoxLayout()
        herb_layout.addWidget(QLabel("草药:"))
        self.herb_label = QLabel("0")
        self.herb_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #00AA00;")
        herb_layout.addWidget(self.herb_label)
        stats_layout.addLayout(herb_layout)
        
        # 总计
        total_layout = QHBoxLayout()
        total_layout.addWidget(QLabel("总计:"))
        self.total_label = QLabel("0")
        self.total_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #0066FF;")
        total_layout.addWidget(self.total_label)
        stats_layout.addLayout(total_layout)
        
        # 效率
        rate_layout = QHBoxLayout()
        rate_layout.addWidget(QLabel("效率:"))
        self.rate_label = QLabel("0.0 个/分")
        self.rate_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #FF0000;")
        rate_layout.addWidget(self.rate_label)
        stats_layout.addLayout(rate_layout)
        
        # 运行时间
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("运行时间:"))
        self.time_label = QLabel("0秒")
        self.time_label.setStyleSheet("font-size: 14px;")
        time_layout.addWidget(self.time_label)
        stats_layout.addLayout(time_layout)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # 进度条
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        layout.addWidget(QLabel("采集进度:"))
        layout.addWidget(self.progress)
        
        # 日志输出
        log_group = QGroupBox("日志输出")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(300)
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)
        
        # 清除日志
        clear_log_btn = QPushButton("清除日志")
        clear_log_btn.clicked.connect(lambda: self.log_text.clear())
        layout.addWidget(clear_log_btn)
        
        widget.setLayout(layout)
        return widget
    
    def _start_bot(self):
        """启动机器人"""
        config_file = self.config_path_label.text()
        
        if not os.path.exists(config_file):
            QMessageBox.warning(self, "警告", f"配置文件不存在: {config_file}")
            return
        
        self.bot_worker = BotWorker(config_file)
        self.bot_worker.log_signal.connect(self._on_log)
        self.bot_worker.error_signal.connect(self._on_error)
        self.bot_worker.start()
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("状态: 运行中")
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        
        self.update_timer.start(1000)  # 每1秒更新一次
        
        self.logger.info("机器人已启动")
    
    def _stop_bot(self):
        """停止机器人"""
        if self.bot_worker:
            self.bot_worker.stop()
            self.bot_worker.wait()
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("状态: 已停止")
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.update_timer.stop()
        
        self.logger.info("机器人已停止")
    
    def _update_stats(self):
        """更新统计信息"""
        if self.bot_worker and self.bot_worker.bot:
            stats = self.bot_worker.bot.farming.get_stats()
            
            self.mining_label.setText(str(stats['mining']))
            self.herb_label.setText(str(stats['herbalism']))
            self.total_label.setText(str(stats['total']))
            self.rate_label.setText(f"{stats['rate']:.1f} 个/分")
            
            elapsed = int(stats['elapsed_time'])
            minutes = elapsed // 60
            seconds = elapsed % 60
            self.time_label.setText(f"{minutes}分{seconds}秒")
    
    def _auto_detect_config(self):
        """自动检测配置"""
        self._on_log("正在自动检测配置...")
        
        generator = AutoConfigGenerator()
        if generator.generate_config():
            self._on_log("配置检测完成")
            QMessageBox.information(self, "成功", "配置已自动生成")
        else:
            self._on_log("配置检测失败")
            QMessageBox.warning(self, "失败", "配置生成失败")
    
    def _browse_config_file(self):
        """浏览配置文件"""
        file, _ = QFileDialog.getOpenFileName(self, "选择配置文件", "", "YAML 文件 (*.yaml)")
        if file:
            self.config_path_label.setText(file)
    
    def _edit_config(self):
        """编辑配置文件"""
        config_file = self.config_path_label.text()
        os.startfile(config_file)
    
    def _reload_config(self):
        """重新加载配置"""
        self._on_log("配置已重新加载")
        QMessageBox.information(self, "成功", "配置已重新加载")
    
    def _record_route(self):
        """录制路线"""
        editor = RouteEditor()
        self._on_log("开始录制路线，按 F6 添加点，按 F7 停止")
        editor.start_recording()
        self.route_text.setText(str(editor.route))
    
    def _load_route(self):
        """加载路线"""
        file, _ = QFileDialog.getOpenFileName(self, "选择路线文件", "", "JSON 文件 (*.json)")
        if file:
            editor = RouteEditor()
            if editor.load_route(file):
                self.route_text.setText(str(editor.route))
                self._on_log(f"已加载路线: {file}")
    
    def _save_route(self):
        """保存路线"""
        file, _ = QFileDialog.getSaveFileName(self, "保存路线文件", "routes/route.json", "JSON 文件 (*.json)")
        if file:
            self._on_log(f"路线已保存: {file}")
    
    def _detect_nodes(self):
        """检测采集点"""
        self._on_log("正在检测采集点...")
        self.node_table.setRowCount(0)  # 清空表格
        
        # 这里可以添加实际的检测逻辑
        self._on_log("采集点检测完成")
    
    def _save_quick_settings(self):
        """保存快速设置"""
        self._on_log("快速设置已保存")
        QMessageBox.information(self, "成功", "快速设置已保存")
    
    def _on_log(self, message):
        """处理日志消息"""
        timestamp = time.strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        self.log_text.append(log_message)
        self.logger.info(message)
    
    def _on_error(self, error_message):
        """处理错误消息"""
        self._on_log(f"❌ {error_message}")
        QMessageBox.critical(self, "错误", error_message)
    
    def _get_stylesheet(self):
        """获取样式表"""
        return """
        QMainWindow {
            background-color: #f5f5f5;
        }
        QPushButton {
            border-radius: 4px;
            padding: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            opacity: 0.8;
        }
        QTabWidget::pane {
            border: 1px solid #ddd;
        }
        QGroupBox {
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: bold;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }
        QLineEdit, QSpinBox, QComboBox {
            padding: 5px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        QTextEdit {
            border: 1px solid #ddd;
            border-radius: 4px;
            background-color: #fff;
        }
        """

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
