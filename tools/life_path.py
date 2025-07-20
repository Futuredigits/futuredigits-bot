def calculate_life_path_number(date_str: str) -> int:
    # Accept DD-MM-YYYY format
    try:
        day, month, year = map(int, date_str.split('-'))
    except ValueError:
        raise ValueError("Invalid date format. Use DD.MM.YYYY.")
    
    digits = [int(d) for d in f"{day:02d}{month:02d}{year}"]
    total = sum(digits)

    def reduce_to_life_path(n):
        if n in {11, 22, 33}:
            return n
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n

    return reduce_to_life_path(total)


def get_life_path_result(number: int) -> str:
    results = {
        1: "✨ *Life Path 1 – The Leader*\n\nYou were born with drive, ambition, and the desire to stand out. You are independent, courageous, and destined to forge your own path. People naturally look to you for guidance, and you're here to inspire confidence through bold action. 🔥\n\nStay grounded, and your leadership will leave a lasting legacy.",
        2: "🤝 *Life Path 2 – The Peacemaker*\n\nYour soul came here to build harmony, not war. You are gentle, intuitive, and deeply sensitive to the feelings of others. You bring balance, diplomacy, and grace to relationships. 🌸\n\nThough quiet in power, your presence soothes and heals. You're the calm in the storm.",
        3: "🎨 *Life Path 3 – The Creative Communicator*\n\nJoyful, expressive, and imaginative — your path is one of inspiration. You are meant to uplift others through art, words, or performance. 🎭\n\nWhen you share your light, people feel alive. Just beware of self-doubt — your gift is your voice.",
        4: "🏗 *Life Path 4 – The Master Builder*\n\nYou're here to create stability, structure, and success through discipline and dedication. Practical, loyal, and hardworking — you value honesty and results. 🔧\n\nWhile others dream, you build. Your legacy is crafted brick by brick.",
        5: "🌍 *Life Path 5 – The Freedom Seeker*\n\nAdventure calls your soul. You’re meant to explore, adapt, and break free from limits. Dynamic and charismatic, you thrive in change. ✈️\n\nYour gift is versatility — live boldly, love widely, and never fear the unknown.",
        6: "💞 *Life Path 6 – The Nurturer*\n\nYou were born to care, protect, and guide. Family, community, and love are your highest values. You have a healing presence, drawn to beauty and responsibility. 🌿\n\nWhen you embrace service without losing yourself, you become a beacon of love.",
        7: "🔮 *Life Path 7 – The Mystic Seeker*\n\nYou are the thinker, the questioner, the soul in search of truth. Spiritual and analytical, you're driven to understand life’s mysteries. 🧘‍♂️\n\nSolitude strengthens you. Trust your inner wisdom — your answers are already within.",
        8: "💼 *Life Path 8 – The Powerhouse*\n\nAmbition pulses through your veins. You’re here to master material success, leadership, and manifestation. You understand business, strategy, and the value of vision. 💰\n\nLead with integrity, and you’ll build empires that uplift others too.",
        9: "🌈 *Life Path 9 – The Humanitarian*\n\nYou are a wise old soul — compassionate, selfless, and deeply aware of life’s deeper purpose. You’re here to uplift humanity, share love, and let go. 🌍\n\nYour life is about service, art, healing, and spiritual truth. Let your heart guide the way.",
        11: "⚡ *Life Path 11 – The Spiritual Messenger*\n\nYou're a lightning rod of intuition and inspiration. With heightened sensitivity and vision, you're here to awaken others through teaching, art, or healing. 🌠\n\nThough your path may be intense, your presence is divine. Walk it with courage.",
        22: "🏛 *Life Path 22 – The Master Builder*\n\nYou came here to manifest dreams into reality. With the soul of a visionary and the mind of a master architect, you’re capable of building something that transforms the world. 🌐\n\nChannel your power with discipline — and the impossible becomes real.",
        33: "🌟 *Life Path 33 – The Master Teacher*\n\nYou are here to be a light in the dark. Compassionate, selfless, and wise beyond your years, your mission is to heal, teach, and uplift others. ✨\n\nThis path requires deep surrender and unconditional love. The world needs your soul."
    }

    text = results.get(number, "⚠️ An error occurred while calculating your Life Path Number.")
    return text + "\n\n🔓 *Want deeper insight? Try Expression or Destiny in Premium Tools!*"
