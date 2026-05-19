# 社区用药AI助手

基于DeepSeek API的专业临床药学咨询助手，为社区居民提供安全、合理的用药指导。

## 🌟 功能特性

### 核心功能
- **智能用药咨询**：根据患者基本信息（年龄、体重、病史等）提供个性化用药建议
- **药物相互作用分析**：检查多种药物同时使用时的相互作用
- **配伍禁忌检查**：检查注射药物配伍、中西药联用等禁忌
- **常见病症推荐**：快速查询常见疾病的非处方药推荐
- **用药安全教育**：药物不良反应识别、特殊人群用药注意

### 专业背景
- 整合病理学、药理学、生理学知识
- 内置临床药学、药代动力学参数
- 药物相互作用高风险组合数据库
- 特殊人群（老年人、儿童、孕妇、肝肾功能不全）用药指南

## 🚀 快速开始

### 前置要求
- Docker & Docker Compose
- DeepSeek API密钥（获取地址：https://platform.deepseek.com/）

### 1. 配置API密钥

```bash
# 复制环境变量模板
cp docker/.env.example .env

# 编辑.env文件，填入您的API密钥
vim .env
```

或在运行前导出环境变量：
```bash
export DEEPSEEK_API_KEY="your-api-key-here"
```

### 2. 一键部署

```bash
# 赋予脚本执行权限
chmod +x deploy.sh stop.sh

# 运行部署脚本
./deploy.sh
```

### 3. 访问服务

部署成功后，访问以下地址：

| 服务 | 地址 |
|------|------|
| Web界面 | http://localhost:8000 |
| API文档 | http://localhost:8000/docs |

## 📁 项目结构

```
medication-assistant/
├── backend/
│   ├── main.py           # FastAPI主程序
│   ├── config.py        # 配置文件
│   ├── prompts.py       # 专业药学提示词
│   └── requirements.txt # Python依赖
├── frontend/
│   └── index.html       # Web界面
├── docker/
│   ├── Dockerfile        # Docker镜像配置
│   ├── docker-compose.yml # Docker Compose配置
│   ├── nginx.conf       # Nginx配置
│   └── .env.example     # 环境变量模板
├── deploy.sh            # 部署脚本
├── stop.sh              # 停止脚本
└── README.md            # 项目文档
```

## 🔧 API接口

### 聊天咨询
```bash
POST /api/chat
Content-Type: application/json

{
  "message": "头痛应该吃什么药？",
  "patient_info": {
    "age": 45,
    "gender": "male",
    "weight": 70,
    "allergies": "阿司匹林",
    "current_medications": ["降压药"]
  }
}
```

### 药物相互作用检查
```bash
POST /api/interaction-check
Content-Type: application/json

{
  "drugs": ["华法林", "阿司匹林", "布洛芬"],
  "patient_info": {...}
}
```

### 症状分析
```bash
POST /api/symptom-analysis
Content-Type: application/json

{
  "message": "发烧38.5度，伴有头痛",
  "patient_info": {...}
}
```

## 🔒 安全说明

### ⚠️ 免责声明
- 本助手仅提供健康教育和用药参考信息
- 不能替代执业医师或药师
- 严重症状或紧急情况请立即就医
- 处方药使用必须遵医嘱

### 生产环境建议
1. 设置`REQUIRE_API_KEY=true`启用API密钥验证
2. 使用Nginx配置HTTPS
3. 限制CORS来源域名
4. 配置防火墙规则
5. 定期更新依赖包

## 🐳 Docker命令参考

```bash
# 查看服务状态
docker-compose -f docker/docker-compose.yml ps

# 查看日志
docker-compose -f docker/docker-compose.yml logs -f

# 重启服务
docker-compose -f docker/docker-compose.yml restart

# 更新版本
docker-compose -f docker/docker-compose.yml pull
docker-compose -f docker/docker-compose.yml up -d --build

# 停止服务
./stop.sh
```

## 🌐 云服务器部署

### 阿里云/腾讯云部署步骤

1. **创建云服务器**
   - 选择Ubuntu 20.04 LTS或CentOS 7
   - 配置安全组：开放80、443端口

2. **安装Docker**
   ```bash
   curl -fsSL https://get.docker.com | sh
   sudo systemctl enable docker
   ```

3. **上传代码**
   ```bash
   scp -r medication-assistant user@server:/home/ubuntu/
   ```

4. **配置域名（可选）**
   - 在域名服务商添加A记录指向服务器IP
   - 申请SSL证书（Let's Encrypt免费）

5. **运行部署**
   ```bash
   cd medication-assistant
   chmod +x deploy.sh
   ./deploy.sh
   ```

## 📝 使用示例

### 示例1：用药咨询
```
用户：我母亲65岁，有高血压和糖尿病，最近有点头痛，可以吃布洛芬吗？

助手：根据您母亲的情况，使用布洛芬需要谨慎...
[详细分析和建议]
```

### 示例2：药物相互作用检查
```
药物组合：华法林 + 阿司匹林 + 布洛芬

分析结果：
⚠️ 严重相互作用
华法林与阿司匹林联用显著增加出血风险...
[详细说明和处理建议]
```

### 示例3：常见病症
```
症状：发烧38.5度，成人

建议：
1. 对乙酰氨基酚500-1000mg，每4-6小时一次（不超过4次/日）
2. 多喝温水，注意休息
3. 如持续高热超过3天，请就医
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 📞 联系方式

如有问题，请提交Issue。
