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
    explanations = {
        13: "⚠️ *Karmic Debt 13 – Lesson of Discipline*\n\n"
            "In a past life, you may have avoided responsibility or sought shortcuts instead of steady effort. "
            "This lifetime asks you to embrace patience, persistence, and the sacred art of building step by step. 🌱 "
            "True freedom comes from mastering consistency.\n\n"
            "💫 *Soul Insight:* This is not a punishment — it’s a chance to finally complete the work your soul once avoided.",

        14: "⚠️ *Karmic Debt 14 – Lesson of Control*\n\n"
            "In previous lives, you may have misused freedom, indulged in excess, or resisted limits. "
            "Now you’re learning moderation, balance, and the power of self-mastery. ✨ "
            "Freedom is no longer about escape — it’s about conscious choice.\n\n"
            "💫 *Soul Insight:* By balancing desire with wisdom, you unlock the highest potential of this vibration.",

        16: "⚠️ *Karmic Debt 16 – Lesson of Ego & Humility*\n\n"
            "This number signals past lifetimes marked by pride, vanity, or misuse of love. "
            "This life brings awakening moments that humble you, guiding you toward deeper compassion. 🌌 "
            "Spiritual truth replaces illusion here.\n\n"
            "💫 *Soul Insight:* This is a sacred invitation to dissolve ego and reconnect to higher wisdom.",

        19: "⚠️ *Karmic Debt 19 – Lesson of Independence*\n\n"
            "In other lifetimes, you may have misused power or relied too heavily on others. "
            "Now you’re learning self-reliance, integrity, and the strength to lead yourself. 🕊️ "
            "This is about owning your power without domination.\n\n"
            "💫 *Soul Insight:* This path frees you from old patterns of dependence and teaches true empowerment."
    }

    if not karmic_numbers:
        return (
            "✨ *No Major Karmic Debts Found!*\n\n"
            "Your birthdate carries a lighter spiritual contract. 🌿 You’ve already resolved many of your past-life "
            "obligations, meaning this lifetime is more about creation than correction.\n\n"
            "💫 *Soul Insight:* You’re free to build new experiences without being bound by old karmic ties — a rare gift "
            "that allows more effortless alignment with your destiny.\n\n"
            "🔓 *Want a full karmic past-life map? Try the **Premium Soul Contract Reading**.*"
        )

    # Combine all karmic debt meanings
    result_parts = ["🔮 *Your Karmic Debt Analysis*:\n"]
    for n in karmic_numbers:
        result_parts.append(explanations[n])

    result_parts.append(
        "\n💫 *Remember:* Karmic Debts are not punishments — they are opportunities for your soul to heal, evolve, "
        "and complete old cycles.\n\n"
        "🔓 *Want to explore these karmic lessons in detail? Try the **Premium Past-Life Karmic Healing Reading**.*"
    )
    return "\n\n".join(result_parts)


