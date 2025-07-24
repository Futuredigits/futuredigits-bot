def calculate_passion_number(full_name: str) -> int:
    """Calculate Passion Number using vowels in the name"""
    vowels = "AEIOUY"
    letter_values = {'A':1, 'E':5, 'I':9, 'O':6, 'U':3, 'Y':7}
    name = full_name.upper()
    total = sum(letter_values[ch] for ch in name if ch in vowels)

    def reduce_num(n):
        if n in {11, 22, 33}:  # Master numbers
            return n
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n

    return reduce_num(total)

def get_passion_number_result(number: int) -> str:
    results = {
        1: "🔥 *Passion Number 1 – Driven by Independence*\n\n"
           "Your hidden fire is self-expression and freedom. Deep inside, you crave to lead, create, and carve your own path in life. "
           "You are fueled by challenges and the thrill of doing what others say is impossible. ✨\n\n"
           "Your soul ignites when you trust your instincts and boldly step into your true power.",

        2: "🌸 *Passion Number 2 – Longing for Harmony*\n\n"
           "Your secret desire is emotional closeness and deep connections. You’re drawn to peace, balance, and meaningful relationships. "
           "Your soul thrives when you bring healing and harmony into the world. 💞\n\n"
           "Vulnerability is your strength, and love is your guiding force.",

        3: "🎨 *Passion Number 3 – Creative Expression*\n\n"
           "Your inner world is alive with color, imagination, and beauty. You are passionate about self-expression, art, and uplifting others. "
           "Your energy is contagious when you share your authentic self. 🌈\n\n"
           "When you express your truth, you awaken joy within yourself and others.",

        4: "🏛 *Passion Number 4 – Desire for Stability*\n\n"
           "Deep down, you long for security, loyalty, and creating something lasting. You are passionate about building strong foundations for yourself and those you love. 🧱\n\n"
           "Your soul finds peace through discipline and dedication, turning dreams into reality.",

        5: "🌍 *Passion Number 5 – Craving Freedom*\n\n"
           "Your soul burns for adventure, excitement, and change. You’re passionate about exploring new ideas, meeting new people, and embracing life’s unpredictable journey. ✈️\n\n"
           "Your true happiness lies in embracing the unknown and living fearlessly.",

        6: "💞 *Passion Number 6 – Desire to Love & Protect*\n\n"
           "You secretly long to care for, protect, and nurture others. Your soul craves harmony, beauty, and meaningful responsibility. 🌿\n\n"
           "Love is your greatest motivator, and through it, you find your deepest fulfillment.",

        7: "🔮 *Passion Number 7 – Craving Wisdom*\n\n"
           "Your inner fire is for knowledge, introspection, and spiritual truth. You long to uncover life’s deeper mysteries and understand the unseen forces guiding existence. 🕊️\n\n"
           "Your soul finds peace in solitude and sacred reflection.",

        8: "💼 *Passion Number 8 – Desire for Mastery*\n\n"
           "You are deeply motivated by success, power, and leaving a legacy. Your soul burns for achievement, influence, and creating abundance. 💰\n\n"
           "When you align ambition with purpose, you become unstoppable.",

        9: "🌈 *Passion Number 9 – Serving the Greater Good*\n\n"
           "Your secret desire is to uplift, inspire, and heal others. You crave compassion, creativity, and contributing to something larger than yourself. 🌍\n\n"
           "When you live from the heart, your soul shines brightest.",

        11: "⚡ *Passion Number 11 – Spiritual Awakener*\n\n"
            "Your deepest passion is to inspire and elevate others with your vision and sensitivity. You long to bring light into dark places and awaken hidden truths. 🌠\n\n"
            "Your intuition is your gift—embrace it fully.",

        22: "🏗 *Passion Number 22 – Master Builder*\n\n"
            "You secretly crave to build something monumental, something that outlasts you. Your soul longs to manifest big dreams and serve humanity on a grand scale. 🌐\n\n"
            "Your power lies in vision combined with discipline.",

        33: "🌟 *Passion Number 33 – Heart Teacher*\n\n"
            "Your ultimate desire is to heal and uplift the world through unconditional love. You are drawn to teaching, guiding, and being a beacon of compassion. ✨\n\n"
            "Your soul’s fulfillment lies in selfless service and love without limits.",
    }
    return results.get(number, "⚠️ Could not calculate Passion Number.")
