#!/bin/bash
# 社区用药AI助手 - 停止服务脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🛑 停止服务..."
docker-compose -f docker/docker-compose.yml down

echo "✅ 服务已停止"
