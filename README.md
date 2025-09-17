# TC-ACApp 多人实时对战游戏

## 项目简介

TC-ACApp是一个基于Django + WebSocket的多人实时对战游戏，专为腾讯面试准备开发。该项目展示了全栈开发能力，包含完整的用户系统、实时通信、游戏匹配、技能战斗等核心功能。

## 技术特色

### 🎯 核心技术栈
- **后端**: Django 4.2.24 + Django Channels (WebSocket)
- **数据库**: SQLite3 + Redis缓存
- **前端**: 原生JavaScript + HTML5 Canvas
- **通信**: Thrift RPC + WebSocket实时通信
- **部署**: uWSGI + Nginx

### 🎮 游戏特性
- **3人实时对战**: 基于积分的智能匹配系统
- **技能战斗**: 火球术、闪烁技能，带冷却时间机制
- **动态血量**: 实时伤害计算与视觉反馈
- **积分排位**: 胜负影响玩家积分，类似ELO系统
- **实时聊天**: 游戏内即时通信功能

## 系统架构

### 后端架构
```
├── tc_acapp/           # Django项目配置
├── game/               # 游戏主应用
│   ├── models/         # 玩家数据模型
│   ├── consumers/      # WebSocket消费者
│   ├── views/          # HTTP视图处理
│   └── static/         # 游戏前端资源
├── match_system/       # 匹配系统服务
│   ├── thrift/         # RPC接口定义
│   └── src/            # 匹配算法实现
```

### 核心模块

#### 1. 用户系统
- **注册/登录**: 完整的用户认证机制
- **玩家模型**: 用户信息、头像、积分管理
- **安全验证**: 密码加密、会话管理

#### 2. 匹配系统
- **智能匹配**: 基于积分差值和等待时间的匹配算法
- **Thrift RPC**: 高性能的服务间通信
- **房间管理**: 动态创建3人对战房间

#### 3. 实时游戏
- **WebSocket通信**: 低延迟的实时数据同步
- **Canvas渲染**: 流畅的游戏画面和动画效果
- **状态同步**: 玩家位置、技能、伤害的实时同步

#### 4. 游戏玩法
```
// 技能系统
- 火球术(Q键): 远程攻击，3秒冷却
- 闪烁(F键): 瞬移技能，5秒冷却

// 操作方式
- 左键: 移动角色
- 右键: 释放选中的技能
- 回车: 打开聊天
```

## 安装与运行

### 环境要求
```bash
Python 3.8+
Redis 6.0+
Node.js (用于JavaScript压缩)
```

### 快速开始
```bash
# 1. 克隆项目
git clone <repository-url>
cd tc_acapp-master

# 2. 安装Python依赖
pip install django==4.2.24
pip install channels channels-redis
pip install django-redis thrift

# 3. 启动Redis
redis-server
# 4. 数据库迁移
python manage.py migrate

# 5. 编译前端资源
bash scripts/compress_game_js.sh

# 6. 启动匹配系统
cd match_system/src
python main.py &

# 7. 启动Django服务器
python manage.py runserver
```

### 生产环境部署
```bash
# 使用uWSGI部署
uwsgi --ini scripts/uwsgi.ini

# 收集静态文件
python manage.py collectstatic
```

## 项目亮点

### 🔥 技术实现
1. **实时多人同步**: 使用WebSocket实现毫秒级的游戏状态同步
2. **智能匹配算法**: 基于玩家积分和等待时间的平衡匹配机制
3. **微服务架构**: 匹配系统独立部署，使用Thrift RPC通信
4. **前端游戏引擎**: 纯JavaScript实现的轻量级游戏引擎

### 🎨 用户体验
1. **响应式设计**: 支持不同分辨率的设备适配
2. **流畅动画**: Canvas绘制的高帧率游戏画面
3. **实时反馈**: 伤害特效、粒子系统、技能冷却显示
4. **社交功能**: 游戏内实时聊天系统

### 📊 性能优化
1. **Redis缓存**: 游戏房间状态和玩家数据缓存
2. **资源压缩**: JavaScript文件自动压缩合并
3. **连接池**: 数据库连接复用和优化
4. **静态资源**: CDN加速的图片和字体资源

## 核心算法

### 匹配算法
```python
def check_match(self, a, b):
    dt = abs(a.score - b.score)
    a_max_dif = a.waiting_time * 50
    b_max_dif = b.waiting_time * 50
    return dt <= a_max_dif and dt <= b_max_dif
```

### 积分系统
- 获胜: +10分
- 失败: -5分
- 匹配考虑积分差距和等待时间

## 技术选型说明

### 为什么选择Django?
- **快速开发**: 内置用户认证、管理后台
- **WebSocket支持**: Django Channels提供异步支持
- **生态成熟**: 丰富的第三方库和部署方案

### 为什么选择Canvas?
- **性能优秀**: 硬件加速的2D渲染
- **控制灵活**: 像素级的绘制控制
- **兼容性好**: 现代浏览器全面支持

### 为什么使用Redis?
- **高性能**: 内存数据库，微秒级响应
- **数据结构**: 支持复杂的游戏状态存储
- **持久化**: 数据安全保障

## 面试要点

### 展示的技术能力
1. **全栈开发**: 前后端完整实现
2. **实时通信**: WebSocket双向通信
3. **分布式系统**: 微服务架构设计
4. **性能优化**: 缓存、压缩、异步处理
5. **用户体验**: 游戏交互设计

### 可扩展的技术方向
- **负载均衡**: Nginx反向代理
- **容器化**: Docker部署方案
- **监控告警**: 游戏数据统计
- **AI机器人**: 更智能的游戏AI

## 在线体验

部署地址: `app7581.acapp.acwing.com.cn`

---

**开发者**: [J.Grigg]  
**开发时间**: [2025/9]  
**联系方式**: [2064747320@qq.com]
