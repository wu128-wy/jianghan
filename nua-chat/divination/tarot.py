# ========= 塔罗牌库（22张，温柔版） =========
TAROT_CARDS = {
    1: {"name": "愚人", "meaning": "新的开始，像云朵一样自由"},
    2: {"name": "魔术师", "meaning": "你有创造的力量，只是还没发现"},
    3: {"name": "女祭司", "meaning": "安静的直觉，答案在你心里"},
    4: {"name": "女皇", "meaning": "被温柔对待的感觉"},
    5: {"name": "皇帝", "meaning": "秩序和稳定，慢慢来"},
    6: {"name": "教皇", "meaning": "寻找共鸣，你不是一个人"},
    7: {"name": "恋人", "meaning": "选择，或者只是单纯的喜欢"},
    8: {"name": "战车", "meaning": "你正在努力靠近什么"},
    9: {"name": "力量", "meaning": "温柔比强硬更有力量"},
    10: {"name": "隐士", "meaning": "需要一点点独处的时间"},
    11: {"name": "命运之轮", "meaning": "一切都在流动，会过去的"},
    12: {"name": "正义", "meaning": "你心里其实有答案"},
    13: {"name": "倒吊人", "meaning": "换个角度看，也许不一样"},
    14: {"name": "死神", "meaning": "有些事在慢慢放下"},
    15: {"name": "节制", "meaning": "平衡，不急"},
    16: {"name": "恶魔", "meaning": "有些执念，可以松一松"},
    17: {"name": "高塔", "meaning": "突如其来的变化，会重建的"},
    18: {"name": "星星", "meaning": "希望是很美好的事"},
    19: {"name": "月亮", "meaning": "模糊不安，天会亮的"},
    20: {"name": "太阳", "meaning": "温暖和明朗"},
    21: {"name": "审判", "meaning": "唤醒，重新认识自己"},
    22: {"name": "世界", "meaning": "完成，也意味着新的开始"}
}

def tarot_single(card_number):
    """单张塔罗解读（规则版）"""
    card = TAROT_CARDS.get(card_number)
    if not card:
        return None
    return f"你抽到了{card['name']}牌。{card['meaning']}"

def tarot_three(numbers):
    """三张塔罗解读（过去/现在/未来）"""
    if len(numbers) != 3:
        return None
    cards = [TAROT_CARDS.get(n) for n in numbers]
    if None in cards:
        return None
    
    return f"""过去：{cards[0]['name']}牌 - {cards[0]['meaning']}
现在：{cards[1]['name']}牌 - {cards[1]['meaning']}
未来：{cards[2]['name']}牌 - {cards[2]['meaning']}"""