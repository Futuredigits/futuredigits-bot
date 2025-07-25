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
        meaning = (
            f"The vibration between *{name1}* and *{name2}* is beautifully aligned — a bond built on mutual respect, "
            f"emotional understanding, and a shared sense of destiny. 🌸 This connection feels effortless, as if your souls "
            f"recognize each other beyond this lifetime.\n\n"
            f"Together, you amplify each other’s strengths while gently softening weaknesses. Challenges, if they appear, "
            f"will serve only as opportunities to deepen love and understanding.\n\n"
            f"This is a rare and sacred connection — passionate without chaos, stable without stagnation. You bring out "
            f"the highest potential in one another. 💫\n\n"
            f"🌟 *Soul Meaning:* Your souls likely share karmic harmony from past lives, reuniting now to support each "
            f"other’s spiritual evolution. This relationship is both a safe haven and a catalyst for growth."
        )

    elif score > 60:
        vibe = "💞 *A balanced and supportive connection.*"
        meaning = (
            f"*{name1}* and *{name2}* share a natural compatibility that brings both harmony and growth. Your connection "
            f"has a healthy balance of ease and lessons. 💐 There’s enough alignment to feel comfortable, but also just "
            f"enough difference to keep the relationship dynamic and evolving.\n\n"
            f"You’re likely to learn patience, understanding, and compromise with each other — but these lessons will "
            f"strengthen your bond over time.\n\n"
            f"💫 This is the kind of connection where two people meet as equals and help each other grow into better versions "
            f"of themselves.\n\n"
            f"🌟 *Soul Meaning:* Your relationship is guided by both harmony and karmic lessons — it’s meant to balance love "
            f"with growth, comfort with evolution."
        )

    elif score > 40:
        vibe = "⚖️ *A karmic connection with growth lessons.*"
        meaning = (
            f"This bond between *{name1}* and *{name2}* is magnetic yet layered with karmic energy. There’s attraction, "
            f"but also challenges that will push both of you to grow spiritually and emotionally. 🔥\n\n"
            f"Sometimes this relationship may feel intense or triggering, but it carries hidden gifts — showing you the parts "
            f"of yourself that need healing and understanding.\n\n"
            f"Such relationships can be deeply transformative, even if they are not always easy.\n\n"
            f"🌟 *Soul Meaning:* This is likely a karmic connection where your souls agreed to meet and evolve together, "
            f"even through discomfort and change."
        )

    else:
        vibe = "🔥 *An intense but challenging connection.*"
        meaning = (
            f"The energy between *{name1}* and *{name2}* is powerful but may feel unstable. This type of bond often brings "
            f"lessons rather than long-term harmony. 🌪️ It may feel like a rollercoaster of attraction, conflict, and deep "
            f"realizations.\n\n"
            f"While this connection can awaken you to hidden truths about yourself, it may require strong boundaries and "
            f"self-awareness to avoid burnout.\n\n"
            f"🌟 *Soul Meaning:* This relationship is a spiritual teacher, revealing what your soul needs to heal and release. "
            f"Sometimes, such connections are not meant to last, but to guide you toward a higher path."
        )

    return (
        f"💑 *Compatibility Reading*\n\n"
        f"✨ *{name1} + {name2}*\n\n"
        f"📊 *Compatibility Score:* `{score}%`\n\n"
        f"{vibe}\n\n"
        f"{meaning}\n\n"
        f"💫 *Remember:* No connection is accidental. Every relationship is part of your soul’s evolution.\n\n"
        f"🔓 *Want to go deeper? Try a **Premium Past-Life Compatibility Reading** to reveal hidden karmic ties and "
        f"future potential.*"
    )

