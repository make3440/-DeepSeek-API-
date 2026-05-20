# 🚀 Docker一键部署 - 快速命令卡

## ⚡ 最简部署流程（3步完成）

### 第1步：获取DeepSeek API密钥
```
🌐 访问：https://platform.deepseek.com/
📝 操作：注册账号 → 获取API Key → 复制密钥
```

### 第2步：配置并部署（复制粘贴即可）
```bash
# 进入项目目录
cd medication-assistant

# 设置API密钥（替换为你的密钥）
export DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxx"

# 运行一键部署
chmod +x deploy.sh && ./deploy.sh
```

### 第3步：访问服务
```
✅ 打开浏览器访问：http://localhost:8000
```

---

## 📋 本地部署（无需域名）

### 完整命令序列
```bash
# 1. 进入项目目录
cd medication-assistant

# 2. 配置API密钥
export DEEPSEEK_API_KEY="sk-你的密钥"

# 3. 一键部署
chmod +x deploy.sh
./deploy.sh

# 4. 等待3-5分钟（首次构建）

# 5. 访问
open http://localhost:8000
```

---

## ☁️ 云服务器部署

### 服务器准备（一次性操作）
```bash
# 1. SSH连接服务器
ssh root@你的服务器IP

# 2. 安装Docker
curl -fsSL https://get.docker.com | sh
systemctl enable docker

# 3. 上传项目（本地执行）
scp -r medication-assistant root@服务器IP:/root/

# 4. 进入项目目录
cd medication-assistant
```

### 部署命令（每次部署）
```bash
# 方式A：简单部署（IP访问）
export DEEPSEEK_API_KEY="sk-你的密钥"
chmod +x deploy.sh && ./deploy.sh

# 方式B：域名部署（推荐）
chmod +x setup-domain.sh && ./setup-domain.sh
```

### 访问地址
```
📍 简单部署：http://你的服务器IP:8000
📍 域名部署：https://你的域名.com
```

---

## 🔧 常用运维命令

### 服务管理
```bash
# 查看状态
docker-compose -f docker/docker-compose.yml ps

# 重启服务
docker-compose -f docker/docker-compose.yml restart

# 停止服务
docker-compose -f docker/docker-compose.yml down

# 完全重建
docker-compose -f docker/docker-compose.yml down && docker-compose -f docker/docker-compose.yml up -d --build
```

### 日志查看
```bash
# 实时日志
docker-compose -f docker/docker-compose.yml logs -f

# 最近100行
docker-compose -f docker/docker-compose.yml logs --tail 100
```

### 更新代码
```bash
git pull
docker-compose -f docker/docker-compose.yml up -d --build
```

---

## 🐛 快速故障排除

### 常见问题30秒解决

| 问题 | 快速检查 | 解决方法 |
|------|---------|---------|
| 服务启动失败 | `docker-compose ps` | 查看日志：`docker-compose logs` |
| API连接错误 | 检查密钥 | 确认密钥正确且未过期 |
| 端口被占用 | `lsof -i :8000` | 改端口或停止占用程序 |
| 构建失败 | 网络检查 | `docker system prune -a` 后重建 |
| 内存不足 | `free -h` | 增加Swap或升级配置 |

### 诊断命令
```bash
# 一键诊断
docker --version && docker-compose --version && docker-compose ps && curl -f http://localhost:8000/
```

---

## 📊 部署时间估算

| 环境 | 首次部署 | 后续更新 |
|------|---------|---------|
| 本地（Mac/Windows） | 5-10分钟 | 10-30秒 |
| 云服务器（国内） | 3-5分钟 | 10-30秒 |
| 云服务器（海外） | 5-15分钟 | 30秒-1分钟 |

---

## ✅ 部署成功标志

看到以下输出表示部署成功：
```bash
========================================
  ✅ 服务启动成功！
========================================

📍 访问地址:
   - API服务: http://localhost:8000
   - API文档: http://localhost:8000/docs
   - Web界面: http://localhost:8000
```

---

## 📖 更多文档

- 完整部署指南：[DOCKER-DEPLOYMENT.md](file:///workspace/medication-assistant/medication-assistant/DOCKER-DEPLOYMENT.md)
- 域名配置指南：[DOMAIN-SETUP-GUIDE.md](file:///workspace/medication-assistant/medication-assistant/DOMAIN-SETUP-GUIDE.md)
- 项目说明文档：[README.md](file:///workspace/medication-assistant/medication-assistant/README.md)

---

## 🎯 推荐工作流

### 快速测试（本地）
```bash
export DEEPSEEK_API_KEY="sk-xxx" && ./deploy.sh && open http://localhost:8000
```

### 生产部署（云服务器+域名）
```bash
export DEEPSEEK_API_KEY="sk-xxx" && ./setup-domain.sh
```

---

**提示**：复制以上命令到终端，按回车即可执行！🚀
