import random
import time

# =========================
# 1. 定义20种卡牌模板（基于自然语义分析理论）
# =========================
card_templates = [
    {"name": "概念积累", "category": "accumulate", "effect": "积累观点清晰度", "clarity": 10},
    {"name": "语义催化", "category": "accumulate", "effect": "迅速提升观点清晰度", "clarity": 15},
    {"name": "定义强化", "category": "accumulate", "effect": "强化语境基础", "clarity": 8},
    {"name": "精确定义刃", "category": "attack", "effect": "以充分观点破防攻击", "base_damage": 20, "min_clarity": 20},
    {"name": "推理加速器", "category": "attack", "effect": "借助推理瞬发攻击", "base_damage": 15, "min_clarity": 15},
    {"name": "量化削弱器", "category": "attack", "effect": "削弱对手结构", "base_damage": 18, "min_clarity": 18},
    {"name": "逻辑悖论爆破", "category": "attack", "effect": "引发逻辑崩溃", "base_damage": 25, "min_clarity": 25},
    {"name": "论证推翻者", "category": "attack", "effect": "颠覆对手论证", "base_damage": 22, "min_clarity": 22},
    {"name": "语义催化剂", "category": "attack", "effect": "催化充能攻击", "base_damage": 19, "min_clarity": 19},
    {"name": "论证破局者", "category": "attack", "effect": "打破论证结构", "base_damage": 17, "min_clarity": 17},
    {"name": "隐喻剥离器", "category": "reduce_clarity", "effect": "剥离对手观点清晰度", "reduce": 10},
    {"name": "语用钳制器", "category": "reduce_clarity", "effect": "钳制对手语用能力", "reduce": 12},
    {"name": "概念澄清者", "category": "reduce_clarity", "effect": "澄清概念模糊", "reduce": 15},
    {"name": "对话扭转器", "category": "reduce_clarity", "effect": "扭转对话局势，降低对手观点清晰度", "reduce": 18},
    {"name": "逻辑扣除器", "category": "deduct", "effect": "扣除对手观点清晰度，不伤生命", "deduct": 20},
    {"name": "语境护盾", "category": "heal", "effect": "修复语境混乱", "heal": 10},
    {"name": "词汇精准化", "category": "heal", "effect": "净化表达混乱", "heal": 12},
    {"name": "参照修正器", "category": "heal", "effect": "重塑语义参照", "heal": 8},
    {"name": "定义重构器", "category": "heal", "effect": "重构表达体系", "heal": 15},
    {"name": "分析加持者", "category": "heal", "effect": "增强思辨恢复", "heal": 15},
]

# =========================
# 2. 构建卡组：30张牌；初始手牌10张
# =========================
deck = [random.choice(card_templates) for _ in range(30)]
random.shuffle(deck)
hand = deck[:10]
deck = deck[10:]

# =========================
# 3. 定义玩家与敌人的初始状态
# =========================
# 使用“观点清晰度”属性替换原来的蓄势（charge）
player_stats = {
    "health": 100,
    "clarity": 0,    # 观点清晰度
    "stun": 0
}

enemy_stats = {
    "health": 100,
    "clarity": 0,
    "stun": 0
}

enemy = {
    "name": "滑坡怪",
    "moves": [
        "这不道德！",
        "大家都这么认为！",
        "你这是攻击我！",
        "你自己也这样！"
    ]
}

# =========================
# 4. 辅助函数：显示手牌、选择卡牌、抽牌
# =========================
def display_hand():
    print("\n你的手牌：")
    for idx, card in enumerate(hand):
        print(f"{idx+1}: {card['name']} - {card['effect']}")

def pick_card():
    display_hand()
    while True:
        choice = input("请选择一张牌（输入数字）：")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(hand):
                return idx
        print("无效选择，请重新输入。")

def draw_card():
    global deck, hand
    if deck:
        new_card = deck.pop(0)
        hand.append(new_card)
        print(f"抽到新牌：{new_card['name']} - {new_card['effect']}")
    else:
        print("牌库已空。")

# =========================
# 5. 定义卡牌效果函数
# =========================
def play_card(card, actor_stats, opponent_stats, actor_label):
    print(f"\n{actor_label} 使用了『{card['name']}』 - {card['effect']}")
    if card["category"] == "accumulate":
        actor_stats["clarity"] += card["clarity"]
        print(f"{actor_label} 的观点清晰度增加 {card['clarity']} 点，当前清晰度：{actor_stats['clarity']}")
    elif card["category"] == "attack":
        if actor_stats["clarity"] < card["min_clarity"]:
            print(f"{actor_label} 的观点清晰度不足（当前 {actor_stats['clarity']}，需要 {card['min_clarity']}），攻击失败！轻微自损！")
            actor_stats["health"] -= 5
        else:
            exponent = (actor_stats["clarity"] - card["min_clarity"]) / card["min_clarity"]
            effective_damage = int(card["base_damage"] * (2 ** exponent))
            print(f"{actor_label} 以观点清晰度 {actor_stats['clarity']} 发动攻击，造成 {effective_damage} 点伤害！")
            opponent_stats["health"] -= effective_damage
            actor_stats["clarity"] = 0
    elif card["category"] == "reduce_clarity":
        reduction = card["reduce"]
        opponent_stats["clarity"] = max(opponent_stats["clarity"] - reduction, 0)
        print(f"{actor_label} 降低对手观点清晰度 {reduction} 点，对手当前清晰度：{opponent_stats['clarity']}")
    elif card["category"] == "deduct":
        deduction = card["deduct"]
        opponent_stats["clarity"] = max(opponent_stats["clarity"] - deduction, 0)
        print(f"{actor_label} 扣除对手观点清晰度 {deduction} 点，对手当前清晰度：{opponent_stats['clarity']}")
    elif card["category"] == "heal":
        actor_stats["health"] += card["heal"]
        print(f"{actor_label} 回复 {card['heal']} 点生命，当前生命：{actor_stats['health']}")

# =========================
# 6. 敌人回合（简单随机策略）
# =========================
def enemy_turn():
    if player_stats["stun"] > 0:
        print("[敌人被控制，无法出招！]")
        player_stats["stun"] -= 1
    else:
        move = random.choice(enemy["moves"])
        print(f"敌人 {enemy['name']} 使出话术：『{move}』")
        print("你感到观点受到冲击，生命 -10")
        player_stats["health"] -= 10

# =========================
# 7. 玩家回合函数
# =========================
def player_turn():
    if player_stats["stun"] > 0:
        print("你被控制，无法出牌！")
        player_stats["stun"] -= 1
        return
    idx = pick_card()
    card = hand.pop(idx)
    play_card(card, player_stats, enemy_stats, "你")
    if len(hand) < 10:
        draw_card()

# =========================
# 8. 状态显示函数
# =========================
def print_status():
    print(f"\n[你] 生命：{player_stats['health']}  观点清晰度：{player_stats['clarity']} | [敌人] 生命：{enemy_stats['health']}  观点清晰度：{enemy_stats['clarity']}")

# =========================
# 9. 主游戏循环
# =========================
def main():
    print("欢迎进入《观点清晰：语义战》 控制台原型")
    while player_stats["health"] > 0 and enemy_stats["health"] > 0:
        print_status()
        player_turn()
        time.sleep(1)
        if enemy_stats["health"] <= 0:
            break
        enemy_turn()
        time.sleep(1)
    print_status()
    if player_stats["health"] > 0:
        print("\n✅ 胜利！你守住了观点清晰！")
    else:
        print("\n❌ 失败！语言秩序混乱，敌人胜利。")

if __name__ == "__main__":
    main()

