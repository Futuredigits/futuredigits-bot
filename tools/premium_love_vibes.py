import datetime
from tools.expression import calculate_expression_number

def calculate_love_vibes(full_name: str):
    # Get today's universal date vibration
    today = datetime.date.today()
    date_sum = sum(int(d) for d in today.strftime("%d%m%Y"))
    
    def reduce_num(n):
        while n > 9 and n not in (11, 22, 33):
            n = sum(int(d) for d in str(n))
        return n
    
    universal_vibe = reduce_num(date_sum)
    
    # User's personal name vibration
    personal_vibe = calculate_expression_number(full_name)
    
    # Romantic "love vibe number" → combine universal + personal
    vibe_number = reduce_num(universal_vibe + personal_vibe)
    
    # Score is a fun % compatibility with today's vibe
    diff = abs(universal_vibe - personal_vibe)
    score = max(20, 100 - diff * 10)  # ensures min 20%
    
    return score, vibe_number


def get_love_vibes_result(name: str, score: int, vibe_number: int) -> str:
    # Rich emotional romantic messages
    vibe_texts = {
        1: (
            "🔥 *Bold Romantic Energy – A Day for New Beginnings*\n\n"
            "Today carries the spark of courage and fresh starts. If your heart has been waiting to express something, "
            "this is the perfect moment to take the lead. 💫 Whether it’s reaching out to someone new, reigniting passion "
            "in an existing relationship, or simply showing yourself love, the universe supports bold, heartfelt action.\n\n"
            "Love today feels direct, exciting, and full of possibility — but only if you dare to embrace it. Be confident, "
            "open, and let your authentic feelings guide you."
        ),
        2: (
            "🌸 *Tender & Harmonious Energy – A Day for Emotional Connection*\n\n"
            "The romantic energy today is soft, nurturing, and deeply attuned to the heart. It’s a beautiful time for "
            "gentle conversations, reconciliation, or simply holding space for love to flow naturally. 💞 Small gestures "
            "of kindness will feel deeply meaningful under this vibration.\n\n"
            "If you’re in a relationship, deepen your bond through shared quiet moments. If you’re single, today’s energy "
            "invites you to reflect on the love you deserve, opening your heart to genuine connection."
        ),
        3: (
            "🎨 *Playful & Flirty Energy – A Day of Lightness and Joy*\n\n"
            "Romance today feels vibrant, fun, and irresistibly magnetic. 🌈 It’s the perfect time to flirt, laugh, and "
            "connect with others without heavy expectations. Creativity and humor fuel attraction now, making your energy "
            "especially charming.\n\n"
            "Whether you’re meeting someone new or rekindling sparks, approach love with curiosity and playfulness. The more "
            "you shine your authentic self, the more love responds to your vibration."
        ),
        4: (
            "🏡 *Stable & Grounded Energy – A Day to Build Deeper Trust*\n\n"
            "Today’s romantic energy brings a sense of security, loyalty, and emotional grounding. It’s a time to show love "
            "through actions rather than words. 🧱 Couples may feel drawn to discuss future plans, strengthen commitments, "
            "or create a comforting space together.\n\n"
            "If you’re single, focus on building self-love and clarity about the kind of partnership that truly supports your "
            "soul’s growth. This is a day to lay strong emotional foundations."
        ),
        5: (
            "💃 *Spontaneous & Adventurous Energy – Expect the Unexpected*\n\n"
            "Love today feels alive, unpredictable, and full of exciting twists. ✈️ It’s the perfect time for spontaneous "
            "gestures, adventurous dates, or simply stepping outside your usual patterns. This energy awakens passion and "
            "opens the door to thrilling connections.\n\n"
            "Stay open-minded and flexible — romance may come from the most unexpected places. If you’ve been waiting for "
            "a shift, today is a spark of fresh excitement."
        ),
        6: (
            "💞 *Nurturing & Loving Energy – A Day of Emotional Warmth*\n\n"
            "Today’s romantic energy is heart-centered and deeply nurturing. 🌿 It’s a wonderful time to care for your partner, "
            "your family, or even yourself. Acts of love and service carry extra meaning now, and emotional connections feel "
            "extra soothing.\n\n"
            "If you’re single, focus on self-care and the love that already surrounds you. Love flows naturally when you’re "
            "aligned with gratitude and kindness."
        ),
        7: (
            "🔮 *Reflective & Spiritual Energy – Love on a Deeper Level*\n\n"
            "Romance today feels introspective, intuitive, and soul-deep. 🌌 It’s a day for quiet moments, deep conversations, "
            "and understanding the emotional layers beneath your connections. If you’ve been feeling unclear about love, today "
            "brings inner clarity.\n\n"
            "Trust your intuition — it’s guiding you toward the kind of love that truly aligns with your spirit."
        ),
        8: (
            "💼 *Empowered Romantic Energy – Magnetic & Strong*\n\n"
            "Today’s energy brings confidence and magnetism into your love life. 💫 It’s a day to stand in your power, know "
            "your worth, and attract love that respects your strength. Romantic encounters may feel passionate and deeply "
            "transformative.\n\n"
            "If you’re in a relationship, this is a great time to discuss shared goals. If you’re single, your confidence is "
            "especially attractive now — love responds to self-assured energy."
        ),
        9: (
            "🌈 *Compassionate & Healing Energy – A Day for Heart Healing*\n\n"
            "Romance today is tender, compassionate, and emotionally healing. 🌍 It’s a beautiful time to forgive, let go of "
            "old wounds, and open your heart to deeper love. Acts of kindness and empathy carry extra weight under this energy.\n\n"
            "Whether single or partnered, focus on the bigger picture of love — it’s about giving and receiving from a place of "
            "pure intention."
        ),
        11: (
            "⚡ *Intense Spiritual Connection – A Soul-Level Love Day*\n\n"
            "Today’s love energy is highly spiritual and intuitive. 🌠 You may feel synchronicities, soul recognition, or "
            "profound emotional moments. Encounters now feel destined, as if guided by unseen forces.\n\n"
            "This is a day to embrace the magic of love beyond logic. Trust what your heart is sensing — it’s being guided."
        ),
        22: (
            "🏗 *Building Sacred Bonds – Long-Term Love Vibes*\n\n"
            "Romantic energy today supports commitment, building strong foundations, and making decisions that shape the "
            "future. 🌐 It’s ideal for couples ready to grow together and create something meaningful.\n\n"
            "If you’re single, focus on the qualities that would truly support a lasting soul connection. Today favors love "
            "that lasts beyond fleeting attraction."
        ),
        33: (
            "🌟 *Unconditional Love Energy – Pure Heart Connection*\n\n"
            "Today’s energy overflows with compassion, healing, and divine love. ✨ It’s a powerful time for forgiveness, "
            "reconciliation, and emotional renewal. Encounters under this energy feel transformative and soul-nourishing.\n\n"
            "Let your love flow freely — it has the power to heal not just your own heart, but the hearts of those around you."
        )
    }

    vibe_message = vibe_texts.get(vibe_number, "✨ Love feels mysterious today… trust the energy and stay open to surprises.")

    return (
        f"❤️ *Love Vibes Reading*\n\n"
        f"✨ *{name}*\n"
        f"📅 *Today’s Romantic Energy:* `{score}%`\n\n"
        f"{vibe_message}\n\n"
        f"💫 *Romantic Tip:* Follow today’s flow — whether it’s bold action, quiet reflection, or unexpected passion, "
        f"the universe is aligning your heart with what it needs most right now.\n\n"
        f"🌟 *As a Premium member, you can also explore your **Compatibility Reading, Karmic Debts, and Personal Year Forecast** "
        f"to deepen your journey of love and connection.*"
    )

