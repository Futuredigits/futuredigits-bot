def calculate_birthday_number(date_str: str) -> int:
    try:
        day = int(date_str.strip().split('.')[0])
    except:
        raise ValueError("Invalid date format. Use DD.MM.YYYY")

    return day if day in {11, 22} else sum(int(d) for d in str(day)) if day > 9 else day


def get_birthday_result(number: int) -> str:
    results = {
        1: "🔥 *Birthday 1 – The Originator*\n\nYou were born with a pioneering spirit. Independent, assertive, and confident — you’re meant to lead, initiate, and stand out. You possess a strong inner drive and the courage to walk your own path, even if others don’t follow. Challenges only sharpen your resilience. Lead with purpose, and your strength becomes a beacon.",
        2: "🌸 *Birthday 2 – The Harmonizer*\n\nYour birthdate gifts you with sensitivity, diplomacy, and emotional depth. You are naturally intuitive, compassionate, and deeply attuned to others. Where others compete, you cooperate. Your quiet strength lies in your ability to bring peace and balance to relationships and situations. The world feels gentler when you’re near.",
        3: "🎨 *Birthday 3 – The Creative Soul*\n\nYou bring joy, color, and emotional expression into the world. Charming and artistic, you have a magnetic way of communicating through words, humor, or performance. People are drawn to your lighthearted energy. When you fully express your truth, you awaken others to their own inner joy.",
        4: "🧱 *Birthday 4 – The Master of Structure*\n\nDiscipline, order, and dedication are your foundation. You were born with the gift of building things that last — be it a home, a business, or a legacy. People trust your reliability and sense of responsibility. While others drift, you create stability. Your methodical approach is your power.",
        5: "🌍 *Birthday 5 – The Freedom Seeker*\n\nYou carry the vibration of curiosity, adventure, and personal liberation. Change energizes you. You were born to explore life through experience — mentally, physically, and emotionally. You thrive when you’re not confined. Embrace the unknown, and your life becomes a dynamic story of transformation.",
        6: "💞 *Birthday 6 – The Nurturer*\n\nYou are a natural caregiver — compassionate, devoted, and loving. Your soul finds fulfillment through family, service, and beauty. Others often lean on your wisdom and sense of responsibility. Your gift lies in making others feel safe and seen. Harmony flows from your heart outward.",
        7: "🔮 *Birthday 7 – The Mystic Observer*\n\nBorn with deep intuition and a sharp mind, you are driven by a thirst for truth. You see beyond surface appearances and long to understand life’s deeper meaning. Solitude and reflection are sacred to you. When you trust your inner guidance, you unlock spiritual mastery.",
        8: "💼 *Birthday 8 – The Powerhouse*\n\nYou were born with ambition, focus, and a natural ability to achieve. Leadership, wealth, and influence align with your life path — but only when paired with integrity. You’re here to master the material world and uplift others through your success. Own your power with wisdom.",
        9: "🌈 *Birthday 9 – The Compassionate Old Soul*\n\nYour birthday carries the energy of wisdom, empathy, and global consciousness. You are here to serve, to heal, and to let go. People sense your depth and heart. Your life is a journey of emotional refinement, artistic grace, and soulful giving. What you release, you transcend.",
        11: "⚡ *Birthday 11 – The Inspired Messenger*\n\nYou were born under a master number — a sign of heightened intuition and spiritual purpose. Your path involves guiding others, not just through words, but through your energy. You're sensitive, visionary, and capable of awakening truth in others. Walk with courage — your light is meant to shine.",
        22: "🏗 *Birthday 22 – The Master Builder*\n\nYou carry one of the most powerful vibrations in numerology. With discipline, vision, and spiritual alignment, you're capable of creating structures that serve the world. You're not here to think small — you're here to manifest on a grand scale. Stay grounded, and your potential becomes limitless."
    }


    text = results.get(number, "⚠️ An error occurred while calculating your Birthday Number.")
    return text + "\n\n🔓 *Want deeper insight? Try Expression or Destiny in Premium Tools!*"
