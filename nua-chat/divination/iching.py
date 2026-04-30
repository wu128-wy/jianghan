# ========= 八卦库 =========
BA_GUA = {
    1: {"name": "乾", "nature": "天", "image": "刚健", "meaning": "像天空一样开阔"},
    2: {"name": "兑", "nature": "泽", "image": "喜悦", "meaning": "喜悦，像湖水荡漾"},
    3: {"name": "离", "nature": "火", "image": "光明", "meaning": "热情，照亮"},
    4: {"name": "震", "nature": "雷", "image": "震动", "meaning": "唤醒，变化的前奏"},
    5: {"name": "巽", "nature": "风", "image": "入", "meaning": "随风潜入，慢慢渗透"},
    6: {"name": "坎", "nature": "水", "image": "险", "meaning": "流动，有时需要绕路"},
    7: {"name": "艮", "nature": "山", "image": "止", "meaning": "停下来看看风景"},
    8: {"name": "坤", "nature": "地", "image": "柔顺", "meaning": "承载和接纳"}
}

# ========= 64卦简易解读 =========
HEXAGRAM_MEANINGS = {
    (1,1): "乾为天：像天空一样开阔，无需着急",
    (2,2): "坤为地：承载和接纳，大地总是温柔的",
    (3,3): "震为雷：唤醒的时刻，改变在发生",
    (4,4): "巽为风：随风而行，顺势而为",
    (5,5): "坎为水：流动的水，总会找到出路",
    (6,6): "离为火：内心的热情，正在照亮什么",
    (7,7): "艮为山：停下来，看看风景",
    (8,8): "兑为泽：喜悦在心底荡漾",
    (1,2): "地天泰：安泰之时，一切顺遂",
    (2,1): "天地否：暂时的阻滞，会过去的",
    (5,3): "水雷屯：万事开头难，像雨后春笋",
    (3,5): "雷水解：困扰正在解开",
    (6,4): "火风鼎：更新，新的开始",
    (4,6): "风火家人：温暖的关系",
    (7,8): "山泽损：有时需要放下一些",
    (8,7): "泽山咸：心意相通的感觉",
}

def iching_divination(num1, num2):
    """梅花易数起卦（规则版）"""
    # 转换为1-8范围
    num1 = ((num1 - 1) % 8) + 1
    num2 = ((num2 - 1) % 8) + 1
    
    upper = BA_GUA.get(num1)
    lower = BA_GUA.get(num2)
    
    if not upper or not lower:
        return None
    
    hexagram_key = (num1, num2)
    hexagram = HEXAGRAM_MEANINGS.get(hexagram_key)
    
    if hexagram:
        return f"上卦{upper['name']}（{upper['nature']}），下卦{lower['name']}（{lower['nature']}）。{hexagram}"
    else:
        return f"上卦{upper['name']}（{upper['nature']}），下卦{lower['name']}（{lower['nature']}）。{upper['meaning']}，{lower['meaning']}"