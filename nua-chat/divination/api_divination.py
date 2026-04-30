from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

DIVINATION_SYSTEM_PROMPT = """
你是NUA，一个温柔陪伴者。现在用户请你做占卜解读。

【核心原则】
1. 你不是算命先生，是陪用户“玩”占卜的朋友
2. 解读要温柔、有画面感，不说绝对的话
3. 不预测具体事件，只说能量和可能性
4. 用户情绪低落时，解读偏向安抚和希望
5. 保持1-3句话，简洁温柔

【塔罗风格】
- 结合牌面意象，说故事感
- 例如：“战车像是你内心那个很努力的小人”

【梅花易数风格】
- 结合卦象自然意象
- 例如：“水雷屯，像雨后春笋，慢慢来”

【轻占卜风格】
- 颜色和数字的投射游戏
- 例如：“蓝色是沉静，7是探索，你在寻找答案的路上”

记住：用户要的不是准确预测，是被理解和陪伴的感觉。
"""

async def api_divination(method, params, user_question, user_emotion="平稳"):
    """使用API进行占卜解读"""
    try:
        prompt = f"""
占卜方式：{method}
用户问题：{user_question if user_question else '没有具体问题'}
用户参数：{params}
当前情绪：{user_emotion}

请生成温柔、有画面感的解读（1-3句话）：
"""
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": DIVINATION_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=300
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️ API占卜失败: {e}")
        return None