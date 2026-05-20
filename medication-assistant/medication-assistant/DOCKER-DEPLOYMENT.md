# Docker一键部署指南

本文档详细介绍如何使用Docker一键部署社区用药AI助手。

## 📋 部署方式选择

### 方式一：本地快速部署（推荐测试使用）
**适用场景**：本地测试、功能验证
**访问地址**：http://localhost:8000

### 方式二：云服务器部署（生产环境）
**适用场景**：正式上线、对外服务
**访问地址**：http://你的服务器IP:8000 或 https://你的域名.com

---

## 🚀 方式一：本地快速部署（无需域名）

### 前置准备

1. **安装Docker Desktop**
   - Windows: https://docs.docker.com/desktop/install/windows-install/
   - Mac: https://docs.docker.com/desktop/install/mac-install/
   - Linux: https://docs.docker.com/engine/install/

2. **获取DeepSeek API密钥**
   - 访问 https://platform.deepseek.com/
   - 注册账号并获取API密钥

### 部署步骤

#### 1. 进入项目目录
```bash
cd medication-assistant
```

#### 2. 配置API密钥（任选一种方式）

**方式A：环境变量（推荐）**
```bash
# Linux/Mac
export DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxx"

# Windows CMD
set DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx

# Windows PowerShell
$env:DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxx"
```

**方式B：修改配置文件**
```bash
# 编辑配置文件
vim backend/config.py

# 找到并修改：
DEEPSEEK_API_KEY = "sk-xxxxxxxxxxxxx"  # 填入你的密钥
```

#### 3. 运行一键部署
```bash
# 赋予执行权限
chmod +x deploy.sh

# 运行部署脚本
./deploy.sh
```

#### 4. 等待部署完成
脚本会自动：
- ✅ 检查Docker环境
- ✅ 构建Docker镜像（约3-5分钟）
- ✅ 启动服务
- ✅ 验证服务状态

#### 5. 访问服务

打开浏览器访问：**http://localhost:8000**

你应该能看到：
- ✅ 社区用药AI助手Web界面
- ✅ 智能用药咨询功能
- ✅ 药物相互作用检查

---

## ☁️ 方式二：云服务器部署（生产环境）

### 前置准备

#### 1. 购买云服务器（推荐配置）
- **平台**：阿里云轻量应用服务器 / 腾讯云轻量应用服务器
- **系统**：Ubuntu 20.04 LTS
- **配置**：2核2G内存 起
- **费用**：约30-50元/月
- **购买链接**：
  - 阿里云：https://www.aliyun.com/product/swas
  - 腾讯云：https://cloud.tencent.com/product/lighthouse

#### 2. 配置云服务器安全组
登录云服务器控制台，开放以下端口：
- **80** - HTTP服务
- **443** - HTTPS服务
- **22** - SSH远程连接

#### 3. 安装Docker
连接到服务器：
```bash
ssh root@你的服务器IP
```

安装Docker：
```bash
# 一键安装Docker
curl -fsSL https://get.docker.com | sh

# 设置Docker开机自启
systemctl enable docker

# 验证安装
docker --version
```

#### 4. 获取DeepSeek API密钥
访问 https://platform.deepseek.com/ 注册并获取API密钥

#### 5. 上传项目代码
**方式A：使用git克隆（如果有仓库）**
```bash
git clone https://github.com/your-repo/medication-assistant.git
cd medication-assistant
```

**方式B：使用SCP上传**
```bash
# 在本地执行（不是服务器）
scp -r medication-assistant root@你的服务器IP:/root/
```

#### 6. 开始部署
```bash
# 进入项目目录
cd medication-assistant

# 方式A：简单部署（IP访问，无需域名）
chmod +x deploy.sh
export DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxx"
./deploy.sh

# 方式B：域名部署（推荐）
chmod +x setup-domain.sh
./setup-domain.sh
```

#### 7. 访问服务

**简单部署**：
```
http://你的服务器IP:8000
```

**域名部署**：
```
https://你的域名.com
```

---

## 📝 常用Docker命令

### 服务管理
```bash
# 查看服务状态
docker-compose -f docker/docker-compose.yml ps

# 查看实时日志
docker-compose -f docker/docker-compose.yml logs -f

# 重启服务
docker-compose -f docker/docker-compose.yml restart

# 停止服务
docker-compose -f docker/docker-compose.yml down

# 停止并删除容器
docker-compose -f docker/docker-compose.yml down -v

# 完全重建（清除缓存）
docker-compose -f docker/docker-compose.yml down --rmi all
docker-compose -f docker/docker-compose.yml up -d --build
```

### 更新部署
```bash
# 拉取最新代码
git pull origin main

# 重新构建并启动
docker-compose -f docker/docker-compose.yml up -d --build
```

### 容器操作
```bash
# 进入容器内部
docker exec -it medication-assistant /bin/bash

# 查看容器资源使用
docker stats

# 查看容器IP地址
docker inspect medication-assistant | grep IPAddress
```

### 日志管理
```bash
# 查看最近100行日志
docker-compose -f docker/docker-compose.yml logs --tail 100

# 导出日志到文件
docker-compose -f docker/docker-compose.yml logs > deployment.log

# 清空日志文件
truncate -s 0 /var/lib/docker/containers/*/*-json.log
```

---

## 🔧 配置文件说明

### 环境变量配置

创建 `.env` 文件（可选）：
```bash
cd medication-assistant
vim .env
```

添加以下内容：
```env
# DeepSeek API配置
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxx
DEEPSEEK_API_BASE=https://api.deepseek.com/v1

# 安全设置
REQUIRE_API_KEY=false
```

### API密钥设置

编辑 `backend/config.py`：
```python
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-xxxxxxxxxxxxx")
```

---

## 🐛 常见问题与解决方案

### 问题1：Docker未安装
**错误信息**：`docker: command not found`

**解决方案**：
```bash
# Ubuntu/Debian
apt update
apt install -y docker.io docker-compose

# CentOS/RHEL
yum install -y docker docker-compose

# 或使用官方安装脚本
curl -fsSL https://get.docker.com | sh
```

### 问题2：端口被占用
**错误信息**：`port is already allocated`

**解决方案**：
```bash
# 查看哪个进程占用了端口
lsof -i :8000

# 或修改docker-compose.yml中的端口映射
ports:
  - "8080:8000"  # 改为8080端口
```

### 问题3：API密钥无效
**错误信息**：`Invalid API key`

**解决方案**：
1. 登录 https://platform.deepseek.com/
2. 进入"API Keys"页面
3. 检查密钥是否过期或被禁用
4. 重新生成新密钥

### 问题4：构建失败
**错误信息**：`build failed`

**解决方案**：
```bash
# 清除Docker缓存
docker system prune -a

# 重新构建
docker-compose -f docker/docker-compose.yml build --no-cache
docker-compose -f docker/docker-compose.yml up -d
```

### 问题5：服务无法启动
**错误信息**：`service failed to start`

**解决方案**：
```bash
# 查看详细错误日志
docker-compose -f docker/docker-compose.yml logs medication-assistant

# 检查Docker服务状态
systemctl status docker

# 重启Docker服务
systemctl restart docker
```

### 问题6：内存不足
**错误信息**：`out of memory`

**解决方案**：
```bash
# 查看内存使用
free -h

# 增加Swap空间
dd if=/dev/zero of=/swapfile bs=1M count=2048
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# 或者减少Docker内存限制
# 编辑 /etc/docker/daemon.json
{
  "memory": "512m"
}
```

---

## 🔒 安全建议

### 生产环境必做

#### 1. 设置API密钥验证
编辑 `backend/config.py`：
```python
REQUIRE_API_KEY = True  # 启用API密钥验证
```

#### 2. 限制CORS来源
编辑 `backend/main.py`：
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # 只允许你的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 3. 配置防火墙
```bash
# 只开放必要端口
ufw allow 22/tcp    # SSH
ufw allow 80/tcp     # HTTP
ufw allow 443/tcp    # HTTPS
ufw enable
```

#### 4. 定期更新
```bash
# 定期更新依赖包
docker-compose -f docker/docker-compose.yml pull
docker-compose -f docker/docker-compose.yml up -d --build

# 更新系统
apt update && apt upgrade -y
```

#### 5. 备份配置
```bash
# 备份重要配置
tar -czf backup.tar.gz backend/config.py .env
```

---

## 📊 部署检查清单

部署完成后，请逐项检查：

- [ ] Docker已安装并运行
- [ ] DeepSeek API密钥已配置
- [ ] 服务已启动：`docker-compose ps`
- [ ] 可以访问Web界面
- [ ] 可以发送消息并获得回复
- [ ] 药物相互作用检查功能正常
- [ ] 日志无错误：`docker-compose logs`
- [ ] 安全组已配置（如在云服务器）
- [ ] 防火墙已配置（如需要）

---

## 🎯 快速测试命令

部署完成后，运行以下命令快速测试：

```bash
# 1. 检查服务状态
docker-compose -f docker/docker-compose.yml ps

# 2. 测试API接口
curl http://localhost:8000/

# 3. 测试聊天功能
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"头痛怎么办"}'

# 4. 查看实时日志
docker-compose -f docker/docker-compose.yml logs -f
```

---

## 💡 提示

1. **首次部署较慢**：Docker首次构建需要下载依赖，约3-5分钟
2. **后续更新快**：使用Docker缓存，后续更新只需几秒钟
3. **查看日志**：遇到问题先查看日志 `docker-compose logs`
4. **保持密钥安全**：不要将API密钥提交到git仓库
5. **监控资源**：生产环境建议使用 `docker stats` 监控资源使用

---

## 📞 获取帮助

如果遇到问题：
1. 查看本文档的"常见问题"部分
2. 查看项目README.md
3. 查看域名配置指南DOMAIN-SETUP-GUIDE.md
4. 运行诊断命令：
```bash
docker --version
docker-compose --version
docker-compose logs
```

祝您部署顺利！🎉
