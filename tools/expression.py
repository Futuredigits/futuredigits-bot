def calculate_expression_number(name: str) -> int:
    name = name.upper()
    letters = {
        'A': 1, 'J': 1, 'S': 1,
        'B': 2, 'K': 2, 'T': 2,
        'C': 3, 'L': 3, 'U': 3,
        'D': 4, 'M': 4, 'V': 4,
        'E': 5, 'N': 5, 'W': 5,
        'F': 6, 'O': 6, 'X': 6,
        'G': 7, 'P': 7, 'Y': 7,
        'H': 8, 'Q': 8, 'Z': 8,
        'I': 9, 'R': 9
    }

    total = sum(letters.get(ch, 0) for ch in name if ch.isalpha())

    def reduce(n):
        if n in {11, 22, 33}:
            return n
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n

    return reduce(total)


def get_expression_result(number: int) -> str:
    results = {
        1: "🔥 *Expression 1 – The Pioneer*\n\nYou’re here to lead with originality and courage. You bring fresh ideas and independent thinking.",
        2: "🤝 *Expression 2 – The Diplomat*\n\nYou are supportive, intuitive, and a master of harmony. You’re here to build bridges.",
        3: "🎤 *Expression 3 – The Artist*\n\nYou’re creative, expressive, and magnetic. You're here to uplift through communication or art.",
        4: "🏗 *Expression 4 – The Organizer*\n\nYou’re practical, reliable, and structured. You bring order and lasting systems.",
        5: "🌍 *Expression 5 – The Explorer*\n\nYou’re dynamic, freedom-loving, and full of curiosity. You’re here to inspire change.",
        6: "💞 *Expression 6 – The Healer*\n\nYou’re nurturing, responsible, and loving. You bring people together with compassion.",
        7: "🧘 *Expression 7 – The Thinker*\n\nYou’re analytical, spiritual, and reflective. You’re here to seek deeper truths.",
        8: "💼 *Expression 8 – The Executive*\n\nYou’re ambitious, strategic, and influential. You're here to lead with power and integrity.",
        9: "🌟 *Expression 9 – The Visionary*\n\nYou’re compassionate, wise, and idealistic. You’re here to uplift and enlighten others.",
        11: "⚡ *Expression 11 – The Inspired Leader*\n\nYou’re intuitive, expressive, and spiritually gifted. You lead with divine insight.",
        22: "🏛 *Expression 22 – The Master Builder*\n\nYou’re capable of turning dreams into structures that serve the world. You hold great potential.",
        33: "🌟 *Expression 33 – The Master Teacher*\n\nYou’re selfless, artistic, and deeply loving. You’re here to guide and heal with higher purpose."
    }

    text = results.get(number, "⚠️ An error occurred while calculating your Expression Number.")
    return text + "\n\n🔓 *Want deeper insight? Try Expression or Destiny in Premium Tools!*"
