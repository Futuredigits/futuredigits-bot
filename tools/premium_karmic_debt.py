def calculate_karmic_debt_numbers(date_str: str) -> list:
    """
    Karmic Debt numbers in numerology are typically 13, 14, 16, and 19.
    We'll calculate all the important sums from the birthdate and check for karmic debts.
    """
    try:
        day, month, year = map(int, date_str.split('.'))
    except Exception:
        raise ValueError("Invalid date format. Use DD.MM.YYYY.")

    # Calculate important numerology components
    total_sum = day + month + sum(int(d) for d in str(year))

    def reduce_num(n):
        while n > 9 and n not in {11, 22, 33}:
            n = sum(int(d) for d in str(n))
        return n

    reduced_total = reduce_num(total_sum)

    # Numbers to check for karmic debts
    numbers_to_check = {day, month, total_sum, reduced_total}

    # Karmic Debt numbers are 13, 14, 16, 19
    karmic_numbers = [n for n in numbers_to_check if n in (13, 14, 16, 19)]
    return karmic_numbers


def get_karmic_debt_result(karmic_numbers: list) -> str:
    """
    Return deep premium-level meaning for each karmic debt number found.
    """
    explanations = {
        13: "⚠️ *Karmic Debt 13 – Lesson of Discipline*\n\n"
            "In a past life, you may have avoided responsibility or resisted steady effort. "
            "This lifetime asks you to embrace patience, persistence, and work ethic. 🌱 "
            "Avoid shortcuts and learn the power of building step by step.",

        14: "⚠️ *Karmic Debt 14 – Lesson of Control*\n\n"
            "You may have misused freedom or indulged in excess in previous lifetimes. "
            "This life teaches moderation, balance, and the mastery of your impulses. ✨ "
            "Freedom is found through inner discipline.",

        16: "⚠️ *Karmic Debt 16 – Lesson of Ego & Humility*\n\n"
            "Past lifetimes may have included pride, vanity, or misuse of love. "
            "This life brings sudden awakenings to humble you and open your heart. 🌌 "
            "Spiritual growth is your ultimate path.",

        19: "⚠️ *Karmic Debt 19 – Lesson of Independence*\n\n"
            "You may have misused power or avoided self-reliance in past incarnations. "
            "This life challenges you to stand on your own, build resilience, and lead with integrity. 🕊️"
    }

    if not karmic_numbers:
        return (
            "✨ *No major Karmic Debts found!*\n\n"
            "Your birthdate does not carry the heavy karmic lessons of 13, 14, 16, or 19. "
            "This suggests a smoother soul path, with more freedom to create new experiences. 🌟"
        )

    # Combine all karmic debt meanings
    result_parts = ["🔮 *Your Karmic Debt Analysis*:\n"]
    for n in karmic_numbers:
        result_parts.append(explanations[n])

    result_parts.append("\n💫 *Remember:* Karmic Debts are not punishments—they are opportunities for soul growth.")
    return "\n\n".join(result_parts)
