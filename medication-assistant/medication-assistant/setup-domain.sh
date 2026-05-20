#!/bin/bash
# 社区用药AI助手 - 域名配置脚本
# 支持自动申请Let's Encrypt免费SSL证书

set -e

echo "========================================"
echo "  社区用药AI助手 - 域名配置向导"
echo "========================================"
echo ""

# 检查是否以root权限运行
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  建议使用root权限运行以获得最佳体验"
    echo ""
fi

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: Docker未安装"
    echo "请先安装Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# 欢迎信息
echo "📋 域名配置步骤："
echo "  1. 配置DNS解析（在你的域名提供商处设置）"
echo "  2. 申请SSL证书（Let's Encrypt免费）"
echo "  3. 配置Nginx"
echo "  4. 启动服务"
echo ""

# 询问域名
read -p "请输入您的域名（如：example.com）: " DOMAIN

if [ -z "$DOMAIN" ]; then
    echo "❌ 错误: 域名不能为空"
    exit 1
fi

echo ""
echo "✅ 域名设置: $DOMAIN"
echo ""

# 检查DNS解析
echo "🔍 正在检查DNS解析..."
SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s icanhazip.com 2>/dev/null)
DOMAIN_IP=$(dig +short $DOMAIN 2>/dev/null | tail -1 || nslookup $DOMAIN 2>/dev/null | grep Address | tail -1 | awk '{print $2}')

if [ "$SERVER_IP" = "$DOMAIN_IP" ]; then
    echo "✅ DNS解析正确，域名已指向本服务器 ($SERVER_IP)"
elif [ -z "$DOMAIN_IP" ]; then
    echo "⚠️  警告: 无法获取域名DNS记录"
    echo "   请确保已在域名提供商处添加A记录指向 $SERVER_IP"
    read -p "是否继续？ (y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        exit 0
    fi
else
    echo "⚠️  警告: DNS解析可能不正确"
    echo "   服务器IP: $SERVER_IP"
    echo "   域名IP: $DOMAIN_IP"
    echo "   请检查DNS设置"
    read -p "是否继续？ (y/N): " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        exit 0
    fi
fi

# 更新nginx配置
echo ""
echo "📝 更新Nginx配置..."
sed -i "s/your-domain.com/$DOMAIN/g" docker/nginx.conf
echo "✅ Nginx配置已更新"

# 检查是否已有SSL证书
if [ -f "docker/ssl/cert.pem" ] && [ -f "docker/ssl/key.pem" ]; then
    echo ""
    echo "✅ 检测到已有SSL证书"
    USE_EXISTING=1
else
    echo ""
    echo "🔐 SSL证书配置"
    echo "  1. 自动申请Let's Encrypt免费证书（推荐）"
    echo "  2. 使用阿里云/腾讯云免费证书"
    echo "  3. 稍后手动配置"
    read -p "请选择证书配置方式 (1/2/3): " CERT_OPTION

    case $CERT_OPTION in
        1)
            echo ""
            echo "🔄 正在安装Certbot..."
            apt update && apt install -y certbot python3-certbot-nginx

            echo ""
            echo "🔄 正在申请Let's Encrypt证书..."
            certbot certonly --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos -m admin@$DOMAIN

            if [ -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
                echo ""
                echo "📦 复制证书到项目目录..."
                mkdir -p docker/ssl
                cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem docker/ssl/cert.pem
                cp /etc/letsencrypt/live/$DOMAIN/privkey.pem docker/ssl/key.pem
                chmod 600 docker/ssl/key.pem
                echo "✅ 证书配置完成"

                # 设置自动续期
                echo ""
                echo "⏰ 配置证书自动续期..."
                (crontab -l 2>/dev/null; echo "0 0 * * * certbot renew --quiet && docker-compose -f $SCRIPT_DIR/docker/docker-compose.yml restart nginx") | crontab -
                echo "✅ 自动续期已配置（每天0点检查）"
            else
                echo "❌ 证书申请失败，请检查域名解析"
                exit 1
            fi
            ;;
        2)
            echo ""
            echo "📥 请下载阿里云/腾讯云的Nginx格式证书"
            echo "   然后将 cert.pem 和 key.pem 复制到 docker/ssl/ 目录"
            echo ""
            read -p "按回车键继续..."
            ;;
        *)
            echo ""
            echo "⚠️  跳过SSL证书配置"
            echo "   请稍后手动配置证书，然后运行 docker-compose up -d"
            USE_EXISTING=0
            ;;
    esac
fi

# 检查API密钥
if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo ""
    echo "🔑 DeepSeek API密钥配置"
    read -p "请输入您的DeepSeek API密钥: " API_KEY

    if [ -z "$API_KEY" ]; then
        echo "❌ 错误: API密钥不能为空"
        exit 1
    fi

    export DEEPSEEK_API_KEY="$API_KEY"
fi

# 部署服务
echo ""
echo "🚀 开始部署服务..."

# 停止旧服务（如果存在）
docker-compose -f docker/docker-compose.yml down 2>/dev/null || true

# 构建并启动
docker-compose -f docker/docker-compose.yml build
docker-compose -f docker/docker-compose.yml up -d

# 等待服务启动
echo ""
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
if curl -f https://$DOMAIN/ &>/dev/null; then
    echo ""
    echo "========================================"
    echo "  ✅ 部署成功！"
    echo "========================================"
    echo ""
    echo "📍 访问地址:"
    echo "   - HTTPS: https://$DOMAIN"
    echo "   - HTTP:  http://$DOMAIN"
    echo ""
    echo "📝 后续操作:"
    echo "   - 查看日志: docker-compose -f docker/docker-compose.yml logs -f"
    echo "   - 停止服务: docker-compose -f docker/docker-compose.yml down"
    echo "   - 重启服务: docker-compose -f docker/docker-compose.yml restart"
    echo ""
    echo "🔒 SSL证书会自动在到期前续期"
    echo ""
else
    echo ""
    echo "⚠️  服务可能未正常启动，请检查日志:"
    echo "   docker-compose -f docker/docker-compose.yml logs"
    exit 1
fi
