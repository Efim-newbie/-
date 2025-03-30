import random
import time
import math

# =========================
# 1. Define 20 card templates based on analytic natural language theory
# =========================
card_templates = [
    # Accumulation cards: increase clarity
    {"name": "Concept Accumulation", "category": "accumulate", "effect": "Accumulate clarity points", "clarity": 10},
    {"name": "Semantic Catalysis", "category": "accumulate", "effect": "Rapidly increase clarity", "clarity": 15},
    {"name": "Definition Enhancement", "category": "accumulate", "effect": "Strengthen foundational context", "clarity": 8},
    # Attack cards: require minimum clarity and deal exponential damage
    {"name": "Precise Definition Blade", "category": "attack", "effect": "Break defenses with accumulated clarity", "base_damage": 20, "min_clarity": 20},
    {"name": "Reasoning Accelerator", "category": "attack", "effect": "Launch an attack using accelerated reasoning", "base_damage": 15, "min_clarity": 15},
    {"name": "Quantitative Weakener", "category": "attack", "effect": "Weaken opponent’s structure", "base_damage": 18, "min_clarity": 18},
    {"name": "Logical Paradox Explosion", "category": "attack", "effect": "Cause a collapse in logic", "base_damage": 25, "min_clarity": 25},
    {"name": "Argument Overthrower", "category": "attack", "effect": "Overthrow the opponent’s argument", "base_damage": 22, "min_clarity": 22},
    {"name": "Semantic Catalyst", "category": "attack", "effect": "Catalyze an empowered attack", "base_damage": 19, "min_clarity": 19},
    {"name": "Argument Breaker", "category": "attack", "effect": "Disrupt the opponent’s argumentative structure", "base_damage": 17, "min_clarity": 17},
    # Reduce clarity cards: lower opponent's clarity
    {"name": "Metaphor Peeler", "category": "reduce_clarity", "effect": "Peel away opponent’s clarity", "reduce": 10},
    {"name": "Pragmatic Clamp", "category": "reduce_clarity", "effect": "Clamp down on opponent’s clarity", "reduce": 12},
    {"name": "Concept Clarifier", "category": "reduce_clarity", "effect": "Clarify conceptual vagueness", "reduce": 15},
    {"name": "Dialogue Reverser", "category": "reduce_clarity", "effect": "Turn the conversation to reduce opponent’s clarity", "reduce": 18},
    # Deduct clarity card: subtract clarity without affecting health
    {"name": "Logical Deductor", "category": "deduct", "effect": "Deduct opponent’s clarity without harming health", "deduct": 20},
    # Heal cards: restore health
    {"name": "Context Shield", "category": "heal", "effect": "Restore chaotic context", "heal": 10},
    {"name": "Vocabulary Precision", "category": "heal", "effect": "Refine chaotic expression", "heal": 12},
    {"name": "Reference Rectifier", "category": "heal", "effect": "Reshape semantic relationships", "heal": 8},
    {"name": "Definition Reconstructor", "category": "heal", "effect": "Reconstruct the expression system", "heal": 15},
    {"name": "Analytic Enhancer", "category": "heal", "effect": "Enhance analytical recovery", "heal": 15},
]

# =========================
# 2. Build the deck: 30 cards; initial hand: 10 cards
# =========================
deck = [random.choice(card_templates) for _ in range(30)]
random.shuffle(deck)
hand = deck[:10]
deck = deck[10:]

# =========================
# 3. Define initial state for player and enemy
# =========================
player_stats = {
    "health": 100,
    "clarity": 0,    # Clarity of opinion
    "stun": 0
}

enemy_stats = {
    "health": 100,
    "clarity": 0,
    "stun": 0
}

enemy = {
    "name": "The Slope Monster",
    "moves": [
        "This is unethical!",
        "Everyone thinks so!",
        "You're attacking me!",
        "You're doing the same!"
    ]
}

# =========================
# 4. Helper functions: display hand, pick card, draw card
# =========================
def display_hand():
    print("\nYour hand:")
    for idx, card in enumerate(hand):
        print(f"{idx+1}: {card['name']} - {card['effect']}")

def pick_card():
    display_hand()
    while True:
        choice = input("Please select a card (enter number): ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(hand):
                return idx
        print("Invalid choice, please try again.")

def draw_card():
    global deck, hand
    if deck:
        new_card = deck.pop(0)
        hand.append(new_card)
        print(f"Drew new card: {new_card['name']} - {new_card['effect']}")
    else:
        print("The deck is empty.")

# =========================
# 5. Card effect function
# =========================
def play_card(card, actor_stats, opponent_stats, actor_label):
    print(f"\n{actor_label} played '{card['name']}' - {card['effect']}")
    if card["category"] == "accumulate":
        actor_stats["clarity"] += card["clarity"]
        print(f"{actor_label}'s clarity increases by {card['clarity']} points. Current clarity: {actor_stats['clarity']}")
    elif card["category"] == "attack":
        if actor_stats["clarity"] < card["min_clarity"]:
            print(f"{actor_label}'s clarity is insufficient (Current: {actor_stats['clarity']}, Required: {card['min_clarity']}). Attack fails and incurs minor self-damage!")
            actor_stats["health"] -= 5
        else:
            exponent = (actor_stats["clarity"] - card["min_clarity"]) / card["min_clarity"]
            effective_damage = int(card["base_damage"] * (2 ** exponent))
            print(f"{actor_label} uses clarity {actor_stats['clarity']} to launch an attack, dealing {effective_damage} damage!")
            opponent_stats["health"] -= effective_damage
            actor_stats["clarity"] = 0
    elif card["category"] == "reduce_clarity":
        reduction = card["reduce"]
        opponent_stats["clarity"] = max(opponent_stats["clarity"] - reduction, 0)
        print(f"{actor_label} reduces opponent's clarity by {reduction} points. Opponent's clarity: {opponent_stats['clarity']}")
    elif card["category"] == "deduct":
        deduction = card["deduct"]
        opponent_stats["clarity"] = max(opponent_stats["clarity"] - deduction, 0)
        print(f"{actor_label} deducts {deduction} clarity points from the opponent. Opponent's clarity: {opponent_stats['clarity']}")
    elif card["category"] == "heal":
        actor_stats["health"] += card["heal"]
        print(f"{actor_label} heals {card['heal']} health points. Current health: {actor_stats['health']}")

# =========================
# 6. Enemy turn (simple random move)
# =========================
def enemy_turn():
    if player_stats["stun"] > 0:
        print("[The enemy is stunned and cannot act!]")
        player_stats["stun"] -= 1
    else:
        move = random.choice(enemy["moves"])
        print(f"The enemy {enemy['name']} uses a verbal move: '{move}'")
        print("You suffer 10 health damage due to the impact!")
        player_stats["health"] -= 10

# =========================
# 7. Player turn function
# =========================
def player_turn():
    if player_stats["stun"] > 0:
        print("You are stunned and cannot play a card!")
        player_stats["stun"] -= 1
        return
    idx = pick_card()
    card = hand.pop(idx)
    play_card(card, player_stats, enemy_stats, "You")
    if len(hand) < 10:
        draw_card()

# =========================
# 8. Status display function
# =========================
def print_status():
    print(f"\n[You] Health: {player_stats['health']} | Clarity: {player_stats['clarity']} || [Enemy] Health: {enemy_stats['health']} | Clarity: {enemy_stats['clarity']}")

# =========================
# 9. Main game loop
# =========================
def main():
    print("Welcome to 'Clarity of Opinion: Semantic Battle' (Console Edition)")
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
        print("\n✅ Victory! You maintained clarity of opinion!")
    else:
        print("\n❌ Defeat! The chaos of language has overwhelmed you.")

if __name__ == "__main__":
    main()
