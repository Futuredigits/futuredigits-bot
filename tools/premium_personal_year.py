import datetime

def calculate_personal_year_number(birthdate: str) -> int:
    try:
        day, month, year = map(int, birthdate.split('.'))
    except ValueError:
        raise ValueError("Invalid date format. Use DD.MM.YYYY.")
    
    current_year = datetime.date.today().year
    total = day + month + sum(int(d) for d in str(current_year))

    def reduce_num(n):
        while n > 9 and n not in (11, 22, 33):
            n = sum(int(d) for d in str(n))
        return n
    
    return reduce_num(total)


def get_personal_year_result(number: int) -> str:
    # Rich yearly messages
    year_texts = {
        1: (
            "🌱 *Personal Year 1 – A Year of New Beginnings*\n\n"
            "This year marks the start of a fresh 9-year cycle for you. It’s a time of planting seeds, setting intentions, "
            "and boldly stepping into new paths. ✨ Opportunities for personal growth, career shifts, or even new relationships "
            "may appear — but you must take initiative.\n\n"
            "💫 *Soul Insight:* Release the past. This year favors independence, courage, and embracing your unique vision. "
            "Everything you start now will shape the years ahead."
        ),
        2: (
            "🌸 *Personal Year 2 – A Year of Harmony & Patience*\n\n"
            "This is a softer, more introspective year focused on relationships, emotional healing, and cooperation. 💞 "
            "It’s a time to nurture connections, deepen trust, and allow things to unfold in divine timing. Life feels "
            "gentler now, asking you to listen more than act.\n\n"
            "💫 *Soul Insight:* This year strengthens your emotional wisdom. Be patient — what grows quietly now will bloom "
            "in future years."
        ),
        3: (
            "🎨 *Personal Year 3 – A Year of Joy & Self-Expression*\n\n"
            "This is a vibrant, creative year filled with social connections, fun, and opportunities to express yourself. 🌈 "
            "Your natural charm and creativity are amplified now, making it easier to meet new people and share your gifts.\n\n"
            "💫 *Soul Insight:* Let go of fear and embrace your authentic voice. This year is about enjoying life and inspiring "
            "others through your presence."
        ),
        4: (
            "🏡 *Personal Year 4 – A Year of Building Foundations*\n\n"
            "This is a year of stability, hard work, and creating structures that support your future. 🧱 It’s time to focus "
            "on discipline, organization, and taking practical steps toward your long-term goals.\n\n"
            "💫 *Soul Insight:* This year strengthens your roots. Be patient and consistent — what you build now will support "
            "the next phase of your journey."
        ),
        5: (
            "💃 *Personal Year 5 – A Year of Freedom & Change*\n\n"
            "This year brings movement, transformation, and unexpected opportunities. ✈️ It’s a time to embrace change, take "
            "risks, and break free from what no longer serves you. Life may feel faster and more adventurous.\n\n"
            "💫 *Soul Insight:* Stay flexible. This year teaches you adaptability and opens doors to new experiences that will "
            "reshape your path."
        ),
        6: (
            "💞 *Personal Year 6 – A Year of Love & Responsibility*\n\n"
            "This is a heart-centered year focused on relationships, family, and emotional commitments. 🌿 You may feel called "
            "to nurture, heal, or create more harmony in your personal life. Love and community are highlighted.\n\n"
            "💫 *Soul Insight:* This year asks you to balance self-care with caring for others. Love is both your lesson and gift."
        ),
        7: (
            "🔮 *Personal Year 7 – A Year of Inner Growth & Reflection*\n\n"
            "This is a deeply spiritual year of introspection, learning, and soul-searching. 🌌 You may feel drawn to spend "
            "more time alone, studying, meditating, or seeking deeper truths. Answers come from within.\n\n"
            "💫 *Soul Insight:* Trust the quiet moments. This year prepares your spirit for profound future transformation."
        ),
        8: (
            "💼 *Personal Year 8 – A Year of Power & Achievement*\n\n"
            "This is a year of stepping into your power, manifesting abundance, and taking leadership. 💫 Career growth, "
            "financial opportunities, and recognition are highlighted — but only if you align with integrity.\n\n"
            "💫 *Soul Insight:* This year teaches you how to balance material success with spiritual wisdom."
        ),
        9: (
            "🌈 *Personal Year 9 – A Year of Completion & Letting Go*\n\n"
            "This is a year of closure, reflection, and emotional release. 🌍 It’s time to finish old cycles, release what no "
            "longer serves you, and prepare for a new 9-year chapter. Expect endings that make space for transformation.\n\n"
            "💫 *Soul Insight:* This year asks for surrender and compassion. What you release now creates room for your next evolution."
        ),
        11: (
            "⚡ *Personal Year 11 – A Master Year of Spiritual Awakening*\n\n"
            "This is a powerful year of heightened intuition, inspiration, and soul-level lessons. 🌠 You may feel more "
            "sensitive, yet deeply connected to your higher purpose. Encounters now may feel fated or karmic.\n\n"
            "💫 *Soul Insight:* Trust your inner guidance. This year aligns you with your higher calling."
        ),
        22: (
            "🏗 *Personal Year 22 – A Master Year of Building Dreams*\n\n"
            "This is a rare year where you have the potential to manifest something truly monumental. 🌐 It’s about combining "
            "spiritual vision with practical action to create lasting impact.\n\n"
            "💫 *Soul Insight:* This year calls you to embrace your power as a creator and leave a meaningful legacy."
        ),
        33: (
            "🌟 *Personal Year 33 – A Master Year of Service & Love*\n\n"
            "This is a deeply compassionate year focused on healing, teaching, and uplifting others. ✨ It’s about giving love "
            "without conditions and embracing your highest spiritual purpose.\n\n"
            "💫 *Soul Insight:* This year asks you to embody pure love as a guide and healer."
        )
    }

    year_message = year_texts.get(number, "✨ A mysterious year ahead awaits your discovery…")

    return (
        f"🌌 *Personal Year Forecast*\n\n"
        f"📅 *Your Personal Year Number:* `{number}`\n\n"
        f"{year_message}\n\n"
        f"💫 *Yearly Guidance:* Align with this vibration and trust the timing of your soul’s journey. Each personal year is "
        f"part of a bigger 9-year cycle that shapes your destiny.\n\n"
        f"🌟 *As a Premium member, you can also explore your **Destiny Number, Karmic Debts, and Compatibility Reading** "
        f"to see how this year connects with your larger soul path.*"
    )
