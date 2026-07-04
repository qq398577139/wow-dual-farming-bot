# 快速开始脚本

## 安装依赖
```bash
pip install -r requirements.txt
```

## 生成自动配置
```bash
python -m src.config_generator
```

## 启动脚本
```bash
python main.py
```

## 启动 Web 控制面板
```bash
python -m src.web_panel
```

然后访问 http://localhost:5000

## 编辑路线
```bash
python -m src.route_editor
```

## 运行测试
```bash
python -m pytest tests/
```

## 查看日志
```bash
tail -f logs/bot.log
```
