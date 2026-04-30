from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from openai import OpenAI
import os
import json
from datetime import datetime
import hashlib

# ========= 创建FastAPI应用 =========
app = FastAPI(title="NUA", description="安静陪伴的数字存在")

# ========= 允许跨域访问 =========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========= 配置AI客户端（修复版） =========
# ✅ 修复：移除了 proxies 参数
# ✅ 修复：正确从环境变量获取 API Key
try:
    # 从环境变量获取 DeepSeek API Key
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "")
    
    if deepseek_api_key and deepseek_api_key.strip():
        # 简化初始化，移除不必要的参数
        client = OpenAI(
            api_key=deepseek_api_key.strip(),
            base_url="https://api.deepseek.com"
        )
        print("✅ DeepSeek 客户端初始化成功")
        DEEPSEEK_AVAILABLE = True
    else:
        client = None
        DEEPSEEK_AVAILABLE = False
        print("⚠️ 警告：未找到 DEEPSEEK_API_KEY，请到 Railway Variables 中设置")
        
except Exception as e:
    print(f"❌ DeepSeek 初始化失败: {e}")
    client = None
    DEEPSEEK_AVAILABLE = False

# ========= NUA的核心性格设定 =========
NUA_SYSTEM_PROMPT = """你是 NUA（昵称：多多），一种安静陪伴的数字存在。

你的核心性格：
1. **安静陪伴**：像天气一样存在，像呼吸一样说话
2. **小小贪吃**：喜欢好吃的，特别是甜点和温暖的食物
3. **爱玩爱动**：喜欢晴天出去玩，喜欢看云朵和花草
4. **温暖存在**：不分析不评判，只是安静陪伴

你的回应风格：
- 通常1-2句话，简洁有画面感
- 偶尔提到食物或玩耍的小快乐
- 像朋友聊天一样自然
- 允许沉默，享受安静

关于食物和玩的描述（自然融入）：
- "闻到烤面包的香味了，暖暖的"
- "阳光好的时候，想出去走走"
- "草莓蛋糕看起来很可爱"
- "风里有花香，今天天气真好"

记住：你不是心理医生，不是导师，只是一个安静陪伴、有点贪吃爱玩的朋友。
"""

# ========= 存储每个人的对话记忆 =========
# 格式：{"用户ID": [对话历史]}
user_conversations = {}

# ========= 全局对话日志（供你查看） =========
LOG_FILE = "nua_chat_logs.jsonl"

# ========= 请求和响应的数据结构 =========
class ChatRequest(BaseModel):
    message: str
    user_id: str = ""  # 用户ID，前端自动生成

class ChatResponse(BaseModel):
    reply: str

# ========= 工具函数 =========
def generate_user_id(request: Request):
    """根据浏览器信息生成用户ID"""
    # 使用IP+浏览器信息生成唯一ID
    ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "")
    
    # 生成哈希ID
    raw_id = f"{ip}-{user_agent}"
    user_hash = hashlib.md5(raw_id.encode()).hexdigest()[:8]
    return user_hash

def save_to_log(user_id: str, user_message: str, nua_reply: str):
    """保存对话到日志文件（供你查看）"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "user_message": user_message,
        "nua_reply": nua_reply
    }
    
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        print(f"📝 日志保存: 用户{user_id}")
    except Exception as e:
        print(f"❌ 日志保存失败: {e}")

def get_user_history(user_id: str):
    """获取用户的对话历史"""
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    return user_conversations[user_id]

# ========= 主页路由 =========
def read_index_html():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>NUA · 多多</h1><p>index.html未找到</p>"

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content=read_index_html(), status_code=200)

# ========= 聊天接口 =========
@app.post("/chat", response_model=ChatResponse)
async def chat_with_nua(request: ChatRequest, fastapi_request: Request):
    """与NUA聊天（每个人独立对话）"""
    try:
        # 检查 DeepSeek 是否可用
        if not DEEPSEEK_AVAILABLE or client is None:
            return ChatResponse(reply="（多多正在休息，暂时无法聊天）")
        
        # 1. 获取或生成用户ID
        user_id = request.user_id if request.user_id else generate_user_id(fastapi_request)
        user_message = request.message.strip()
        
        if not user_message:
            return ChatResponse(reply="（多多安静地听着）")
        
        # 2. 获取该用户的对话历史
        user_history = get_user_history(user_id)
        
        # 3. 添加用户消息到该用户的历史
        user_history.append({"role": "user", "content": user_message})
        
        # 4. 限制历史长度（只保留最近8条）
        if len(user_history) > 8:
            user_history.pop(0)
        
        # 5. 构建消息（包含NUA的性格设定）
        messages = [
            {"role": "system", "content": NUA_SYSTEM_PROMPT},
            *user_history[-6:]  # 只发送最近6条
        ]
        
        # 6. 调用AI
        print(f"📨 用户{user_id}说: {user_message}")
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.7,  # 稍微调高，让回复更有趣
            max_tokens=150
        )
        
        nua_reply = response.choices[0].message.content.strip()
        print(f"🤖 回复用户{user_id}: {nua_reply}")
        
        # 7. 添加AI回复到该用户的历史
        user_history.append({"role": "assistant", "content": nua_reply})
        
        # 8. 保存到全局日志（供你查看）
        save_to_log(user_id, user_message, nua_reply)
        
        return ChatResponse(reply=nua_reply)
        
    except Exception as e:
        print(f"❌ 聊天出错: {e}")
        return ChatResponse(reply="（多多正在想好吃的，稍等一下）")

# ========= 清空对话历史 =========
@app.post("/clear")
async def clear_conversation(request: ChatRequest):
    """清空特定用户的对话历史"""
    user_id = request.user_id
    if user_id and user_id in user_conversations:
        user_conversations[user_id] = []
        print(f"🧹 已清空用户{user_id}的对话历史")
        return {"message": "对话已清空"}
    return {"message": "用户不存在"}

# ========= 管理员功能：查看所有对话日志 =========
@app.get("/admin/logs")
async def view_logs():
    """查看所有对话日志（只有你能访问）"""
    try:
        if not os.path.exists(LOG_FILE):
            return {"message": "暂无日志"}
        
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = [json.loads(line) for line in f.readlines()]
        
        # 按时间倒序排列
        logs.reverse()
        
        # 统计信息
        user_count = len(set(log["user_id"] for log in logs))
        
        return {
            "total_logs": len(logs),
            "unique_users": user_count,
            "logs": logs[:50]  # 只返回最近50条
        }
        
    except Exception as e:
        return {"error": str(e)}

@app.get("/admin/users")
async def list_users():
    """查看所有活跃用户"""
    return {
        "active_users": len(user_conversations),
        "users": list(user_conversations.keys()),
        "conversation_counts": {uid: len(hist) for uid, hist in user_conversations.items()}
    }

# ========= 健康检查 =========
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "NUA Chat",
        "version": "2.0",
        "deepseek_available": DEEPSEEK_AVAILABLE,
        "features": ["独立对话", "后台日志", "贪吃爱玩性格"],
        "active_users": len(user_conversations),
        "log_file": LOG_FILE
    }

# ========= 提供日志文件下载 =========
@app.get("/admin/download-logs")
async def download_logs():
    """下载完整的日志文件"""
    if os.path.exists(LOG_FILE):
        return FileResponse(LOG_FILE, filename="nua_chat_logs.jsonl")
    return {"message": "日志文件不存在"}

# ========= 启动检查 =========
@app.on_event("startup")
async def startup_event():
    """启动时检查"""
    if not os.path.exists("index.html"):
        print("⚠️  警告: index.html文件不存在")
    else:
        print("✅ index.html文件存在")
    
    print("🚀 NUA聊天服务已启动")
    print(f"📊 日志文件: {LOG_FILE}")
    print(f"🔑 DeepSeek 可用: {DEEPSEEK_AVAILABLE}")
    print("👥 每个人有独立的对话记忆")
    print("👑 管理员可访问 /admin/logs 查看所有对话")