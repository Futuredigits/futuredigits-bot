from tools.expression import calculate_expression_number
from tools.birthday import calculate_birthday_number

def calculate_destiny_number(name: str, birthdate: str) -> int:
    name_number = calculate_expression_number(name)
    birth_number = calculate_birthday_number(birthdate)
    total = name_number + birth_number

    def reduce(n):
        if n in {11, 22, 33}:
            return n
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n

    return reduce(total)


def get_destiny_result(number: int) -> str:
    results = {
        1: "🔥 *Destiny 1 – The Independent Leader*\n\nYour destiny is to stand strong, lead with vision, and carve a unique path in life. You are here to develop courage, confidence, and self-reliance. The more you embrace your individuality and rise above fear, the more you awaken others to their own strength. You’re not just a leader — you’re a way-shower.",
        2: "🌸 *Destiny 2 – The Peaceful Unifier*\n\nYou are destined to bring harmony, balance, and compassion into the world. Your path is not forceful, but deeply powerful through patience, emotional intelligence, and divine timing. You serve as a bridge between hearts — a gentle guide in a chaotic world.",
        3: "🎨 *Destiny 3 – The Inspired Creator*\n\nYour purpose is to uplift through joy, beauty, and creative expression. Whether through art, writing, voice, or presence — you are here to awaken light in others. You inspire simply by being your authentic self. When you express your truth, you heal the world.",
        4: "🏗 *Destiny 4 – The Builder of Foundations*\n\nYou’re here to create systems, structures, and stability in a world that often lacks grounding. Through patience, hard work, and integrity, you bring form to dreams. Your path is one of mastery through discipline. You are the roots that allow others to rise.",
        5: "✈️ *Destiny 5 – The Evolutionary Explorer*\n\nYou are meant to grow through movement, freedom, and dynamic experiences. Life will push you into constant change — not to break you, but to help you expand. You’re here to liberate both yourself and others through bold living, flexibility, and truth-seeking.",
        6: "💞 *Destiny 6 – The Heart-Centered Healer*\n\nYour soul is called to uplift through love, responsibility, and deep emotional presence. You are destined to guide, protect, and harmonize families, communities, or those in need. Beauty, justice, and compassion are your tools. You are love in motion.",
        7: "🔮 *Destiny 7 – The Seeker of Truth*\n\nYou are here to explore the mysteries of life and self. Your destiny lies in introspection, spiritual study, and inner mastery. The solitude you crave is sacred — it allows you to hear wisdom others cannot. You carry deep insights that can awaken the collective mind.",
        8: "💼 *Destiny 8 – The Power Alchemist*\n\nYou are meant to master abundance, influence, and leadership in the material world. Your destiny involves building, managing, and empowering with integrity. True success for you lies in aligning vision with service — turning ambition into impact.",
        9: "🌍 *Destiny 9 – The Global Healer*\n\nYou are here to give, uplift, and inspire on a soul level. Yours is the path of compassion, emotional wisdom, and spiritual service. You will experience endings — but always to make room for greater love. When you live from the heart, your presence becomes transformative.",
        11: "⚡ *Destiny 11 – The Spiritual Lightbearer*\n\nYou are a messenger of divine insight. Your destiny is to illuminate the way for others — not through force, but through vibration, intuition, and inspired truth. You were born to awaken. Embrace your sensitivity — it is the gateway to your gift.",
        22: "🏛 *Destiny 22 – The Master Builder of Humanity*\n\nYou are capable of manifesting visions on a global scale. Your path combines spiritual insight with practical mastery. You are here to construct systems, communities, or movements that leave lasting impact. Discipline is your ally. The world awaits your design.",
        33: "🌟 *Destiny 33 – The Embodied Teacher of Love*\n\nYou are here to serve, heal, and uplift through pure compassion. Yours is a destiny of deep spiritual responsibility — to teach by example, to love without condition, and to channel divine wisdom through everyday acts. When you surrender to service, you become a living light."
    }


    text = results.get(number, "⚠️ An error occurred while calculating your Destiny Number.")
    return text + "\n\n🔓 *Want deeper insight? Try Expression or Destiny in Premium Tools!*"
