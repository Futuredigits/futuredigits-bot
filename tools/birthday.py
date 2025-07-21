def calculate_birthday_number(date_str: str) -> int:
    try:
        day = int(date_str.strip().split('.')[0])
    except:
        raise ValueError("Invalid date format. Use DD.MM.YYYY")

    return day if day in {11, 22} else sum(int(d) for d in str(day)) if day > 9 else day


def get_birthday_result(number: int) -> str:
    results = {
        1: "🔥 *Birthday 1 – Born Leader*\n\nYou were born with confidence, initiative, and independence. You naturally stand out and pave your own path.",
        2: "🌸 *Birthday 2 – Natural Peacemaker*\n\nYou bring harmony and kindness into everything you do. Sensitivity is your strength.",
        3: "🎨 *Birthday 3 – Creative Communicator*\n\nYou're joyful, expressive, and imaginative. Others are drawn to your playful nature.",
        4: "🧱 *Birthday 4 – Steady Builder*\n\nYou're grounded, reliable, and practical. You bring structure and dependability wherever you go.",
        5: "🌍 *Birthday 5 – Dynamic Adventurer*\n\nFreedom, travel, and excitement are your soul’s fuel. You thrive in motion and change.",
        6: "💞 *Birthday 6 – Nurturing Soul*\n\nYou naturally care for others. Home, beauty, and responsibility are part of your heart’s design.",
        7: "🔮 *Birthday 7 – Spiritual Seeker*\n\nYou are intuitive, analytical, and introspective. Depth and wisdom guide your journey.",
        8: "💼 *Birthday 8 – Power Player*\n\nYou're ambitious and capable. Leadership and success are part of your natural path.",
        9: "🌈 *Birthday 9 – Inspired Humanitarian*\n\nYou're deeply compassionate and artistic. You want to uplift and serve humanity.",
        11: "⚡ *Birthday 11 – Intuitive Visionary*\n\nYou have heightened sensitivity and inspiration. You are here to awaken and guide others.",
        22: "🏗 *Birthday 22 – Master Builder*\n\nYou were born to turn dreams into reality. Your potential to lead and serve is extraordinary."
    }

    text = results.get(number, "⚠️ An error occurred while calculating your Birthday Number.")
    return text + "\n\n🔓 *Want deeper insight? Try Expression or Destiny in Premium Tools!*"
