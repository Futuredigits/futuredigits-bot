def calculate_personality_number(name: str) -> int:
    name = name.upper()
    consonants = {
        'B': 2, 'C': 3, 'D': 4, 'F': 6, 'G': 7, 'H': 8, 'J': 1, 'K': 2, 'L': 3,
        'M': 4, 'N': 5, 'P': 7, 'Q': 8, 'R': 9, 'S': 1, 'T': 2, 'V': 4,
        'W': 5, 'X': 6, 'Y': 7, 'Z': 8
    }

    total = sum(consonants.get(char, 0) for char in name if char in consonants)
    print("✅ Total consonant value:", total)  # ← Debug line

    def reduce(n):
        if n in {11, 22, 33}:
            return n
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n

    reduced = reduce(total)
    print("✅ Reduced personality number:", reduced)  # ← Debug line

    return reduced


def get_personality_result(number: int) -> str:
    results = {
        1: "🔥 *Personality 1 – The Confident Leader*\n\nYou come across as bold, driven, and capable. People see you as someone who takes charge, stands tall, and leads with certainty. Your energy commands respect. 💪\n\nLead with integrity and others will follow.",
        2: "🌸 *Personality 2 – The Gentle Peacemaker*\n\nYou appear warm, diplomatic, and soft-spoken. Others are drawn to your calm presence and your ability to make people feel safe and understood. 🤝\n\nYou’re the quiet strength behind every team.",
        3: "🎭 *Personality 3 – The Charmer*\n\nYou radiate charm, playfulness, and creativity. People see you as expressive, fun, and emotionally engaging. You have a light that makes others smile. 🌈\n\nUse your presence to inspire joy.",
        4: "🧱 *Personality 4 – The Reliable Rock*\n\nYou give off a grounded, stable, and dependable presence. People trust you. They see you as hardworking and responsible. Your energy is steady and strong. 🛠️\n\nYou bring order to chaos.",
        5: "🌟 *Personality 5 – The Free Spirit*\n\nYou appear exciting, curious, and bold. People see you as dynamic and open to anything. You thrive on new experiences — and others feel your spark. ✈️\n\nStay wild, stay true.",
        6: "💞 *Personality 6 – The Nurturer*\n\nYou’re seen as kind, responsible, and emotionally comforting. People feel protected and supported in your presence. Beauty, harmony, and service radiate from you. 🌿\n\nLead with love — it’s your superpower.",
        7: "🧘 *Personality 7 – The Mysterious Thinker*\n\nYou come across as private, deep, and introspective. People may sense you’re intelligent or spiritual, but also distant. Your calm mystique draws curiosity. 🔮\n\nLet your wisdom speak softly.",
        8: "💼 *Personality 8 – The Power Presence*\n\nYou project strength, authority, and ambition. Others often see you as confident and successful — someone who knows their value. 💰\n\nOwn your power with humility.",
        9: "🌈 *Personality 9 – The Compassionate Soul*\n\nYou radiate empathy, warmth, and wisdom. People see you as generous, emotionally evolved, and connected to a bigger mission. 🌍\n\nYou make others feel seen and loved.",
        11: "⚡ *Personality 11 – The Enlightened Presence*\n\nYou come across as inspiring, insightful, and spiritually elevated. Others may sense your inner light or intuitive strength, even if they can't explain it. 🌠\n\nYour presence uplifts by simply being.",
        22: "🏛 *Personality 22 – The Master Builder Aura*\n\nYou carry the energy of leadership and long-term vision. People sense you’re capable of big things. You radiate trust, strength, and purpose. 🌐\n\nStand in your legacy.",
        33: "🌟 *Personality 33 – The Radiant Healer*\n\nYou shine with compassion, wisdom, and spiritual beauty. People feel your loving presence, even from afar. You carry the vibration of peace. ✨\n\nYou are the light in dark places."
    }

    text = results.get(number, "⚠️ An error occurred while calculating your Personality Number.")
    return text + "\n\n🔓 *Want deeper insight? Try Expression or Destiny in Premium Tools!*"








