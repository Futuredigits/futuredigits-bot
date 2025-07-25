import datetime

def reduce_num(n: int) -> int:
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(d) for d in str(n))
    return n

def universal_vibe_message(vibe: int) -> str:
    messages = {
        1: (
            "🌱 *Universal Day 1 – Fresh Starts & New Beginnings*\n\n"
            "Today carries the energy of independence, courage, and new possibilities. It’s a great day to start projects, "
            "make decisions, or take the first step toward something you’ve been delaying. 💫\n\n"
            "💖 *How to align:* Be bold, trust yourself, and plant seeds for future growth."
        ),
        2: (
            "🌸 *Universal Day 2 – Harmony & Relationships*\n\n"
            "Today’s collective energy is softer, focused on cooperation, empathy, and emotional connection. It’s ideal for "
            "resolving conflicts, building partnerships, or simply nurturing your heart. 💞\n\n"
            "💖 *How to align:* Be patient, listen deeply, and honor your relationships."
        ),
        3: (
            "🎨 *Universal Day 3 – Joy, Creativity & Expression*\n\n"
            "This is a vibrant day full of social energy, playfulness, and inspiration. It’s perfect for expressing your ideas, "
            "connecting with others, or doing something creative. 🌈\n\n"
            "💖 *How to align:* Share your authentic self—your words and energy uplift others."
        ),
        4: (
            "🏡 *Universal Day 4 – Stability & Discipline*\n\n"
            "Today brings grounding energy. It’s a good day for planning, organizing, and taking steady steps toward your long-term goals. 🧱\n\n"
            "💖 *How to align:* Focus on what truly matters. Build, organize, and create structure in your life."
        ),
        5: (
            "💃 *Universal Day 5 – Change & Adventure*\n\n"
            "The energy today is dynamic and full of movement. Expect surprises, opportunities for growth, and the chance to break free from routine. ✈️\n\n"
            "💖 *How to align:* Stay flexible, try something new, and embrace the unexpected."
        ),
        6: (
            "💞 *Universal Day 6 – Love & Harmony*\n\n"
            "Today’s vibration is nurturing and heart-centered. It’s a day for family, love, healing, and emotional balance. 🌿\n\n"
            "💖 *How to align:* Connect with loved ones, care for your well-being, and create harmony in your surroundings."
        ),
        7: (
            "🔮 *Universal Day 7 – Reflection & Inner Wisdom*\n\n"
            "This is a quiet, introspective day. It’s about learning, meditating, and seeking deeper truths. 🌌\n\n"
            "💖 *How to align:* Take time for yourself, listen to your intuition, and trust your inner knowing."
        ),
        8: (
            "💼 *Universal Day 8 – Power & Achievement*\n\n"
            "Today brings ambitious, empowering energy. It’s excellent for career moves, financial planning, or making important decisions. 💫\n\n"
            "💖 *How to align:* Step into your confidence and use your influence wisely."
        ),
        9: (
            "🌈 *Universal Day 9 – Completion & Letting Go*\n\n"
            "Today’s energy is about closure, forgiveness, and releasing what no longer serves you. It’s a day for emotional healing and compassion. 🌍\n\n"
            "💖 *How to align:* Let go of the past with love, and make space for the new."
        ),
        11: (
            "⚡ *Master Universal Day 11 – Spiritual Awakening*\n\n"
            "This is a highly intuitive day filled with synchronicities and soul-level insights. 🌠 You may feel extra sensitive and connected to higher guidance.\n\n"
            "💖 *How to align:* Follow your intuition—it’s showing you the next step on your soul path."
        ),
        22: (
            "🏗 *Master Universal Day 22 – Building Big Dreams*\n\n"
            "Today is a powerful day for manifesting visions into reality. It’s about taking practical steps toward big goals that serve not just you, but others. 🌐\n\n"
            "💖 *How to align:* Focus on long-term impact. Your efforts today can create lasting change."
        ),
        33: (
            "🌟 *Master Universal Day 33 – Compassion & Healing*\n\n"
            "This is a deeply spiritual day focused on love, service, and emotional healing. ✨ It’s about giving and receiving love freely.\n\n"
            "💖 *How to align:* Be kind, forgive, and share your wisdom to uplift others."
        )
    }
    return messages.get(vibe, "✨ A mysterious energy flows through today. Stay open to its lessons.")

def get_daily_universal_vibe_forecast() -> str:
    today = datetime.date.today()
    date_str = today.strftime("%d %B %Y")
    
    # Universal Day Number
    date_sum = sum(int(d) for d in today.strftime("%d%m%Y"))
    vibe = reduce_num(date_sum)
    
    # Get the forecast
    vibe_text = universal_vibe_message(vibe)
    
    return (
        f"🗓 *Daily Universal Vibe – {date_str}*\n\n"
        f"{vibe_text}\n\n"
        f"💫 *How to flow with today:* Remember that the universe has its own rhythm. When you align with the energy of the day, everything feels more effortless.\n\n"
        f"🌟 *As a Premium member, you can also explore your **Moon Energy, Personal Year Forecast, and Compatibility** "
        f"to see how today connects with your soul journey.*"
    )
