from tools.expression import calculate_expression_number

def calculate_compatibility_score(name1: str, name2: str) -> int:
    num1 = calculate_expression_number(name1)
    num2 = calculate_expression_number(name2)
    
    # Simple compatibility metric: absolute difference
    diff = abs(num1 - num2)
    
    # Convert difference to a 1-100 score (smaller diff = higher compatibility)
    score = max(10, 100 - diff * 10)
    return score

def get_compatibility_result(score: int, name1: str, name2: str) -> str:
    if score > 80:
        vibe = "💖 *A deeply harmonious connection!*"
        meaning = f"{name1} and {name2} share a strong vibrational resonance. Your paths align beautifully, creating effortless chemistry and mutual growth."
    elif score > 60:
        vibe = "💞 *A balanced and supportive connection.*"
        meaning = f"Your bond has natural harmony with a few karmic lessons to enrich your journey. Respect and understanding will deepen your connection."
    elif score > 40:
        vibe = "⚖️ *A karmic connection with growth lessons.*"
        meaning = f"There’s attraction but also challenges that teach patience and balance. You are mirrors helping each other evolve."
    else:
        vibe = "🔥 *An intense but challenging connection.*"
        meaning = f"This bond sparks transformation but may feel turbulent. It’s here to awaken deeper self-awareness, even if it’s not forever."

    return (
        f"💑 *Compatibility Reading*\n\n"
        f"✨ *{name1} + {name2}*\n\n"
        f"📊 *Compatibility Score:* `{score}%`\n\n"
        f"{vibe}\n\n"
        f"{meaning}\n\n"
        f"💫 *Remember:* No connection is accidental. Each relationship is part of your soul’s evolution."
    )
