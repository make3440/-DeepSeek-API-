"""
社区用药AI助手 - 配置文件
请复制此文件并填入您的API密钥
"""

import os

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your-deepseek-api-key-here")  # 从环境变量读取或手动填写
DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")

# 服务器配置
HOST = "0.0.0.0"
PORT = 8000

# 日志配置
LOG_LEVEL = "INFO"

# 安全配置
API_KEY_HEADER = "X-API-Key"
REQUIRE_API_KEY = False
