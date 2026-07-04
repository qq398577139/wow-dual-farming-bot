#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WoW 双采自动化脚本完整文档
"""

# 中文使用文档

"""
# WoW 双采自动化脚本 - 完整使用指南

## 目录
1. 系统要求
2. 安装步骤
3. 快速开始
4. 配置说明
5. 高级功能
6. 故障排除
7. 常见问题

---

## 1. 系统要求

### 硬件要求
- 处理器: Intel i5 或更高
- 内存: 8GB 或更高
- 硬盘: 最少 500MB 空闲空间
- 显卡: 支持 OpenCV 的任何显卡

### 软件要求
- Windows 7/8/10/11
- Python 3.8 或更高版本
- 魔兽世界时光服客户端
- 最新的显卡驱动

---

## 2. 安装步骤

### 步骤 1: 安装 Python

1. 访问 https://www.python.org/downloads/
2. 下载 Python 3.10 或更高版本
3. 安装时**必须勾选** "Add Python to PATH"
4. 验证安装:
   ```bash
   python --version
   ```

### 步骤 2: 克隆或下载项目

```bash
git clone https://github.com/qq398577139/wow-dual-farming-bot.git
cd wow-dual-farming-bot
```

或者直接下载 ZIP 文件并解压。

### 步骤 3: 安装依赖

```bash
pip install -r requirements.txt
```

如果遇到问题，可以使用中国镜像:

```bash
pip install -r requirements.txt -i https://pypi.tsinghua.edu.cn/simple
```

### 步骤 4: 配置文件

```bash
cp config/config.template.yaml config/config.yaml
```

然后编辑 `config/config.yaml` 根据你的需求调整参数。

---

## 3. 快速开始

### 方式 1: 自动配置（推荐新手）

```bash
python -m src.config_generator
```

这会自动检测你的游戏窗口并生成最优配置。

### 方式 2: 手动配置

编辑 `config/config.yaml`:

```yaml
characters:
  character1:
    name: "主号"
    account: "your_account"
    password: "your_password"
    professions: "both"  # both=双采, mining=采矿, herbalism=草药
    enabled: true
```

### 方式 3: 启动脚本

```bash
python main.py --config config/config.yaml
```

或使用调试模式:

```bash
python main.py --debug
```

---

## 4. 配置说明

### 4.1 游戏配置

```yaml
game:
  window_title: "World of Warcraft"  # 游戏窗口标题
  resolution:
    width: 1920   # 游戏窗口宽度
    height: 1080  # 游戏窗口高度
```

### 4.2 角色配置

```yaml
characters:
  character1:
    name: "主号"  # 角色名称
    account: "account1"  # 账号
    password: "password1"  # 密码
    professions: "both"  # 职业: both/mining/herbalism
    enabled: true  # 是否启用此角色
```

### 4.3 采集配置

```yaml
farming:
  mining:
    enabled: true  # 启用采矿
    detection_threshold: 0.8  # 检测阈值（0-1）
    hotkey: "1"  # 采矿技能快捷键
  herbalism:
    enabled: true  # 启用草药采集
    detection_threshold: 0.8  # 检测阈值
    hotkey: "2"  # 草药技能快捷键
```

### 4.4 战斗配置

```yaml
combat:
  enabled: true  # 启用战斗逃脱
  escape_method: "mount"  # 逃脱方式: mount/run
  mount_hotkey: "3"  # 坐骑快捷键
  sensitivity: 0.5  # 敏感度（0-1）
```

### 4.5 视觉配置

```yaml
vision:
  enabled: true  # 启用视觉识别
  update_interval: 0.5  # 更新间隔（秒）
  mining_color:  # 采矿点颜色（HSV）
    h: [0, 30]   # 色调范围
    s: [50, 255] # 饱和度范围
    v: [50, 255] # 亮度范围
```

---

## 5. 高级功能

### 5.1 路线编辑器

使用路线编辑器创建自定义采集路线:

```bash
python -m src.route_editor
```

**操作方法:**
1. 选择 "1. 记录新路线"
2. 在游戏中走到采集点
3. 按 **F6** 标记该点
4. 按 **F7** 停止记录
5. 选择保存

### 5.2 性能监控

脚本会自动监控性能并输出报告。你也可以在运行时检查性能:

```bash
# 查看性能日志
tail -f logs/performance.log
```

### 5.3 调试模式

启用调试模式获取详细日志:

```bash
python main.py --debug
```

日志位置: `logs/bot.log`

---

## 6. 故障排除

### 问题 1: "找不到游戏窗口"

**解决方案:**
1. 确保魔兽世界客户端已打开
2. 检查窗口标题是否正确
3. 修改 `config.yaml` 中的 `window_title`

### 问题 2: "未检测到采集点"

**解决方案:**
1. 检查视觉配置中的颜色范围
2. 运行 `python -m src.config_generator` 自动检测
3. 手动调整 `mining_color` 和 `herbalism_color`

### 问题 3: "脚本一直在某处转圈"

**解决方案:**
1. 检查路线是否正确设置
2. 尝试手动编辑路线: `python -m src.route_editor`
3. 增加 `navigation.arrival_distance` 的值

### 问题 4: "经常误判为战斗状态"

**解决方案:**
1. 调整 `combat.sensitivity` 的值（降低灵敏度）
2. 修改敌人颜色检测范围
3. 增加 `vision.update_interval`

### 问题 5: "脚本运行缓慢"

**解决方案:**
1. 降低游戏分辨率或图形设置
2. 关闭其他占用CPU的程序
3. 增加 `routes.stop_duration` 以给游戏更多响应时间

---

## 7. 常见问题

### Q: 脚本会被检测到吗？
A: 本脚本使用了大量的延迟和随机性来避免检测，但使用任何自动化脚本都存在风险。请自行承担责任。

### Q: 能否多开运行？
A: 可以，但需要：
1. 为每个实例创建单独的配置文件
2. 使用不同的日志文件
3. 运行多个 Python 实例

### Q: 脚本支持哪些职业？
A: 脚本支持任何有采矿和草药采集技能的职业。

### Q: 如何停止脚本？
A: 按 **Ctrl+C** 停止脚本。脚本会输出最终统计信息。

### Q: 可以自定义快捷键吗？
A: 可以，在 `config.yaml` 中修改 `hotkey` 设置。

### Q: 日志保存在哪里？
A: 日志保存在 `logs/` 目录下：
- `bot.log` - 主程序日志
- `performance.log` - 性能日志
- `config_generator.log` - 配置生成日志

### Q: 如何报告 Bug？
A: 请在 GitHub 上提交 Issue:
https://github.com/qq398577139/wow-dual-farming-bot/issues

---

## 支持和反馈

如有问题，请通过以下方式联系:
- GitHub Issues: https://github.com/qq398577139/wow-dual-farming-bot/issues
- 邮件: qq398577139@qq.com

---

## 免责声明

本脚本仅供学习和研究使用。使用本脚本可能违反魔兽世界的服务条款。
使用者需自行承担使用本脚本的一切后果，本项目不承担任何责任。

---

更新时间: 2024年
版本: 1.0.0
"""
