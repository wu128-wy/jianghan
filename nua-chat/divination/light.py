# ========= 颜色意象库 =========
COLOR_MEANINGS = {
    "红": "热情、行动力", "蓝": "沉静、思考", "黄": "明朗、希望",
    "绿": "生长、疗愈", "紫": "直觉、灵感", "粉": "温柔、爱意",
    "黑": "未知、深度", "白": "纯净、新开始", "橙": "活力、创造",
    "棕": "踏实、稳定"
}

# ========= 数字意象库 =========
NUMBER_MEANINGS = {
    1: "开始", 2: "平衡", 3: "创造", 4: "稳定",
    5: "变化", 6: "关怀", 7: "探索", 8: "力量",
    9: "完成", 10: "圆满"
}

def light_divination(color, number):
    """轻占卜解读（规则版）"""
    # 支持简写
    color_map = {"红":"红", "红色":"红", "蓝":"蓝", "蓝色":"蓝", "黄":"黄", "黄色":"黄"}
    color = color_map.get(color, color)
    
    color_meaning = COLOR_MEANINGS.get(color)
    number_meaning = NUMBER_MEANINGS.get(number)
    
    if not color_meaning or not number_meaning:
        return None
    
    main_trait = color_meaning.split('、')[0]
    return f"{color}是{color_meaning}的颜色，{number}是{number_meaning}的数字。也许你正处在「{main_trait}中{number_meaning}」的阶段。"