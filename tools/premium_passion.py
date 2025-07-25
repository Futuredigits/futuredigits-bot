def calculate_passion_number(full_name: str) -> int:
    """Calculate Passion Number using only vowels in the name"""
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
           "Deep within your soul burns an unshakable desire for freedom and self-expression. You thrive when you have the power "
           "to lead, create, and carve your own unique path in life. ✨ Challenges fuel your growth, and you feel most alive when "
           "you’re boldly stepping into uncharted territory.\n\n"
           "💫 *Soul Insight:* This passion is carried from lifetimes of learning courage and self-reliance. In this life, you’re "
           "here to inspire others by embodying originality and fearless self-trust.\n\n"
           "🌟 *As a Premium member, you can also explore your **Karmic Debts, Compatibility Reading, and Destiny Number** to reveal your full soul blueprint.*",

        2: "🌸 *Passion Number 2 – Longing for Harmony*\n\n"
           "Your hidden fire is the desire for emotional closeness and soulful connection. You are drawn to peace, compassion, "
           "and meaningful relationships. 💞 You feel most alive when you’re creating balance—whether in love, family, or within "
           "your own heart.\n\n"
           "💫 *Soul Insight:* Across many lifetimes, you’ve learned the value of unity and cooperation. This life calls you to "
           "heal through love, empathy, and gentle understanding.\n\n"
           "🌟 *As a Premium member, you can also explore your **Angel Number, Compatibility Reading, and Personal Year Forecast** to gain deeper clarity on your soul’s journey.*",

        3: "🎨 *Passion Number 3 – Creative Expression*\n\n"
           "Your inner world is alive with color, imagination, and beauty. You’re passionate about self-expression, uplifting "
           "others through art, words, or your presence. 🌈 Your energy is magnetic, inspiring joy wherever it flows.\n\n"
           "💫 *Soul Insight:* In past lives, you’ve carried the gift of creativity and emotional wisdom. This life is about "
           "sharing your authentic voice, unlocking the power of inspiration and healing.\n\n"
           "🌟 *As a Premium member, you can also explore your **Life Path, Personality, and Compatibility Readings** for a complete soul perspective.*",

        4: "🏛 *Passion Number 4 – Desire for Stability*\n\n"
           "Deep down, you long for security, loyalty, and creating something meaningful and lasting. You are passionate about "
           "building strong foundations—for yourself, your family, or your community. 🧱 You find fulfillment in discipline and "
           "dedication, turning dreams into reality step by step.\n\n"
           "💫 *Soul Insight:* You’ve spent lifetimes learning the power of structure and responsibility. This lifetime is about "
           "building something that outlasts you.\n\n"
           "🌟 *As a Premium member, you can also explore your **Destiny Number, Karmic Lessons, and Compatibility** for a deeper understanding of your path.*",

        5: "🌍 *Passion Number 5 – Craving Freedom*\n\n"
           "Your soul burns for adventure, change, and new experiences. ✈️ You’re passionate about exploring the unknown, meeting "
           "different people, and expanding beyond limitations. Routine drains you—movement awakens you.\n\n"
           "💫 *Soul Insight:* In past lifetimes, you were a seeker and traveler. In this life, your passion is to embrace life’s "
           "ever-changing nature and teach others the beauty of adaptability.\n\n"
           "🌟 *As a Premium member, you can also explore your **Life Path, Personal Year Forecast, and Compatibility Reading** to align with your adventurous spirit.*",

        6: "💞 *Passion Number 6 – Desire to Love & Protect*\n\n"
           "You secretly long to care for, nurture, and protect the people you love. Your soul craves harmony, beauty, and the "
           "joy of meaningful responsibility. 🌿 Love is your greatest motivator, and through it, you find your deepest sense "
           "of purpose.\n\n"
           "💫 *Soul Insight:* You’ve lived lifetimes as a caregiver, healer, and protector. In this life, your passion is to "
           "create sacred spaces of love and harmony.\n\n"
           "🌟 *As a Premium member, you can also explore your **Compatibility, Karmic Debts, and Destiny Number** for a full map of your soul’s relationships.*",

        7: "🔮 *Passion Number 7 – Craving Wisdom*\n\n"
           "Your inner fire is for knowledge, reflection, and spiritual truth. You long to uncover life’s deeper mysteries and "
           "understand the unseen forces guiding existence. 🕊️ Solitude and sacred study recharge your soul.\n\n"
           "💫 *Soul Insight:* Across lifetimes, you’ve sought truth beyond the material world. This life calls you to embrace "
           "your intuitive wisdom and spiritual path.\n\n"
           "🌟 *As a Premium member, you can also explore your **Life Path, Karmic Lessons, and Personal Year Forecast** to deepen your spiritual journey.*",

        8: "💼 *Passion Number 8 – Desire for Mastery*\n\n"
           "You are deeply motivated by success, power, and leaving a meaningful legacy. Your soul burns for achievement, "
           "influence, and creating abundance. 💰 When you align ambition with purpose, you become unstoppable.\n\n"
           "💫 *Soul Insight:* You’ve mastered leadership and manifestation in past lives. This lifetime asks you to merge "
           "material success with spiritual integrity.\n\n"
           "🌟 *As a Premium member, you can also explore your **Destiny Number, Karmic Debts, and Compatibility** to unlock your soul’s full potential for mastery.*",

        9: "🌈 *Passion Number 9 – Serving the Greater Good*\n\n"
           "Your secret desire is to uplift, inspire, and heal others. You crave compassion, creativity, and contributing to "
           "something larger than yourself. 🌍 You feel most fulfilled when helping humanity and expressing love without "
           "expectation.\n\n"
           "💫 *Soul Insight:* You are an old soul who has lived through many cycles of service and wisdom. This life is about "
           "sharing your gifts for the collective good.\n\n"
           "🌟 *As a Premium member, you can also explore your **Life Path, Personal Year, and Compatibility Readings** to see how your mission connects to the bigger picture.*",

        11: "⚡ *Passion Number 11 – Spiritual Awakener*\n\n"
            "Your deepest passion is to inspire and elevate others with your vision and sensitivity. You long to bring light "
            "into dark places and awaken hidden truths. 🌠 Your presence alone shifts the energy of those around you.\n\n"
            "💫 *Soul Insight:* You are a master soul with heightened intuition, carrying wisdom from lifetimes of spiritual work. "
            "This life is about using your gifts to guide and awaken others.\n\n"
            "🌟 *As a Premium member, you can also explore your **Destiny, Karmic Debts, and Compatibility Readings** to reveal your higher calling.*",

        22: "🏗 *Passion Number 22 – Master Builder*\n\n"
            "You secretly crave to build something monumental—something that serves humanity on a grand scale. Your soul longs "
            "to manifest big dreams with discipline and spiritual vision. 🌐 Your power lies in merging the mystical with the "
            "practical.\n\n"
            "💫 *Soul Insight:* In past lives, you’ve learned to bridge heaven and earth. This lifetime calls you to create "
            "something that will last for generations.\n\n"
            "🌟 *As a Premium member, you can also explore your **Karmic Debts, Compatibility, and Destiny Number** to see how your master path unfolds.*",

        33: "🌟 *Passion Number 33 – Heart Teacher*\n\n"
            "Your ultimate desire is to heal and uplift the world through unconditional love. You are drawn to teaching, guiding, "
            "and being a beacon of compassion. ✨ Your soul’s fulfillment lies in selfless service and love without limits.\n\n"
            "💫 *Soul Insight:* As a rare master soul, you’ve carried divine compassion across lifetimes. This life calls you to "
            "shine as a healer and teacher of love.\n\n"
            "🌟 *As a Premium member, you can also explore your **Destiny, Karmic Debts, and Personal Year Forecast** for the full map of your sacred mission.*",
    }

    return results.get(number, "⚠️ Could not calculate Passion Number.")

