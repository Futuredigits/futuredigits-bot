def calculate_passion_number(full_name: str) -> int:
    vowels = "AEIOUY"
    letter_values = {'A':1, 'E':5, 'I':9, 'O':6, 'U':3, 'Y':7}
    name = full_name.upper()
    total = sum(letter_values[ch] for ch in name if ch in vowels)

    def reduce_num(n):
        if n in {11, 22, 33}:
            return n
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n
    
    return reduce_num(total)


def get_passion_result(number: int) -> str:
    results = {
        1: "🔥 *Passion 1 – Driven by Independence*\n\nDeep within, you’re fueled by the desire to lead, create, and achieve on your own terms. "
           "You’re passionate about freedom, originality, and proving your strength to yourself. "
           "\n\n💫 *Your hidden key:* Trust your instincts. Every challenge awakens your true power.",
        2: "🌸 *Passion 2 – Longing for Harmony*\n\nYour deepest craving is emotional closeness, gentle connection, and meaningful partnerships. "
           "Your soul thrives when there is balance between you and the world around you."
           "\n\n💫 *Your hidden key:* Vulnerability is your strength — let love guide you.",
        3: "🎨 *Passion 3 – Expressive Heart*\n\nYour soul is restless for joy, art, and emotional freedom. "
           "You’re passionate about creativity, laughter, and making life more beautiful for yourself and others."
           "\n\n💫 *Your hidden key:* Express your truth without fear — it’s your superpower.",
        4: "🏛 *Passion 4 – Devotion to Stability*\n\nDeep down, you long for a strong foundation — security, loyalty, and meaningful work."
           "\n\n💫 *Your hidden key:* Discipline brings you freedom — build with love, not fear.",
        5: "🌍 *Passion 5 – Craving Freedom*\n\nYour hidden fire burns for adventure, change, and new experiences. "
           "\n\n💫 *Your hidden key:* Embrace the unknown — it’s where your true magic lives.",
        6: "💞 *Passion 6 – Desire to Love & Protect*\n\nDeep in your soul, you long to care for others and create harmony in your surroundings."
           "\n\n💫 *Your hidden key:* Love is your greatest motivator — but don’t forget yourself.",
        7: "🔮 *Passion 7 – Craving Wisdom*\n\nYou secretly long for deeper meaning, inner peace, and spiritual truth."
           "\n\n💫 *Your hidden key:* Your solitude is sacred — honor it.",
        8: "💼 *Passion 8 – Desire for Mastery*\n\nYour hidden fire is ambition, success, and personal power."
           "\n\n💫 *Your hidden key:* True success is when it uplifts others, not just you.",
        9: "🌈 *Passion 9 – Serving the Greater Good*\n\nYour soul is moved by compassion, creativity, and helping humanity."
           "\n\n💫 *Your hidden key:* When you give, you heal yourself.",
        11: "⚡ *Passion 11 – Awakener of Souls*\n\nYour passion lies in inspiring and elevating others with your light."
           "\n\n💫 *Your hidden key:* Embrace your sensitivity — it’s your gift.",
        22: "🏗 *Passion 22 – Master Builder*\n\nDeep down, you long to create something monumental and lasting."
           "\n\n💫 *Your hidden key:* Vision + discipline = legacy.",
        33: "🌟 *Passion 33 – Heart Teacher*\n\nYour secret fire is to heal, nurture, and teach through love."
           "\n\n💫 *Your hidden key:* Surrender to service — it’s your divine calling."
    }
    return results.get(number, "⚠️ Could not calculate Passion Number.")
