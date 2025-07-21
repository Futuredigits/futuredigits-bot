def calculate_soul_urge_number(name: str) -> int:
    name = name.upper()
    vowels = {'A': 1, 'E': 5, 'I': 9, 'O': 6, 'U': 3}

    total = sum(vowels.get(char, 0) for char in name if char in vowels)

    def reduce(n):
        if n in {11, 22, 33}:
            return n
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n

    return reduce(total)


def get_soul_urge_result(number: int) -> str:
    results = {
        1: "🔥 *Soul Urge 1 – Independent Spirit*\n\nYour heart craves leadership, freedom, and individuality. You're driven by a need to express your personal power and make bold choices. Confidence and courage define your soul's mission. 💪\n\nFollow your passion and let your inner fire lead the way.",
        2: "💗 *Soul Urge 2 – Harmonizer of Hearts*\n\nDeep down, you yearn for love, connection, and emotional balance. Cooperation and peace are your highest values. You're the emotional glue in relationships and friendships. 🌸\n\nLet your empathy shine — the world needs your heart.",
        3: "🎤 *Soul Urge 3 – Creative Heart*\n\nYour soul longs for joy, expression, and creative freedom. You feel most alive when sharing your voice, art, or ideas. 🌈\n\nUplift others by doing what you love. You were born to inspire.",
        4: "🏛 *Soul Urge 4 – Inner Foundation Builder*\n\nSecurity, order, and dedication bring you peace. Your soul desires to create a stable, lasting life — through patience, planning, and service. 🧱\n\nYou find joy in hard work and responsibility. Your roots run deep.",
        5: "🌍 *Soul Urge 5 – Craving for Freedom*\n\nYour soul resists limits. You’re driven by curiosity, experience, and freedom. Adventure, travel, and variety call you constantly. ✈️\n\nWhen you follow your truth, you unlock life’s richness.",
        6: "👪 *Soul Urge 6 – Devoted Caregiver*\n\nYou yearn to protect, love, and support others. Family, beauty, and responsibility are sacred to you. 💞\n\nYou are a natural nurturer — lead with compassion and grace.",
        7: "🔮 *Soul Urge 7 – Inner Seeker*\n\nYour soul longs for depth, mystery, and truth. You crave solitude, knowledge, and a spiritual connection to the universe. 🌌\n\nTrust your intuition — you're meant to uncover life’s secrets.",
        8: "💼 *Soul Urge 8 – Ambition Within*\n\nYou desire success, influence, and recognition. Your soul thrives when manifesting big visions and mastering the material world. 💰\n\nWhen aligned with purpose, you become unstoppable.",
        9: "🌈 *Soul Urge 9 – Humanitarian Heart*\n\nYou are deeply moved by compassion, art, and a desire to serve. You long to heal, teach, and uplift. 🌍\n\nLive with purpose, and your soul becomes light for others.",
        11: "⚡ *Soul Urge 11 – Inspired Messenger*\n\nYour heart beats for divine truth and spiritual awakening. You crave meaning, purpose, and the ability to uplift others. 🌠\n\nYour sensitivity is sacred — embrace your light.",
        22: "🏗 *Soul Urge 22 – Master Architect of Humanity*\n\nYou dream big — your soul wants to build something eternal. You feel responsible for using your gifts to serve the world. 🏛\n\nFocus and discipline unlock your destiny.",
        33: "🌟 *Soul Urge 33 – Sacred Teacher of Love*\n\nYour soul was born to love unconditionally and serve as a beacon for others. You're drawn to healing, teaching, and pure compassion. ✨\n\nYour heart is your power — share it fully."
    }

    text = results.get(number, "⚠️ An error occurred while calculating your Soul Urge Number.")
    return text + "\n\n🔓 *Want deeper insight? Try Personality or Destiny tools!*"
