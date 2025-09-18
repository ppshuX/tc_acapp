# TC-ACApp 实时多人对战游戏系统 

## 📋 项目概述

TC-ACApp 是一个基于 Django + WebSocket + Thrift RPC 的实时多人在线对战游戏平台，专为展示全栈开发技术栈而构建。项目实现了完整的用户系统、智能匹配算法、实时通信、技能战斗以及社交功能等核心模块。

### 🎯 在线体验地址
**游戏链接**: https://app7581.acapp.acwing.com.cn/

## ⭐ 核心特性

### 🎮 游戏功能
- **3人实时对战**: 基于积分的智能匹配系统，实时同步游戏状态
- **技能系统**: 火球术（Q键，3秒CD）+ 闪烁术（F键，5秒CD）
- **动态伤害**: 实时伤害计算、视觉特效与血量反馈
- **积分排位**: 获胜+10分，失败-5分，类似ELO排位系统
- **实时聊天**: 游戏内即时通信功能（Enter键打开/ESC键关闭）
- **拳皇模式(KOF)**: 独立的拳皇风格对战游戏模式
- **个人空间(MySpace)**: 完整的社交系统，包括用户互动和内容分享

### 🏷️ 社交功能
- **用户关注系统**: 关注/取消关注其他玩家，实时更新粉丝数量
- **动态发布**: 发布、查看、删除个人动态内容
- **用户列表**: 浏览所有注册用户及其基本信息
- **个人主页**: 展示用户资料、动态和社交数据

### 🔧 技术特性
- **实时通信**: WebSocket + Django Channels 实现毫秒级数据同步
- **微服务架构**: 独立匹配系统，使用Thrift RPC通信
- **游戏引擎**: 原生JavaScript + Canvas实现的轻量级2D游戏引擎
- **用户认证**: JWT Token + 中间件实现的安全认证机制
- **缓存系统**: Redis缓存游戏房间状态和用户数据
- **RESTful API**: 完整的REST API接口设计，支持前后端分离

## 🏗️ 系统架构

### 技术栈
```
后端技术：
├── Django 4.2.24         # Web框架
├── Django Channels        # WebSocket支持
├── Django REST Framework  # API接口
├── Thrift RPC            # 服务间通信
├── Redis                 # 缓存和消息队列
├── SQLite3               # 数据库
└── JWT                   # 身份验证

前端技术：
├── 原生JavaScript        # 游戏逻辑
├── HTML5 Canvas          # 游戏渲染
├── jQuery                # DOM操作
└── CSS3                  # 样式设计

部署技术：
├── uWSGI                 # WSGI服务器
├── Nginx                 # 反向代理
└── Bash Scripts          # 部署脚本
```

### 核心模块架构
```
tc_acapp/
├── tc_acapp/                    # Django项目配置
│   ├── settings.py             # 项目配置（数据库、缓存、Channels等）
│   ├── asgi.py                 # ASGI配置（WebSocket支持）
│   └── urls.py                 # 主URL路由
├── game/                       # 游戏主应用
│   ├── models/                 # 数据模型
│   │   ├── player/player.py    # 玩家模型（用户、积分、头像）
│   │   └── myspace/            # 社交功能模型
│   │       ├── post.py         # 帖子模型
│   │       └── follow.py       # 关注关系模型
│   ├── consumers/              # WebSocket消费者
│   │   └── multiplayer/index.py # 多人游戏WebSocket处理器
│   ├── views/                  # HTTP视图
│   │   ├── settings/           # 用户设置相关视图
│   │   ├── myspace/            # 个人空间相关视图
│   │   │   ├── getinfo.py      # 获取用户信息API
│   │   │   ├── post_view.py    # 动态管理API
│   │   │   ├── follow.py       # 关注系统API  
│   │   │   ├── userlist.py     # 用户列表API
│   │   │   └── player.py       # 用户注册API
│   │   ├── kof/                # 拳皇游戏相关视图
│   │   │   └── index.py        # KOF游戏入口
│   │   └── playground/         # 多人对战相关视图
│   ├── static/js/src/          # 前端JavaScript源码
│   │   ├── zbase.js            # 游戏主类
│   │   ├── playground/         # 游戏场景
│   │   ├── menu/               # 菜单系统
│   │   └── settings/           # 设置界面
│   ├── templates/              # 前端模板文件
│   │   ├── kof/index.html      # KOF拳皇游戏页面模板
│   │   ├── myspace/index.html  # MySpace个人空间页面模板
│   │   └── multiends/web.html  # 多端适配模板
│   ├── urls/                   # URL路由配置
│   │   ├── myspace/index.py    # MySpace路由配置
│   │   ├── kof/index.py        # KOF路由配置
│   │   ├── settings/index.py   # 设置路由配置
│   │   └── playground/index.py # 游戏路由配置
│   └── channelsmiddleware.py   # JWT WebSocket中间件
└── match_system/               # 匹配系统微服务
    ├── src/main.py             # 匹配服务主程序
    └── thrift/match.thrift     # Thrift接口定义
```

## 🎯 核心功能详解

### 1. MySpace个人空间系统

MySpace是一个完整的社交功能模块，为用户提供个人展示和社交互动的平台。

#### 功能特性
- **用户关注系统**: 支持关注/取消关注功能，实时更新粉丝数量
- **动态发布系统**: 发布个人动态、查看他人动态、删除自己的动态
- **用户发现**: 浏览平台上的所有用户，查看用户基本信息
- **个人主页**: 展示用户资料、动态列表和社交统计数据

#### API接口设计
```python
# 关注系统API
class FollowView(APIView):
    def post(self, request):
        source_id = request.user.id
        target_id = int(request.POST['target_id'])
        # 切换关注状态：已关注则取消，未关注则添加
        fs = Follow.objects.filter(source=source_id, target=target_id)
        if fs.exists():
            player.followerCount -= 1
            fs.delete()
        else:
            player.followerCount += 1
            Follow.objects.create(source=source_id, target=target_id)

# 动态系统API
class PostView(APIView):
    def get(self, request):
        # 获取指定用户的所有动态
        posts = Post.objects.filter(user_id=user_id).order_by('-pk')
        
    def post(self, request):
        # 发布新动态
        Post.objects.create(user_id=request.user.id, content=content)
        
    def delete(self, request):
        # 删除自己的动态
        Post.objects.filter(user_id=user.id, pk=post_id).delete()
```

#### 数据模型
```python
# 关注关系模型
class Follow(models.Model):
    source = models.IntegerField(default=0)  # 关注者ID
    target = models.IntegerField(default=0)  # 被关注者ID

# 动态内容模型
class Post(models.Model):
    user_id = models.IntegerField(default=0)
    content = models.TextField(max_length=1000)  # 动态内容
    createtime = models.DateTimeField(default=now)  # 创建时间
```

#### 前端实现
- **单页应用**: 使用Vue.js构建的现代化用户界面
- **响应式设计**: 适配不同设备屏幕尺寸
- **实时更新**: 动态内容和关注状态的实时刷新

### 2. KOF拳皇游戏模式

KOF(King of Fighters)是一个独立的格斗游戏模式，提供经典的拳皇风格对战体验。

#### 游戏特色
- **经典拳皇风格**: 模拟经典拳皇游戏的操作感受
- **独立游戏引擎**: 基于专门优化的JavaScript游戏引擎
- **流畅动画**: 高帧率的角色动画和特效系统
- **技能连招**: 支持复杂的技能组合和连击系统

#### 技术实现
```javascript
// KOF游戏主类
class KOF {
    constructor(id) {
        this.id = id;
        this.$kof = $('#' + id);
        this.setup_game_engine();
    }
    
    setup_game_engine() {
        // 初始化专用的拳皇游戏引擎
        // 不同于多人对战的playground引擎
    }
}
```

#### 界面设计
```html
<!-- KOF专用模板 -->
<div id="kof"></div>
<script type="module">
    import { KOF } from "{% static 'js/base.js' %}";
    let kof = new KOF('kof');
</script>
```

### 3. 智能匹配系统
```python
# 匹配算法核心逻辑
def check_match(self, a, b):
    dt = abs(a.score - b.score)         # 积分差值
    a_max_dif = a.waiting_time * 50     # 玩家A最大容忍差值
    b_max_dif = b.waiting_time * 50     # 玩家B最大容忍差值
    return dt <= a_max_dif and dt <= b_max_dif
```

**特性说明**:
- 基于积分的平衡匹配
- 动态调整匹配阈值（等待时间越长，容忍度越高）
- 3人小队实时匹配
- Thrift RPC实现高性能服务通信

### 2. WebSocket实时通信
```javascript
// 前端WebSocket连接
class MultiPlayerSocket {
    constructor(playground) {
        this.ws = new WebSocket("wss://app7581.acapp.acwing.com.cn/wss/multiplayer/");
        this.playground = playground;
    }
    
    // 发送玩家移动信息
    send_move_to(tx, ty) {
        this.ws.send(JSON.stringify({
            'event': 'move_to',
            'uuid': this.uuid,
            'tx': tx,
            'ty': ty,
        }));
    }
}
```

**实现功能**:
- 玩家位置同步
- 技能释放广播
- 伤害结算同步
- 游戏内聊天

### 3. 游戏引擎设计

#### 游戏对象基类
```javascript
class AcGameObject {
    constructor() {
        this.has_called_start = false;
        this.timedelta = 0;
        this.uuid = this.create_uuid();
    }
    
    update() {
        this.update_time();
        if (!this.has_called_start) {
            this.start();
            this.has_called_start = true;
        }
        this.update_game_logic();
        this.render();
    }
}
```

#### 技能系统实现
```javascript
// 火球术技能
shoot_fireball(tx, ty) {
    let angle = Math.atan2(ty - this.y, tx - this.x);
    let vx = Math.cos(angle), vy = Math.sin(angle);
    let fireball = new FireBall(this.playground, this, 
        this.x, this.y, 0.01, vx, vy, "orange", 0.5, 1, 0.01);
    this.fireballs.push(fireball);
    this.fireball_coldtime = 3; // 3秒冷却
    return fireball;
}

// 闪烁术技能
blink(tx, ty) {
    let d = this.get_dist(this.x, this.y, tx, ty);
    d = Math.min(d, 0.8); // 最大闪烁距离
    let angle = Math.atan2(ty - this.y, tx - this.x);
    this.x += d * Math.cos(angle);
    this.y += d * Math.sin(angle);
    this.blink_coldtime = 5; // 5秒冷却
}
```

### 4. 数据模型设计

#### 玩家模型
```python
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.URLField(max_length=256, blank=True)
    openid = models.CharField(default="", max_length=50, blank=True, null=True)
    score = models.IntegerField(default=1500)  # 初始积分1500
```

#### 社交功能模型
```python
# 帖子模型
class Post(models.Model):
    user_id = models.IntegerField(default=0)
    content = models.TextField(default="", max_length=1000)
    createtime = models.DateTimeField(default=now)

# 关注模型
class Follow(models.Model):
    source = models.IntegerField(default=0)  # 关注者
    target = models.IntegerField(default=0)  # 被关注者
```

## 🚀 快速部署指南

### 环境要求
```bash
Python 3.8+
Redis 6.0+
Node.js (用于JavaScript压缩)
```

### 1. 环境搭建
```bash
# 克隆项目
git clone <repository-url>
cd tc_acapp

# 安装Python依赖
pip install django==4.2.24
pip install channels channels-redis
pip install django-redis djangorestframework
pip install djangorestframework-simplejwt
pip install thrift
```

### 2. 数据库初始化
```bash
# 执行数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

### 3. 启动服务

#### 启动Redis缓存服务
```bash
redis-server
```

#### 启动匹配系统服务
```bash
cd match_system/src
python main.py &
```

#### 编译前端资源
```bash
# 执行JavaScript压缩
bash scripts/compress_game_js.sh
```

#### 启动Django开发服务器
```bash
python manage.py runserver
```

### 4. 生产环境部署
```bash
# 收集静态文件
python manage.py collectstatic

# 使用uWSGI部署
uwsgi --ini scripts/uwsgi.ini
```

## 🎮 游戏操作指南

### 多人对战模式操作
- **鼠标左键**: 移动角色到指定位置
- **鼠标右键**: 释放选中的技能
- **Q键**: 选择火球术（冷却3秒）
- **F键**: 选择闪烁术（冷却5秒）
- **Enter键**: 打开游戏内聊天
- **ESC键**: 关闭聊天界面

### KOF拳皇模式操作
- **独立控制系统**: KOF模式采用专门的格斗游戏操作方式
- **技能连招**: 支持复杂的按键组合和连击系统
- **角色切换**: 可选择不同的拳皇角色进行对战
- **特殊技能**: 每个角色都有独特的必杀技和超必杀技

### MySpace个人空间使用
#### 浏览用户
1. 访问 `/myspace/` 进入个人空间主页
2. 浏览用户列表，查看所有注册用户
3. 点击用户头像查看详细资料和动态

#### 关注系统
1. 在用户详情页面点击"关注"按钮
2. 系统自动更新关注状态和粉丝数量
3. 已关注的用户可以点击取消关注

#### 动态管理
1. **发布动态**: 在个人主页输入内容并发布
2. **查看动态**: 浏览自己和他人的动态内容
3. **删除动态**: 在自己的动态上点击删除按钮

### 游戏流程

#### 多人对战流程
1. **等待匹配**: 进入多人模式后，系统自动匹配3名玩家
2. **准备阶段**: 所有玩家进入房间，显示"已就绪：X人"
3. **战斗阶段**: 3人全部就绪后开始战斗，显示"Fighting!"
4. **胜负判定**: 最后存活的玩家获胜，积分+10；失败者积分-5

#### KOF对战流程
1. **角色选择**: 进入KOF模式后选择战斗角色
2. **对战准备**: 系统加载角色和场景资源
3. **格斗对决**: 使用格斗游戏操作进行战斗
4. **结果统计**: 显示对战结果和表现数据

### 技能系统详解
- **火球术**: 远程攻击技能，造成25点伤害，射程1个单位，冷却3秒
- **闪烁术**: 瞬移技能，最大距离0.8单位，冷却5秒
- **技能冷却**: 右下角显示技能图标和冷却进度

## 🔧 关键技术实现

### WebSocket认证中间件
```python
class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        try:
            # 从查询参数获取JWT Token
            token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]
            UntypedToken(token)  # 验证Token有效性
            decoded_data = jwt_decode(token, settings.SIMPLE_JWT["SIGNING_KEY"], 
                                    algorithms=["HS256"])
            scope["user"] = await get_user(validated_token=decoded_data)
        except:
            scope["user"] = AnonymousUser()
        return await super().__call__(scope, receive, send)
```

### 游戏状态缓存
```python
# 游戏房间信息存储在Redis中
def match_success(self, ps):
    room_name = f"room-{ps[0].uuid}-{ps[1].uuid}-{ps[2].uuid}"
    players = []
    for p in ps:
        players.append({
            'uuid': p.uuid,
            'username': p.username,
            'photo': p.photo,
            'hp': 100,  # 初始血量
        })
    cache.set(room_name, players, 3600)  # 1小时有效期
```

### 前端游戏循环
```javascript
class AcGame {
    constructor(id) {
        this.$ac_game = $('#' + id);
        this.settings = new Settings(this);
        this.menu = new AcGameMenu(this);
        this.playground = new AcGamePlayground(this);
        
        this.start_game_loop();
    }
    
    start_game_loop() {
        setInterval(() => {
            this.update();
        }, 1000/60); // 60FPS游戏循环
    }
}
```

## 📊 性能优化

### 后端优化
- **Redis缓存**: 游戏房间状态和玩家数据缓存，减少数据库查询
- **连接复用**: Django数据库连接池，提高数据库访问效率
- **Thrift RPC**: 高性能的二进制协议，减少服务间通信开销
- **异步处理**: Django Channels异步WebSocket处理，支持高并发

### 前端优化
- **JavaScript压缩**: 自动化脚本压缩合并JS文件，减少加载时间
- **Canvas优化**: 智能重绘机制，只更新变化的游戏对象
- **资源预加载**: 图片和音效资源预加载，避免游戏中卡顿
- **内存管理**: 游戏对象生命周期管理，避免内存泄漏

### 网络优化
- **WebSocket保持连接**: 减少连接建立开销
- **数据压缩**: JSON数据最小化传输
- **CDN加速**: 静态资源CDN分发，提升加载速度

## 🔐 安全特性

### 身份认证
- **JWT Token认证**: 无状态的用户认证机制
- **WebSocket认证**: 自定义中间件保护WebSocket连接
- **CSRF防护**: Django内置CSRF保护机制

### 数据安全
- **SQL注入防护**: Django ORM自动防护SQL注入
- **XSS防护**: 前端数据过滤和转义
- **输入验证**: 后端API参数严格校验

## 📈 可扩展功能

### 游戏功能扩展
- **更多技能**: 治疗、护盾、控制类技能
- **装备系统**: 武器、防具、道具系统
- **排行榜**: 全服积分排行榜
- **观战模式**: 实时观看其他玩家对战
- **房间系统**: 自定义房间、私人对战

#### KOF模式扩展
- **角色系统**: 多个可选拳皇角色，各有独特技能
- **故事模式**: 单人剧情模式，体验经典拳皇故事
- **联机对战**: 支持在线PVP拳皇对战
- **录像回放**: 精彩对局录制和回放功能
- **自定义按键**: 支持用户自定义操作按键

### MySpace社交功能扩展
- **好友系统**: 好友添加、私聊功能，建立更紧密的社交关系
- **动态交互**: 点赞、评论、转发动态，增强用户互动
- **话题标签**: 动态支持话题标签，便于内容分类和发现
- **私信系统**: 用户之间的私密消息交流
- **个人相册**: 图片上传和相册管理功能
- **活动发布**: 用户可以发布和参与社区活动
- **内容审核**: 自动化内容审核系统，维护社区环境

### 技术架构扩展
- **微服务化**: 用户服务、匹配服务、游戏服务独立部署
- **负载均衡**: Nginx负载均衡，支持多实例部署
- **容器化**: Docker容器化部署，便于扩容和维护
- **监控系统**: 性能监控、错误告警、数据统计
- **AI机器人**: 智能AI对手，丰富游戏体验
- **CDN加速**: 静态资源和媒体文件CDN分发
- **消息队列**: RabbitMQ或Kafka处理高并发消息

### 社交功能扩展
- **公会系统**: 公会创建、团队对战
- **成就系统**: 游戏成就、称号系统
- **活动系统**: 限时活动、节日特别活动
- **内容推荐**: 基于用户行为的智能内容推荐
- **社区版块**: 论坛功能，支持不同话题讨论区

## 📝 开发说明

### 项目结构说明
- `game/static/js/src/`: 前端JavaScript源代码
- `game/consumers/`: WebSocket消费者，处理实时通信
- `match_system/`: 独立的匹配系统服务
- `game/models/`: Django数据模型定义
- `game/views/`: HTTP API视图处理器
- `scripts/`: 部署和构建脚本

### 开发调试
```bash
# 启动开发模式（DEBUG=True）
python manage.py runserver

# 查看WebSocket连接日志
# 在settings.py中配置日志级别

# 监控Redis缓存
redis-cli monitor

# 查看匹配系统日志
cd match_system/src && python main.py
```

### API接口

#### 核心游戏接口
- `/settings/getinfo/`: 获取用户信息
- `/settings/register/`: 用户注册
- `/settings/ranklist/`: 获取排行榜

#### MySpace社交系统接口
- `/myspace/getinfo/`: 获取个人空间信息
- `/myspace/post/`: 帖子相关操作（GET获取动态，POST发布动态，DELETE删除动态）
- `/myspace/follow/`: 关注系统（POST切换关注状态）
- `/myspace/userlist/`: 获取用户列表（显示所有用户及粉丝数）
- `/myspace/user/`: 用户管理（POST注册新用户）

#### KOF游戏模式接口
- `/kof/`: 拳皇游戏模式入口页面

#### WebSocket实时通信接口
- `wss://域名/wss/multiplayer/`: 多人游戏WebSocket连接
  - 支持事件：`create_player`, `move_to`, `shoot_fireball`, `attack`, `blink`, `message`

## 👨‍💻 项目信息

**开发者**: [J.Grigg]  
**开发时间**: 2025年9月  
**联系方式**: 2064747320@qq.com  
**在线演示**: https://app7581.acapp.acwing.com.cn/

---

*这个项目展示了现代Web应用开发的完整技术栈，从前端游戏引擎到后端微服务架构，从实时通信到数据持久化，是一个综合性的全栈开发示例项目。*
