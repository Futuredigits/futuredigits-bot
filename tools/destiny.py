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
        1: "🔥 *Destiny 1 – The Trailblazer*\n\nYour path is to lead with strength and boldness. You're meant to create your own way.",
        2: "🌸 *Destiny 2 – The Peacebringer*\n\nYour soul mission is harmony, partnership, and emotional intelligence.",
        3: "🎨 *Destiny 3 – The Inspirer*\n\nYou’re destined to bring joy through self-expression, creativity, and connection.",
        4: "🏗 *Destiny 4 – The Foundation Builder*\n\nYou’re here to build with stability, patience, and purpose.",
        5: "✈️ *Destiny 5 – The Freedom Seeker*\n\nYour journey involves growth through experience, adventure, and flexibility.",
        6: "💞 *Destiny 6 – The Guardian*\n\nYou’re here to uplift through service, family, and community care.",
        7: "🔮 *Destiny 7 – The Wisdom Seeker*\n\nYou’re destined to seek truth, knowledge, and inner awakening.",
        8: "💼 *Destiny 8 – The Power Architect*\n\nYou're here to master leadership, wealth, and personal authority.",
        9: "🌍 *Destiny 9 – The Global Healer*\n\nYou’re meant to serve, inspire, and lead with compassion.",
        11: "⚡ *Destiny 11 – The Illuminator*\n\nYou’re a spiritual guide, destined to uplift through wisdom and light.",
        22: "🏛 *Destiny 22 – The Master Visionary*\n\nYou are here to build powerful systems that uplift humanity.",
        33: "🌟 *Destiny 33 – The Divine Teacher*\n\nYou’re destined to love, heal, and serve with unconditional compassion."
    }

    text = results.get(number, "⚠️ An error occurred while calculating your Destiny Number.")
    return text + "\n\n🔓 *Want deeper insight? Try Expression or Destiny in Premium Tools!*"
