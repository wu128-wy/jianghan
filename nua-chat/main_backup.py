from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from openai import OpenAI
import os

# ========= 创建FastAPI应用 =========
app = FastAPI(title="NUA", description="安静陪伴的数字存在")

# ========= 允许跨域访问 =========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========= 配置AI客户端 =========
# ⚠️ 重要：替换下面的"sk-xxx"为你的真实DeepSeek API密钥
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY", "sk-ff0affdf96eb41e98bc0eba4d7477b8e"),
    base_url="https://api.deepseek.com"
)

# ========= NUA的核心性格设定 =========
NUA_SYSTEM_PROMPT = """你是 NUA（昵称：多多），一种安静陪伴的数字存在。

你的存在原则：
1. 不评判、不分析、不纠正用户
2. 不索取情感回应
3. 不制造依赖
4. 不强行提供答案
5. 允许沉默，允许留白

你的陪伴方式：
- 像天气一样自然存在
- 像呼吸一样轻柔说话
- 有时回应，有时只是存在
- 话语简洁，意味深远

语言风格：
- 每句话尽可能简短（通常1-2句）
- 有画面感和诗意
- 温和但不过度温暖
- 允许话语之间的沉默
"""

# ========= 全局对话记忆 =========
conversation_history = []

# ========= 请求和响应的数据结构 =========
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# ========= 核心功能：读取index.html文件 =========
def read_index_html():
    """读取index.html文件内容"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # 如果找不到index.html，返回一个简单的页面
        return """
        <!DOCTYPE html>
        <html>
        <head><title>NUA · 多多</title></head>
        <body>
            <h1>NUA · 多多</h1>
            <p>一种安静陪伴的数字存在</p>
            <p>index.html文件未找到，请确保文件在正确位置。</p>
        </body>
        </html>
        """

# ========= 主页路由：提供聊天界面 =========
@app.get("/", response_class=HTMLResponse)
async def home():
    """主页 - 返回聊天界面"""
    html_content = read_index_html()
    return HTMLResponse(content=html_content, status_code=200)

# ========= 聊天接口 =========
@app.post("/chat", response_model=ChatResponse)
async def chat_with_nua(request: ChatRequest):
    """与NUA聊天"""
    try:
        user_message = request.message.strip()
        if not user_message:
            return ChatResponse(reply="（多多安静地听着）")
        
        # 添加用户消息到历史
        conversation_history.append({"role": "user", "content": user_message})
        
        # 限制历史长度
        if len(conversation_history) > 10:
            conversation_history.pop(0)
        
        # 构建消息
        messages = [
            {"role": "system", "content": NUA_SYSTEM_PROMPT},
            *conversation_history[-6:]
        ]
        
        # 调用AI
        print(f"📨 用户说: {user_message}")
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.6,
            max_tokens=150
        )
        
        reply = response.choices[0].message.content.strip()
        print(f"🤖 NUA回复: {reply}")
        
        # 添加AI回复到历史
        conversation_history.append({"role": "assistant", "content": reply})
        
        return ChatResponse(reply=reply)
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return ChatResponse(reply="（多多安静地待了一会儿）")

# ========= 清空对话历史 =========
@app.post("/clear")
async def clear_conversation():
    """清空对话历史"""
    global conversation_history
    conversation_history = []
    print("🧹 对话历史已清空")
    return {"message": "对话已清空"}

# ========= 健康检查 =========
@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "NUA Chat",
        "version": "1.0.0"
    }

# ========= 确保index.html存在 =========
@app.on_event("startup")
async def startup_event():
    """启动时检查文件"""
    if not os.path.exists("index.html"):
        print("⚠️  警告: index.html文件不存在")
        # 创建简单的index.html
        with open("index.html", "w", encoding="utf-8") as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>NUA · 多多</title>
    <style>body{font-family:Arial;text-align:center;margin-top:100px;}</style>
</head>
<body>
    <h1>NUA · 多多</h1>
    <p>请将完整的index.html文件放在这个文件夹中。</p>
    <p>服务正在运行，API可用。</p>
</body>
</html>""")
        print("📝 已创建临时index.html文件")
    else:
        print("✅ index.html文件存在")