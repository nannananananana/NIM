from openai import OpenAI
import os

client = OpenAI(
    base_url= os.getenv("BASE_URL_LLAMA","https://llama-baitong-nv-test-zlbkerxsmy.cn-shanghai.fcapp.run/v1"),
    api_key=os.getenv("API_KEY","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")
)

story_types = {
    "冒险": {
        "user_intro": "创造专属于你的冒险故事吧！",
        "model_prompt": "你是一位无畏的探险家，站在一个神秘洞穴的入口，准备进入未知的领域。"
    },
    "奇幻": {
        "user_intro": "进入魔法的世界，书写你的奇幻传奇！",
        "model_prompt": "你是一位年轻的魔法学徒，刚刚进入一片充满神秘生物的魔法森林。"
    },
    "科幻": {
        "user_intro": "穿越到未来的科技宇宙，探索未知星球的奥秘！",
        "model_prompt": "你是一位宇航员，刚刚登陆一颗未知的星球，四周都是奇怪的岩石和发光的植物。"
    },
    "悬疑": {
        "user_intro": "在悬疑的情境中解开一个个谜题，能否找到真相？",
        "model_prompt": "你是一位侦探，收到了一封神秘信件，信中隐藏着一个不为人知的秘密。"
    },
    "恐怖": {
        "user_intro": "勇敢进入恐怖的深渊，感受令人毛骨悚然的冒险！",
        "model_prompt": "夜晚来临，你独自在一座荒废的房子中，四周一片寂静，隐隐传来诡异的声响。"
    },
    "历史": {
        "user_intro": "穿越时空，体验古代的波澜壮阔！",
        "model_prompt": "你是一位古代的战士，站在即将开战的战场上，历史将因你而改变。"
    },
    "爱情": {
        "user_intro": "进入浪漫世界，书写属于你的爱情故事！",
        "model_prompt": "你在繁忙的城市中遇到一个陌生人，意想不到的浪漫即将发生。"
    },
    "神秘": {
        "user_intro": "探索神秘的未知世界，揭开深藏的秘密！",
        "model_prompt": "你来到一个小镇，发现每个居民都隐藏着一段秘密。"
    },
    "职场": {
        "user_intro": "进入职场风云，体验不一样的奋斗之旅！",
        "model_prompt": "你是一家跨国公司的新人，面临着复杂的人际关系和职场挑战。"
    },
    "禁忌": {
        "user_intro": "踏入禁忌之地，体验大胆刺激的冒险！",
        "model_prompt": "你被引入一个隐秘的社交圈，体验不为人知的冒险与诱惑。"
    }
}

def get_story_response(context, turn_count):
    # 根据回合数调整生成内容的提示
    if turn_count == 0:
        prompt = f"按照指示，生成故事内容：{context[0]}。回答保证使用中文"
    elif turn_count < 3:
        prompt = f"{context[-1]} 续写接下来会发生什么，回答保证使用中文，并且要求回答的内容要与前面的故事内容连贯"
    elif turn_count == 3:
        prompt = f"{context[-1]} 故事逐渐接近尾声，回答保证使用中文，并且要求回答的内容要与前面的故事内容连贯"
    else:
        prompt = f"{context[-1]} 给前面的故事写结局。回答保证使用中文"
    
    # 使用整个上下文作为消息传递给模型
    messages = [{"role": "user", "content": msg} for msg in context] + [{"role": "user", "content": prompt}]
    
    # 生成内容
    completion = client.chat.completions.create(
        model="meta/llama-3.1-8b-instruct",
        messages=messages,
        temperature=0.7,
        top_p=0.7,
        max_tokens=600,
        stream=True
    )
    
    response = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content
    return response
