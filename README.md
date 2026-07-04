# WoW 双采自动化脚本

魔兽世界时光服索拉查盆地双采自动化脚本，支持自动采矿和草药采集。

## 功能特性

- ✅ 自动采矿和草药采集
- ✅ 路线规划和导航
- ✅ 自动位置识别
- ✅ 战斗自动逃脱
- ✅ 多角色切换管理
- ✅ 采集日志记录
- ✅ 配置文件支持

## 环境要求

- Python 3.8+
- Windows 系统（用于游戏窗口交互）
- 魔兽世界时光服客户端
- 必要的 Python 依赖包

## 安装

1. 克隆仓库
```bash
git clone https://github.com/qq398577139/wow-dual-farming-bot.git
cd wow-dual-farming-bot
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置文件
```bash
cp config/config.template.yaml config/config.yaml
# 编辑 config.yaml 配置你的参数
```

## 使用方法

### 基础使用
```bash
python main.py
```

### 指定配置文件
```bash
python main.py --config config/config.yaml
```

### 启用调试模式
```bash
python main.py --debug
```

## 项目结构

```
wow-dual-farming-bot/
├── main.py                 # 主入口文件
├── requirements.txt        # 依赖管理
├── config/
│   ├── config.template.yaml # 配置模板
│   └── config.yaml         # 配置文件（本地）
├── src/
│   ├── __init__.py
│   ├── bot.py             # 机器人核心逻辑
│   ├── vision.py          # 图像识别模块
│   ├── navigation.py      # 路线规划模块
│   ├── farming.py         # 采集模块
│   ├── combat.py          # 战斗逃脱模块
│   ├── character.py       # 角色管理模块
│   ├── logger.py          # 日志模块
│   └── utils.py           # 工具函数
├── routes/
│   └── solace_basin.py    # 索拉查盆地路线
├── logs/
│   └── .gitkeep
└── tests/
    └── __init__.py
```

## 配置说明

详见 `config/config.template.yaml`

## 免责声明

该脚本仅供学习和研究使用。使用本脚本可能违反魔兽世界的服务条款。使用者需自行承担使用本脚本的一切后果，本项目不承担任何责任。

## License

MIT License

## 贡献

欢迎提交 Issues 和 Pull Requests！

## 联系方式

如有问题，请提交 Issue 或联系维护者。
