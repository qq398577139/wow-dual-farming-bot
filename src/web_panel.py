#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的 Web 控制面板
"""

from flask import Flask, render_template, jsonify, request
from src.bot import FarmingBot
from src.logger import BotLogger
import threading
import json

app = Flask(__name__)
bot_instance = None
bot_thread = None

logger = BotLogger('WebPanel', 'logs/web_panel.log')

@app.route('/')
def index():
    """主页"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>WoW 双采脚本 - 控制面板</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
            }
            .button-group {
                display: flex;
                gap: 10px;
                margin: 20px 0;
                justify-content: center;
            }
            button {
                padding: 10px 20px;
                font-size: 14px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                background-color: #4CAF50;
                color: white;
            }
            button:hover {
                background-color: #45a049;
            }
            button.stop {
                background-color: #f44336;
            }
            button.stop:hover {
                background-color: #da190b;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 10px;
                margin: 20px 0;
            }
            .stat-box {
                background-color: #f9f9f9;
                padding: 15px;
                border-left: 4px solid #4CAF50;
                border-radius: 4px;
            }
            .stat-box h3 {
                margin: 0 0 10px 0;
                color: #666;
                font-size: 14px;
            }
            .stat-box .value {
                font-size: 24px;
                font-weight: bold;
                color: #333;
            }
            .log {
                background-color: #f9f9f9;
                padding: 15px;
                border-radius: 4px;
                max-height: 300px;
                overflow-y: auto;
                border: 1px solid #ddd;
            }
            .log-line {
                font-family: monospace;
                font-size: 12px;
                margin: 2px 0;
                color: #666;
            }
            .log-line.info { color: #0066cc; }
            .log-line.warning { color: #ff9900; }
            .log-line.error { color: #cc0000; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎮 WoW 双采自动化脚本</h1>
            
            <div class="button-group">
                <button onclick="startBot()">启动</button>
                <button class="stop" onclick="stopBot()">停止</button>
                <button onclick="getStats()">刷新统计</button>
            </div>
            
            <div class="stats" id="stats">
                <div class="stat-box">
                    <h3>采矿数量</h3>
                    <div class="value" id="mining-count">0</div>
                </div>
                <div class="stat-box">
                    <h3>草药数量</h3>
                    <div class="value" id="herbalism-count">0</div>
                </div>
                <div class="stat-box">
                    <h3>总采集</h3>
                    <div class="value" id="total-count">0</div>
                </div>
            </div>
            
            <h3>最近日志</h3>
            <div class="log" id="logs"></div>
        </div>
        
        <script>
            function startBot() {
                fetch('/api/start', {method: 'POST'})
                    .then(r => r.json())
                    .then(d => alert(d.message));
            }
            
            function stopBot() {
                fetch('/api/stop', {method: 'POST'})
                    .then(r => r.json())
                    .then(d => alert(d.message));
            }
            
            function getStats() {
                fetch('/api/stats')
                    .then(r => r.json())
                    .then(d => {
                        document.getElementById('mining-count').textContent = d.mining || 0;
                        document.getElementById('herbalism-count').textContent = d.herbalism || 0;
                        document.getElementById('total-count').textContent = d.total || 0;
                    });
            }
            
            // 每5秒更新一次统计
            setInterval(getStats, 5000);
            getStats();
        </script>
    </body>
    </html>
    '''

@app.route('/api/start', methods=['POST'])
def api_start():
    """启动机器人"""
    global bot_instance, bot_thread
    
    if bot_thread and bot_thread.is_alive():
        return jsonify({'success': False, 'message': '机器人已在运行'})
    
    try:
        bot_instance = FarmingBot('config/config.yaml')
        bot_thread = threading.Thread(target=bot_instance.start, daemon=True)
        bot_thread.start()
        logger.info("通过 Web 面板启动机器人")
        return jsonify({'success': True, 'message': '机器人已启动'})
    except Exception as e:
        logger.error(f"启动失败: {e}")
        return jsonify({'success': False, 'message': f'启动失败: {e}'})

@app.route('/api/stop', methods=['POST'])
def api_stop():
    """停止机器人"""
    global bot_instance
    
    if bot_instance:
        bot_instance.stop()
        logger.info("通过 Web 面板停止机器人")
        return jsonify({'success': True, 'message': '机器人已停止'})
    else:
        return jsonify({'success': False, 'message': '机器人未运行'})

@app.route('/api/stats')
def api_stats():
    """获取统计信息"""
    if bot_instance and hasattr(bot_instance, 'farming'):
        stats = bot_instance.farming.get_stats()
        return jsonify({
            'mining': stats['mining'],
            'herbalism': stats['herbalism'],
            'total': stats['total'],
            'elapsed_time': stats['elapsed_time']
        })
    else:
        return jsonify({'mining': 0, 'herbalism': 0, 'total': 0, 'elapsed_time': 0})

def main():
    """启动 Web 服务器"""
    logger.info("启动 Web 控制面板 - http://localhost:5000")
    app.run(debug=False, host='localhost', port=5000)

if __name__ == '__main__':
    main()
