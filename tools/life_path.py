def calculate_life_path_number(date_str: str) -> int:
    digits = [int(d) for d in date_str if d.isdigit()]
    total = sum(digits)

    def reduce_to_life_path(n):
        if n in {11, 22, 33}:
            return n
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n

    return reduce_to_life_path(total)


def get_life_path_result(number: int) -> str:
    descriptions = {
        1: "✨ *Life Path 1*: The Leader\nYou’re independent, driven, and destined to lead. Bold choices and new beginnings define your path.",
        2: "🤝 *Life Path 2*: The Peacemaker\nDiplomatic and intuitive, you're here to bring harmony and connection into the world.",
        3: "🎨 *Life Path 3*: The Creator\nExpressive, joyful, and full of imagination — you're meant to inspire and uplift others.",
        4: "🏗 *Life Path 4*: The Builder\nGrounded, disciplined, and practical. Your purpose is to create strong foundations.",
        5: "🌍 *Life Path 5*: The Adventurer\nYou crave freedom, variety, and new experiences. Change is your natural state.",
        6: "💞 *Life Path 6*: The Nurturer\nCompassionate and responsible — you're here to support, love, and bring beauty to others’ lives.",
        7: "🔮 *Life Path 7*: The Seeker\nSpiritual and analytical, your path is one of deep discovery, wisdom, and inner truth.",
        8: "💼 *Life Path 8*: The Powerhouse\nAmbitious and focused, you're here to master material success and lead with strength.",
        9: "🌈 *Life Path 9*: The Humanitarian\nEmpathetic and wise, you’re called to serve and uplift others with compassion.",
        11: "⚡ *Life Path 11*: The Visionary\nSpiritually gifted, intuitive, and inspiring — you’re meant to guide others through illumination.",
        22: "🏛 *Life Path 22*: The Master Builder\nYou hold the power to turn big dreams into reality with vision, structure, and persistence.",
        33: "🌟 *Life Path 33*: The Master Teacher\nSelfless, devoted, and wise — your soul mission is to heal and uplift humanity."
    }
    return descriptions.get(number, "An error occurred calculating your Life Path.")
