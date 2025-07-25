import datetime
import math

def reduce_num(n: int) -> int:
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(d) for d in str(n))
    return n

def get_moon_phase(today: datetime.date) -> str:
    # Simple moon phase calculation
    diff = today - datetime.date(2001, 1, 1)
    days = diff.days
    lunations = days / 29.53058867
    pos = lunations - int(lunations)
    if pos < 0.03: return "🌑 New Moon"
    elif pos < 0.25: return "🌒 Waxing Crescent"
    elif pos < 0.28: return "🌓 First Quarter"
    elif pos < 0.47: return "🌔 Waxing Gibbous"
    elif pos < 0.53: return "🌕 Full Moon"
    elif pos < 0.72: return "🌖 Waning Gibbous"
    elif pos < 0.78: return "🌗 Last Quarter"
    elif pos < 0.97: return "🌘 Waning Crescent"
    else: return "🌑 New Moon"

def moon_energy_message(phase: str, vibe: int) -> str:
    # Rich descriptions based on Moon phase + vibe
    phase_messages = {
        "🌑 New Moon": (
            "A fresh lunar cycle begins, bringing quiet yet powerful energy for setting intentions and starting anew. "
            "This is a time for reflection, clarity, and planting the seeds of your next chapter."
        ),
        "🌒 Waxing Crescent": (
            "The Moon is growing, and so is your momentum. It’s time to take small, aligned steps toward your dreams, "
            "nurturing the ideas you’ve just planted."
        ),
        "🌓 First Quarter": (
            "The Moon is half-lit, reminding you that growth requires action. Challenges may appear now, but they are opportunities "
            "to adjust and strengthen your path."
        ),
        "🌔 Waxing Gibbous": (
            "Energy is building, calling you to refine your goals and prepare for completion. Trust the process and stay consistent."
        ),
        "🌕 Full Moon": (
            "The Full Moon illuminates everything—your desires, your fears, and your truths. Emotions may feel heightened, "
            "but clarity and revelation are here. It’s a time for celebration, manifestation, and release."
        ),
        "🌖 Waning Gibbous": (
            "The Moon begins to wane, inviting gratitude and reflection. It’s time to share your wisdom and let go of what you no longer need."
        ),
        "🌗 Last Quarter": (
            "A time of release and closure. Clear out old patterns, finish lingering tasks, and prepare your soul for renewal."
        ),
        "🌘 Waning Crescent": (
            "A quiet, introspective time before the next cycle begins. Rest, recharge, and listen to your inner voice."
        ),
    }

    vibe_messages = {
        1: "🌱 *Today’s Numerology Vibration: 1* – A day for fresh starts, courage, and taking bold steps.",
        2: "🌸 *Vibration 2* – A day for harmony, emotional connection, and building trust.",
        3: "🎨 *Vibration 3* – A day for creativity, self-expression, and joyful connections.",
        4: "🏡 *Vibration 4* – A grounding day to focus on stability, structure, and planning.",
        5: "💃 *Vibration 5* – A day of freedom, change, and unexpected opportunities.",
        6: "💞 *Vibration 6* – A nurturing day for love, family, and emotional healing.",
        7: "🔮 *Vibration 7* – A reflective, spiritual day for introspection and insight.",
        8: "💼 *Vibration 8* – A powerful day for success, leadership, and manifestation.",
        9: "🌈 *Vibration 9* – A compassionate day for release, forgiveness, and completion.",
        11: "⚡ *Master Vibration 11* – A highly intuitive day of spiritual awakening and insight.",
        22: "🏗 *Master Vibration 22* – A day to manifest big visions into reality.",
        33: "🌟 *Master Vibration 33* – A day of unconditional love, healing, and divine service."
    }

    return f"{phase_messages.get(phase, '')}\n\n{vibe_messages.get(vibe, '')}"

def get_moon_energy_forecast() -> str:
    today = datetime.date.today()
    date_str = today.strftime("%d %B %Y")
    
    # Moon Phase
    moon_phase = get_moon_phase(today)
    
    # Universal Day Vibration
    date_sum = sum(int(d) for d in today.strftime("%d%m%Y"))
    vibe = reduce_num(date_sum)
    
    # Rich lunar + numerology meaning
    moon_message = moon_energy_message(moon_phase, vibe)
    
    return (
        f"🌕 *Moon Energy Forecast for {date_str}*\n\n"
        f"**Moon Phase Today:** {moon_phase}\n\n"
        f"{moon_message}\n\n"
        f"💫 *How to align with today’s Moon energy:* Listen to your intuition and flow with the cosmic rhythm. "
        f"Every lunar phase carries a gift—today is about embracing its lesson fully.\n\n"
        f"🌟 *As a Premium member, you can also explore your **Personal Year Forecast, Karmic Debts, and Compatibility** "
        f"to see how today’s energy fits into your bigger soul journey.*"
    )
