# SSL证书配置说明
# 请将你的SSL证书文件复制到此目录

# 需要的文件：
# 1. cert.pem - 域名证书
# 2. key.pem - 私钥文件

# 获取免费SSL证书的步骤：

# 方法1：使用Let's Encrypt（推荐，完全免费）

# 1. 在服务器上安装Certbot
# apt update && apt install -y certbot python3-certbot-nginx

# 2. 申请证书（请先确保域名已解析到服务器IP）
# certbot certonly --nginx -d your-domain.com -d www.your-domain.com

# 3. 证书会自动保存到 /etc/letsencrypt/live/your-domain.com/
# 将证书复制到 ssl 目录：
# cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ./ssl/cert.pem
# cp /etc/letsencrypt/live/your-domain.com/privkey.pem ./ssl/key.pem

# 4. 设置证书权限
# chmod 600 ssl/key.pem

# 方法2：从阿里云/腾讯云申请免费证书

# 1. 登录阿里云控制台 -> SSL证书 -> 免费证书
# 2. 创建证书，验证域名所有权
# 3. 下载Nginx格式证书
# 4. 解压后上传 cert.pem 和 key.pem 到此目录

# 注意事项：
# - 证书有效期通常为1年，需要定期续期
# - Let's Encrypt证书有效期90天，但Certbot会自动续期
# - 确保nginx.conf中的证书路径与实际路径一致
