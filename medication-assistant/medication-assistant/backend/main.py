"""
社区用药AI助手 - FastAPI后端服务
接入DeepSeek API，提供专业药学咨询
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import httpx
import json
import logging
import os
import traceback
from datetime import datetime

# 导入配置和提示词
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_BASE, REQUIRE_API_KEY, API_KEY_HEADER
from prompts import SYSTEM_PROMPT, PATIENT_INFO_TEMPLATE

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="社区用药AI助手",
    description="基于DeepSeek API的专业临床药学咨询助手",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class Message(BaseModel):
    role: str = Field(default="user", description="角色: user 或 assistant")
    content: str = Field(description="消息内容")

class PatientInfo(BaseModel):
    """患者基本信息"""
    age: Optional[int] = Field(None, description="年龄")
    gender: Optional[str] = Field(None, description="性别: male/female")
    weight: Optional[float] = Field(None, description="体重(kg)")
    height: Optional[float] = Field(None, description="身高(cm)")
    allergies: Optional[str] = Field(None, description="过敏史")
    medical_history: Optional[List[str]] = Field(default_factory=list, description="既往病史")
    current_medications: Optional[List[str]] = Field(default_factory=list, description="当前用药")
    liver_function: Optional[str] = Field(None, description="肝功能")
    kidney_function: Optional[str] = Field(None, description="肾功能")
    pregnancy_status: Optional[str] = Field(None, description="妊娠状态")

class ChatRequest(BaseModel):
    """聊天请求"""
    message: str = Field(description="用户消息")
    patient_info: Optional[PatientInfo] = Field(None, description="患者信息")
    conversation_history: Optional[List[Message]] = Field(default_factory=list, description="对话历史")

class ChatResponse(BaseModel):
    """聊天响应"""
    response: str = Field(description="AI回复")
    tokens_used: Optional[int] = Field(None, description="使用的token数量")

class InteractionCheckRequest(BaseModel):
    """药物相互作用检查请求"""
    drugs: List[str] = Field(description="要检查的药物列表")
    patient_info: Optional[PatientInfo] = Field(None, description="患者信息")

class InteractionCheckResponse(BaseModel):
    """药物相互作用检查响应"""
    analysis: str = Field(description="相互作用分析结果")

# API密钥验证（可选）
async def verify_api_key(request: Request):
    if REQUIRE_API_KEY:
        api_key = request.headers.get(API_KEY_HEADER)
        if not api_key or api_key != os.getenv("APP_API_KEY"):
            raise HTTPException(status_code=401, detail="无效的API密钥")

def build_patient_context(patient_info: Optional[PatientInfo]) -> str:
    """构建患者信息上下文"""
    if not patient_info:
        return ""
    
    context_parts = ["\n\n【患者基本信息】"]
    
    if patient_info.age:
        context_parts.append(f"- 年龄：{patient_info.age}岁")
    if patient_info.gender:
        gender_map = {"male": "男", "female": "女"}
        context_parts.append(f"- 性别：{gender_map.get(patient_info.gender, patient_info.gender)}")
    if patient_info.weight:
        context_parts.append(f"- 体重：{patient_info.weight}kg")
    if patient_info.height:
        context_parts.append(f"- 身高：{patient_info.height}cm")
    if patient_info.allergies:
        context_parts.append(f"- 过敏史：{patient_info.allergies}")
    if patient_info.medical_history:
        context_parts.append(f"- 既往病史：{', '.join(patient_info.medical_history)}")
    if patient_info.current_medications:
        context_parts.append(f"- 当前用药：{', '.join(patient_info.current_medications)}")
    if patient_info.liver_function:
        context_parts.append(f"- 肝功能：{patient_info.liver_function}")
    if patient_info.kidney_function:
        context_parts.append(f"- 肾功能：{patient_info.kidney_function}")
    if patient_info.pregnancy_status:
        context_parts.append(f"- 妊娠状态：{patient_info.pregnancy_status}")
    
    return "\n".join(context_parts) + "\n"

async def call_deepseek(messages: List[Dict], max_tokens: int = 2000) -> Dict:
    """调用DeepSeek API"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.3,  # 较低温度以保持专业性和一致性
        "stream": False
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{DEEPSEEK_API_BASE}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            return {
                "content": result["choices"][0]["message"]["content"],
                "tokens": result.get("usage", {}).get("total_tokens", 0)
            }
    except httpx.HTTPStatusError as e:
        logger.error(f"DeepSeek API HTTP错误: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail="AI服务请求失败")
    except Exception as e:
        logger.error(f"DeepSeek API调用错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI服务调用失败: {str(e)}")

# API路由
@app.get("/")
async def root():
    """健康检查"""
    return {
        "status": "online",
        "service": "社区用药AI助手",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/info")
async def get_info():
    """获取服务信息"""
    return {
        "name": "社区用药AI助手",
        "description": "基于DeepSeek API的专业临床药学咨询助手",
        "features": [
            "用药咨询与建议",
            "药物相互作用分析",
            "配伍禁忌检查",
            "用药安全教育",
            "常见病症推荐"
        ],
        "disclaimer": "本服务仅供参考，不能替代执业医师或药师。如有紧急情况，请立即就医。"
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, req: Request):
    """主聊天接口"""
    await verify_api_key(req)
    
    # 构建消息列表
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # 添加患者信息上下文
    patient_context = build_patient_context(request.patient_info)
    if patient_context:
        messages.append({
            "role": "system",
            "content": f"请结合以下患者信息提供个性化建议：{patient_context}"
        })
    
    # 添加对话历史
    if request.conversation_history:
        for msg in request.conversation_history[-10:]:  # 限制历史长度
            messages.append({"role": msg.role, "content": msg.content})
    
    # 添加当前消息
    messages.append({"role": "user", "content": request.message})
    
    # 调用DeepSeek API
    result = await call_deepseek(messages)
    
    return ChatResponse(
        response=result["content"],
        tokens_used=result["tokens"]
    )

@app.post("/api/interaction-check", response_model=InteractionCheckResponse)
async def check_interactions(request: InteractionCheckRequest, req: Request):
    """药物相互作用检查接口"""
    await verify_api_key(req)
    
    patient_context = build_patient_context(request.patient_info)
    
    interaction_prompt = f"""
请分析以下药物组合的相互作用和配伍禁忌：

药物列表：{', '.join(request.drugs)}
{patient_context}

请提供：
1. 每对药物的相互作用描述
2. 临床意义评估（严重⚠️/中等⚡/轻微ℹ️）
3. 处理建议和替代方案（如需要）
4. 用药时机建议（如需间隔服用）

格式清晰，便于阅读。
"""
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": interaction_prompt}
    ]
    
    result = await call_deepseek(messages, max_tokens=3000)
    
    return InteractionCheckResponse(analysis=result["content"])

@app.post("/api/symptom-analysis")
async def symptom_analysis(request: ChatRequest, req: Request):
    """症状分析接口"""
    await verify_api_key(req)
    
    patient_context = build_patient_context(request.patient_info)
    
    symptom_prompt = f"""
请根据以下症状描述进行分析和建议：

症状：{request.message}
{patient_context}

请提供：
1. 可能的原因分析
2. 初步处理建议
3. 何时需要就医
4. 如需用药，请给出非处方药建议（包括药品名称、剂量、用法）
"""
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": symptom_prompt}
    ]
    
    result = await call_deepseek(messages, max_tokens=2500)
    
    return {"analysis": result["content"], "tokens_used": result["tokens"]}

@app.get("/api/patient-template")
async def get_patient_template():
    """获取患者信息收集模板"""
    return {
        "template": PATIENT_INFO_TEMPLATE,
        "fields": [
            {"name": "age", "label": "年龄", "type": "number", "required": True},
            {"name": "gender", "label": "性别", "type": "select", "options": ["男", "女"], "required": True},
            {"name": "weight", "label": "体重(kg)", "type": "number", "required": False},
            {"name": "height", "label": "身高(cm)", "type": "number", "required": False},
            {"name": "allergies", "label": "过敏史", "type": "text", "required": False},
            {"name": "medical_history", "label": "既往病史", "type": "multiselect", "options": ["高血压", "糖尿病", "心脏病", "肝病", "肾病", "哮喘", "胃溃疡"], "required": False},
            {"name": "current_medications", "label": "当前用药", "type": "text", "required": False},
            {"name": "liver_function", "label": "肝功能异常", "type": "select", "options": ["正常", "轻度异常", "中度异常", "重度异常"], "required": False},
            {"name": "kidney_function", "label": "肾功能异常", "type": "select", "options": ["正常", "轻度异常", "中度异常", "重度异常"], "required": False}
        ]
    }

# 错误处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"全局错误: {str(exc)}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"服务器内部错误: {str(exc)}"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
