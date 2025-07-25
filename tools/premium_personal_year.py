import datetime

def reduce_num(n: int) -> int:
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(d) for d in str(n))
    return n

def calculate_personal_year_number_for(birthdate: str, target_year: int) -> int:
    day, month, year = map(int, birthdate.split('.'))
    total = day + month + sum(int(d) for d in str(target_year))
    return reduce_num(total)

def personal_year_theme_long(n: int) -> str:
    details = {
        1: (
            "🌱 *Personal Year 1 – The Year of New Beginnings*\n\n"
            "This year marks the start of a brand-new 9-year cycle for you. It is a time of self-discovery, independence, and bold action. "
            "Life will feel like a blank canvas waiting for your vision. You may feel an inner push to step away from old patterns, start fresh projects, or redefine who you truly are. 💫\n\n"
            "In love, this year can bring new connections or a shift in existing relationships as you prioritize your personal growth. "
            "In career and life purpose, it’s a year to take initiative—plant the seeds that will grow over the next cycle.\n\n"
            "💖 *Soul Lesson:* Learn to trust yourself and embrace your individuality. This year is about YOU stepping into your true power.\n"
        ),
        2: (
            "🌸 *Personal Year 2 – The Year of Harmony & Patience*\n\n"
            "This year softens the energy, inviting emotional healing, nurturing connections, and deepening relationships. "
            "It’s a time of listening rather than pushing, allowing the universe to reveal things slowly and beautifully. "
            "You’ll crave emotional closeness and may be drawn to partnerships or collaborations that bring balance. 💞\n\n"
            "In love, this is a tender year of building trust and intimacy. In career, it’s about cooperation rather than competition. "
            "Spiritually, you’ll feel more intuitive and sensitive, aligned with gentle guidance.\n\n"
            "💖 *Soul Lesson:* Practice patience, trust divine timing, and strengthen your emotional wisdom.\n"
        ),
        3: (
            "🎨 *Personal Year 3 – The Year of Joy & Self-Expression*\n\n"
            "This is a vibrant and social year where life feels lighter. Creativity flows more easily, and you’re meant to express your authentic self without fear. "
            "Your energy is magnetic now, attracting new friendships, love, and opportunities. 🌈\n\n"
            "In love, it’s a playful, romantic year with plenty of social connections. Career-wise, it’s perfect for creative projects, communication, and sharing your ideas. "
            "Spiritually, joy itself becomes your teacher—reminding you to live in the present.\n\n"
            "💖 *Soul Lesson:* Release self-doubt and embrace your inner light. When you express your truth, you inspire others.\n"
        ),
        4: (
            "🏡 *Personal Year 4 – The Year of Stability & Building Foundations*\n\n"
            "This is a grounding year of structure, discipline, and responsibility. Life slows down to help you create strong roots—whether in career, finances, home, or health. "
            "It’s not about quick wins, but about building something solid and lasting. 🧱\n\n"
            "In love, this is a year of deeper commitment and creating emotional security. In career, it’s about hard work, organization, and long-term plans. "
            "Spiritually, it teaches patience and the beauty of steady progress.\n\n"
            "💖 *Soul Lesson:* Focus on consistency and building the stable future you desire.\n"
        ),
        5: (
            "💃 *Personal Year 5 – The Year of Freedom & Change*\n\n"
            "This is a year of movement, transformation, and adventure. Expect the unexpected—life will bring new people, opportunities, and experiences that push you out of your comfort zone. "
            "It’s a time to break free from routines that feel limiting and embrace the unknown. ✈️\n\n"
            "In love, sparks fly with passion and excitement, but relationships may feel less stable if they lack true depth. In career, this is a year for flexibility and exploring different paths. "
            "Spiritually, it reminds you to trust the flow of life.\n\n"
            "💖 *Soul Lesson:* Let go of control and embrace the magic of change—it’s guiding you toward growth.\n"
        ),
        6: (
            "💞 *Personal Year 6 – The Year of Love & Responsibility*\n\n"
            "This is a heart-centered year where family, relationships, and home life take center stage. You may feel called to nurture, heal, or create harmony in your personal world. "
            "Commitments deepen now—emotionally and spiritually. 🌿\n\n"
            "In love, this is a year for romance, commitment, or even starting a family. In career, you may feel drawn to work that serves or supports others. "
            "Spiritually, it’s about opening your heart fully and learning love without conditions.\n\n"
            "💖 *Soul Lesson:* Find balance between caring for others and honoring your own needs.\n"
        ),
        7: (
            "🔮 *Personal Year 7 – The Year of Reflection & Spiritual Growth*\n\n"
            "This is a deeply introspective year. You’ll crave solitude, learning, and a deeper connection with your soul. "
            "Life slows down externally so you can look within for answers. 🌌\n\n"
            "In love, it’s a quieter year, focusing on emotional depth rather than outward romance. In career, it’s about research, analysis, or refining your skills. "
            "Spiritually, this is a powerful year for awakening, intuition, and understanding your life purpose on a deeper level.\n\n"
            "💖 *Soul Lesson:* Trust the wisdom within and embrace the stillness that reveals truth.\n"
        ),
        8: (
            "💼 *Personal Year 8 – The Year of Power & Achievement*\n\n"
            "This is a year of stepping into your power. Career, finances, and personal influence are highlighted, bringing opportunities for success and recognition. "
            "It’s a year to claim your worth and manifest abundance with integrity. 💫\n\n"
            "In love, this year requires balance—power dynamics may surface but can lead to deeper trust if handled with care. In career, it’s about leadership, ambition, and tangible results. "
            "Spiritually, it’s a lesson in balancing material success with higher purpose.\n\n"
            "💖 *Soul Lesson:* Align ambition with soul values to create meaningful success.\n"
        ),
        9: (
            "🌈 *Personal Year 9 – The Year of Completion & Release*\n\n"
            "This is a year of closure, reflection, and letting go. You may feel endings in relationships, career paths, or old patterns that no longer serve your highest good. "
            "It’s preparing you for a brand-new cycle next year. 🌍\n\n"
            "In love, it’s a healing year, where forgiveness and release open the heart. In career, it may bring transitions or completion of long-held goals. "
            "Spiritually, it teaches compassion, surrender, and trust in the greater plan.\n\n"
            "💖 *Soul Lesson:* Release the past with love—what you let go creates space for your future.\n"
        ),
        11: (
            "⚡ *Personal Year 11 – The Master Year of Spiritual Awakening*\n\n"
            "This is a powerful and sensitive year of heightened intuition, deep spiritual insights, and karmic lessons. "
            "You may feel more emotional and empathic as your soul aligns with a higher calling. 🌠\n\n"
            "In love, soul-level connections may appear, revealing karmic or destined relationships. In career, inspiration and creativity flow strongly, but you must stay balanced to avoid overwhelm. "
            "Spiritually, this is a year of enlightenment and aligning with divine purpose.\n\n"
            "💖 *Soul Lesson:* Trust your intuition—it’s guiding you toward your true path.\n"
        ),
        22: (
            "🏗 *Personal Year 22 – The Master Builder Year*\n\n"
            "This rare master year carries the potential to manifest something monumental. It combines spiritual insight with practical action, allowing you to create lasting impact for yourself and others. 🌐\n\n"
            "In love, it’s a year to build strong, lasting partnerships. In career, you can achieve extraordinary success through discipline and vision. "
            "Spiritually, it asks you to merge the mystical with the material.\n\n"
            "💖 *Soul Lesson:* Dream big and act with integrity—your legacy begins here.\n"
        ),
        33: (
            "🌟 *Personal Year 33 – The Master Year of Love & Service*\n\n"
            "This is a profoundly spiritual year of compassion, healing, and guiding others through your wisdom. "
            "It’s about embodying unconditional love and serving in ways that uplift humanity. ✨\n\n"
            "In love, it deepens emotional bonds and brings healing connections. In career, it’s about service, teaching, or creating beauty that inspires others. "
            "Spiritually, it’s a sacred year of aligning with divine love.\n\n"
            "💖 *Soul Lesson:* Lead through love, compassion, and selfless service.\n"
        )
    }
    return details.get(n, "✨ A mysterious yet powerful energy surrounds this year.")

def personal_year_theme_short(n: int) -> str:
    previews = {
        1: "🌱 *New beginnings, fresh starts, and bold opportunities*",
        2: "🌸 *Harmony, emotional healing, and deeper relationships*",
        3: "🎨 *Joy, self-expression, creativity, and social expansion*",
        4: "🏡 *Stability, discipline, and building strong foundations*",
        5: "💃 *Freedom, change, adventure, and unexpected opportunities*",
        6: "💞 *Love, family, responsibility, and deeper commitments*",
        7: "🔮 *Reflection, soul-searching, and spiritual clarity*",
        8: "💼 *Power, success, financial growth, and recognition*",
        9: "🌈 *Completion, closure, emotional release, and transition*",
        11: "⚡ *Spiritual awakening, heightened intuition, and divine purpose*",
        22: "🏗 *Building dreams into reality, manifesting on a grand scale*",
        33: "🌟 *Compassion, healing, teaching, and unconditional love*"
    }
    return previews.get(n, "✨ A mysterious energy guiding your journey")

def get_personal_year_forecast(birthdate: str) -> str:
    today = datetime.date.today()
    current_year = today.year
    
    # Calculate this year + next 2 years
    this_year_num = calculate_personal_year_number_for(birthdate, current_year)
    next_year_num = calculate_personal_year_number_for(birthdate, current_year + 1)
    future_year_num = calculate_personal_year_number_for(birthdate, current_year + 2)
    
    this_year_long = personal_year_theme_long(this_year_num)
    next_year_short = personal_year_theme_short(next_year_num)
    future_year_short = personal_year_theme_short(future_year_num)
    
    return (
        f"🌌 *Your Personal Year Forecast {current_year}*\n\n"
        f"{this_year_long}\n"
        f"💫 *How to thrive this year:* Align your choices with this vibration, and you’ll flow effortlessly with life’s rhythm.\n\n"
        f"🔮 *Your Roadmap Ahead:*\n"
        f"✅ *{current_year + 1} → Personal Year {next_year_num} – {next_year_short[2:]}*\n"
        f"✅ *{current_year + 2} → Personal Year {future_year_num} – {future_year_short[2:]}*\n\n"
        f"🌟 *As a Premium member, you can also explore your **Destiny Number, Compatibility Reading, and Karmic Debts** to see how these years connect to your bigger soul journey.*"
    )
