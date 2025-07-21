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
    1: "🔥 *Soul Urge 1 – Independent Spirit*\n\nDeep within, you crave to lead, achieve, and forge your own path. You’re driven by inner strength, personal freedom, and a desire to stand out. Your soul shines when you're taking initiative and turning ideas into action. 💪\n\nStay bold — you were born to be original.\n\n🔓 *Want deeper clarity? Try Personality or Destiny tools!*",
    2: "💗 *Soul Urge 2 – Peaceful Heart*\n\nAt your core, you long for harmony, connection, and emotional closeness. Your soul seeks balance in relationships and deep mutual understanding. Gentle, supportive, and intuitive — you’re the heart behind every peaceful solution. 🌸\n\nLet your kindness lead.\n\n🔓 *Want deeper clarity? Try Personality or Destiny tools!*",
    3: "🎨 *Soul Urge 3 – Expressive Dreamer*\n\nYour inner world is filled with color, emotion, and imagination. You feel most alive when expressing joy through words, art, or movement. The desire to inspire and uplift others is part of your soul’s design. 🌈\n\nSpeak your truth — your light is contagious.\n\n🔓 *Want deeper clarity? Try Personality or Destiny tools!*",
    4: "🏛 *Soul Urge 4 – Steady Builder*\n\nYour soul longs for structure, loyalty, and purposeful progress. Deep within, you desire to create something lasting — whether it's a home, a legacy, or a life built on truth and discipline. You thrive on responsibility and order. 🧱\n\nStay grounded — you bring strength to every space.\n\n🔓 *Want deeper clarity? Try Personality or Destiny tools!*",
    5: "🌍 *Soul Urge 5 – Freedom Seeker*\n\nRestless and curious, your soul craves movement, excitement, and change. You are deeply motivated by personal freedom, new experiences, and living life without constraints. ✈️\n\nWhen you follow your own rhythm, you light up the world.\n\n🔓 *Want deeper clarity? Try Personality or Destiny tools!*",
    6: "💞 *Soul Urge 6 – Compassionate Caregiver*\n\nYour deepest desire is to love, serve, and protect. Family, beauty, and harmony are sacred to you. You’re fulfilled when nurturing others and creating safe, loving spaces. 🌿\n\nYour soul is love in action — let it flow freely.\n\n🔓 *Want deeper clarity? Try Personality or Destiny tools!*",
    7: "🔮 *Soul Urge 7 – Truth Seeker*\n\nYou feel called to uncover life’s mysteries. Your soul yearns for inner peace, solitude, and the deeper meaning behind everything. Thoughtful, spiritual, and introspective — you thrive when exploring the unseen. 🌌\n\nTrust your inner voice — it holds your answers.\n\n🔓 *Want deeper clarity? Try Personality or Destiny tools!*",
    8: "💼 *Soul Urge 8 – Ambitious Heart*\n\nPower, achievement, and impact fuel your inner drive. Your soul craves mastery, influence, and the freedom that success brings. Business, leadership, and strategy come naturally to you. 💰\n\nEmbrace your ambition with purpose — it’s your gift.\n\n🔓 *Want deeper clarity? Try Personality or Destiny tools!*",
    9: "🌈 *Soul Urge 9 – Healer of the Heart*\n\nYou are deeply compassionate, with a soul longing to uplift, heal, and inspire. You feel most fulfilled when helping others, expressing beauty, or standing for a cause. 🌍\n\nYour empathy is your superpower — lead with love.\n\n🔓 *Want deeper clarity? Try Personality or Destiny tools!*",
    11: "⚡ *Soul Urge 11 – Sacred Messenger*\n\nYour soul is stirred by divine inspiration and higher purpose. You’re driven to awaken others through truth, art, or healing. Sensitivity is your strength — and spiritual connection is your core. 🌠\n\nYour light is meant to guide.\n\n🔓 *Want deeper clarity? Try Personality or Destiny tools!*",
    22: "🏗 *Soul Urge 22 – Master Visionary*\n\nYou dream of building something that truly matters. Your soul is called to create real-world change through discipline, vision, and service. When aligned, you become a powerful architect of destiny. 🌐\n\nBig purpose lives inside you.\n\n🔓 *Want deeper clarity? Try Personality or Destiny tools!*",
    33: "🌟 *Soul Urge 33 – Heart of a Teacher*\n\nYour soul is here to love, uplift, and bring light to others. You’re drawn to healing, teaching, and selfless service. The more you surrender to compassion, the more powerful you become. ✨\n\nLead with love — it's your divine gift.\n\n🔓 *Want deeper clarity? Try Personality or Destiny tools!*"
}

    text = results.get(number, "⚠️ An error occurred while calculating your Soul Urge Number.")
    return text + "\n\n🔓 *Want deeper insight? Try Personality or Destiny tools!*"
