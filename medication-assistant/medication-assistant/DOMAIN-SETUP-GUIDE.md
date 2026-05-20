# 域名配置完整指南

本文档详细介绍如何为社区用药AI助手配置域名和HTTPS证书。

## 📋 配置概览

```
域名购买 → DNS解析 → SSL证书 → Nginx配置 → 启动服务
```

预计完成时间：**30分钟-1小时**

## 第一步：购买域名

### 推荐平台

1. **阿里云万网**（推荐，国内速度快）
   - 网站：https://wanwang.aliyun.com/
   - 价格：.com约55元/年，.cn约35元/年
   - 优点：国内速度快，SSL证书申请方便

2. **腾讯云DNSPod**
   - 网站：https://dnspod.cloud.tencent.com/
   - 价格：.com约53元/年
   - 优点：SSL证书管理方便

3. **Namesilo**（国际平台，价格便宜）
   - 网站：https://www.namesilo.com/
   - 价格：.com约49元/年
   - 优点：价格便宜，隐私保护好

### 购买建议

- 首选 `.com` 或 `.cn` 域名
- 避免使用特殊字符或过长的域名
- 建议一次购买多年，避免忘记续费

## 第二步：配置DNS解析

购买域名后，需要将域名指向你的服务器IP。

### 阿里云DNS配置

1. 登录阿里云控制台
2. 进入"云解析DNS" -> "域名解析"
3. 点击"添加解析"

添加以下记录：

| 记录类型 | 主机记录 | 记录值 | TTL |
|---------|---------|--------|-----|
| A | @ | 你的服务器公网IP | 600秒 |
| A | www | 你的服务器公网IP | 600秒 |

### 腾讯云DNSPod配置

1. 登录DNSPod控制台
2. 进入"我的域名" -> 添加域名
3. 添加记录：

| 记录类型 | 主机记录 | 记录值 | TTL |
|---------|---------|--------|-----|
| A | @ | 你的服务器公网IP | 600 |
| A | www | 你的服务器公网IP | 600 |

### 验证DNS配置

配置完成后，可以通过以下方式验证：

```bash
# 使用dig命令查看解析结果
dig your-domain.com

# 或使用nslookup
nslookup your-domain.com

# 检查域名是否指向正确IP
ping your-domain.com
```

**注意**：DNS解析通常需要5分钟-24小时生效，大多数情况下10分钟内生效。

## 第三步：申请SSL证书

SSL证书用于启用HTTPS加密，保护用户数据安全。

### 方法一：Let's Encrypt免费证书（推荐）

Let's Encrypt提供免费的SSL证书，支持自动续期。

#### 3.1.1 安装Certbot

连接到你的服务器：

```bash
ssh root@你的服务器IP
```

安装Certbot：

```bash
# Ubuntu/Debian
apt update
apt install -y certbot python3-certbot-nginx

# CentOS/RHEL
yum install -y epel-release
yum install -y certbot python3-certbot-nginx
```

#### 3.1.2 申请证书

确保DNS解析已生效后，执行：

```bash
certbot certonly --nginx -d your-domain.com -d www.your-domain.com
```

按提示输入：
- 邮箱地址（用于过期提醒）
- 同意服务条款（A）
- 同意分享邮箱（可选）

#### 3.1.3 证书位置

成功申请后，证书保存在：

```
/etc/letsencrypt/live/your-domain.com/
├── fullchain.pem    # 完整证书链
├── privkey.pem      # 私钥
├── cert.pem         # 服务器证书
└── chain.pem        # 中间证书
```

#### 3.1.4 复制证书到项目目录

```bash
# 创建SSL目录
mkdir -p medication-assistant/docker/ssl

# 复制证书
cp /etc/letsencrypt/live/your-domain.com/fullchain.pem medication-assistant/docker/ssl/cert.pem
cp /etc/letsencrypt/live/your-domain.com/privkey.pem medication-assistant/docker/ssl/key.pem

# 设置权限
chmod 600 medication-assistant/docker/ssl/key.pem
```

#### 3.1.5 配置自动续期

Let's Encrypt证书有效期90天，但可以自动续期：

```bash
# 测试续期（不实际执行）
certbot renew --dry-run

# 设置定时任务自动续期
crontab -e

# 添加以下行（每天凌晨2点检查续期）
0 2 * * * certbot renew --quiet && systemctl restart nginx
```

### 方法二：阿里云免费证书

#### 3.2.1 申请免费证书

1. 登录阿里云控制台
2. 进入"SSL证书" -> "免费证书"
3. 点击"立即购买"（免费）
4. 创建证书，填写域名信息
5. 选择验证方式（DNS验证）
6. 按提示添加DNS记录

#### 3.2.2 下载证书

审核通过后，下载Nginx格式证书，解压后得到：
- xxx.pem（证书文件）
- xxx.key（私钥文件）

#### 3.2.3 上传到服务器

```bash
# 创建SSL目录
mkdir -p medication-assistant/docker/ssl

# 上传证书（使用scp或SFTP）
scp xxx.pem root@你的服务器IP:/root/medication-assistant/docker/ssl/cert.pem
scp xxx.key root@你的服务器IP:/root/medication-assistant/docker/ssl/key.pem

# 设置权限
chmod 600 medication-assistant/docker/ssl/key.pem
```

### 方法三：腾讯云免费证书

1. 登录腾讯云控制台
2. 进入"SSL证书" -> "我的证书"
3. 点击"申请免费证书"
4. 填写域名信息，选择DNS验证
5. 添加DNS记录
6. 下载Nginx证书

上传步骤同上。

## 第四步：配置Nginx

项目已包含Nginx配置文件，需要更新域名。

### 4.1 更新nginx.conf

```bash
cd medication-assistant

# 编辑nginx配置
vim docker/nginx.conf
```

找到并修改：
```nginx
server_name your-domain.com www.your-domain.com;  # 将your-domain.com替换为你的域名
```

### 4.2 验证配置

```bash
# 测试Nginx配置
docker-compose -f docker/docker-compose.yml config
```

## 第五步：部署服务

### 5.1 快速部署

```bash
cd medication-assistant

# 赋予脚本执行权限
chmod +x deploy.sh setup-domain.sh

# 运行部署脚本
./deploy.sh
```

### 5.2 交互式域名配置

如果你还没有SSL证书，可以使用交互式脚本：

```bash
# 运行域名配置向导（会自动申请Let's Encrypt证书）
./setup-domain.sh
```

脚本会：
1. 检查DNS解析
2. 自动申请Let's Encrypt证书
3. 配置Nginx
4. 启动服务

### 5.3 手动启动（已配置SSL）

```bash
# 设置API密钥
export DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxx"

# 构建镜像
docker-compose -f docker/docker-compose.yml build

# 启动服务
docker-compose -f docker/docker-compose.yml up -d

# 查看状态
docker-compose -f docker/docker-compose.yml ps
```

## 第六步：验证部署

### 6.1 检查服务状态

```bash
# 查看容器状态
docker-compose -f docker/docker-compose.yml ps

# 查看日志
docker-compose -f docker/docker-compose.yml logs -f
```

### 6.2 访问测试

打开浏览器访问：

- HTTPS：https://your-domain.com
- HTTP： http://your-domain.com（会自动跳转到HTTPS）

### 6.3 SSL证书验证

使用以下工具检查SSL配置：

1. **SSL Labs在线检测**
   - 访问：https://www.ssllabs.com/ssltest/
   - 输入你的域名
   - 查看评分和详细信息

2. **命令行检查**
   ```bash
   # 检查证书信息
   openssl s_client -connect your-domain.com:443 -servername your-domain.com

   # 查看证书详情
   echo | openssl s_client -connect your-domain.com:443 2>/dev/null | openssl x509 -noout -dates -issuer
   ```

## 常见问题

### Q1: DNS解析不生效怎么办？

**A**: DNS解析需要时间，通常5分钟-24小时。
- 清除本地DNS缓存：`ipconfig /flushdns`（Windows）或 `systemd-resolve --flush-caches`（Linux）
- 使用 `dig your-domain.com` 查看当前解析结果
- 确认A记录已正确添加

### Q2: Let's Encrypt证书申请失败？

**A**: 常见原因和解决方案：
- **域名未解析**：确保DNS已生效后再申请
- **防火墙阻止**：开放80和443端口
  ```bash
  ufw allow 80/tcp
  ufw allow 443/tcp
  ```
- **Nginx未停止**：如果80端口被占用，先停止相关服务

### Q3: HTTPS证书警告？

**A**: 可能原因：
- **证书不匹配**：检查nginx.conf中的域名是否正确
- **证书过期**：使用 `certbot renew` 续期
- **证书链不完整**：确保使用 fullchain.pem

### Q4: 如何强制HTTP跳转HTTPS？

**A**: 项目配置已默认启用强制跳转。如需手动配置，在nginx.conf中取消注释：
```nginx
return 301 https://$server_name$request_uri;
```

### Q5: SSL证书在哪续期？

**A**:
- **Let's Encrypt**：自动续期（已配置crontab）
- **阿里云/腾讯云**：登录控制台手动续期，或开启自动续期

## 成本总结

| 项目 | 推荐方案 | 费用 |
|------|---------|------|
| 域名 | 阿里云/腾讯云 | 35-55元/年 |
| 服务器 | 阿里云/腾讯云轻量应用服务器 | 30-50元/月 |
| SSL证书 | Let's Encrypt（免费） | 0元 |
| **总计** | | **约400-600元/年** |

## 下一步

配置完成后，你可以：

1. **配置防火墙**：只开放80和443端口
   ```bash
   ufw allow 22/tcp  # SSH
   ufw allow 80/tcp  # HTTP
   ufw allow 443/tcp # HTTPS
   ufw enable
   ```

2. **配置监控**：使用免费监控服务（如UptimeRobot）监控网站可用性

3. **备份配置**：定期备份docker目录和SSL证书

4. **性能优化**：根据需要调整Docker资源限制

## 获取帮助

如果遇到问题，可以：
- 查看Docker日志：`docker-compose logs`
- 检查Nginx状态：`docker-compose exec nginx nginx -t`
- 参考项目README.md
