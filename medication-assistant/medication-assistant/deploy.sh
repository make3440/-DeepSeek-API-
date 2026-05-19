#!/bin/bash
# 社区用药AI助手 - 快速部署脚本

set -e

echo "========================================"
echo "  社区用药AI助手 - 部署脚本"
echo "========================================"

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: Docker未安装"
    echo "请先安装Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ 错误: Docker Compose未安装"
    echo "请先安装Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查API密钥
if [ -z "$DEEPSEEK_API_KEY" ]; then
    echo ""
    echo "⚠️  警告: 未设置DEEPSEEK_API_KEY环境变量"
    echo ""
    read -p "请输入您的DeepSeek API密钥: " API_KEY
    
    if [ -z "$API_KEY" ]; then
        echo "❌ 错误: API密钥不能为空"
        exit 1
    fi
    
    export DEEPSEEK_API_KEY="$API_KEY"
fi

echo ""
echo "📦 开始构建Docker镜像..."
docker-compose -f docker/docker-compose.yml build

echo ""
echo "🚀 启动服务..."
docker-compose -f docker/docker-compose.yml up -d

echo ""
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
if curl -f http://localhost:8000/ &> /dev/null; then
    echo ""
    echo "✅ 服务启动成功！"
    echo ""
    echo "📍 访问地址:"
    echo "   - API服务: http://localhost:8000"
    echo "   - API文档: http://localhost:8000/docs"
    echo "   - Web界面: http://localhost:8000"
    echo ""
    echo "📝 常用命令:"
    echo "   - 查看日志: docker-compose -f docker/docker-compose.yml logs -f"
    echo "   - 停止服务: docker-compose -f docker/docker-compose.yml down"
    echo "   - 重启服务: docker-compose -f docker/docker-compose.yml restart"
    echo ""
else
    echo ""
    echo "❌ 服务启动失败，请检查日志:"
    echo "   docker-compose -f docker/docker-compose.yml logs"
    exit 1
fi
