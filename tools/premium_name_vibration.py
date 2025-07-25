from tools.expression import calculate_expression_number

def get_name_vibration_meaning(full_name: str) -> str:
    # Calculate Expression Number from name
    number = calculate_expression_number(full_name)

    meanings = {
        1: "🔥 *Vibration 1 – The Independent Leader*\n\nYour name carries the energy of originality and confidence. "
           "It reflects a soul that came here to lead, create, and forge new paths. You inspire others through your strength and courage. "
           "You’re meant to stand out and embrace your individuality.\n\n💫 *Message:* Trust your instincts—your name vibration pushes you toward greatness.",

        2: "🌸 *Vibration 2 – The Harmonizer*\n\nYour name carries the soft, loving energy of cooperation and diplomacy. "
           "You are naturally intuitive, empathetic, and sensitive to the emotions of others. "
           "Your soul came here to build bridges and create harmony.\n\n💫 *Message:* Your vibration thrives when you nurture connections and trust divine timing.",

        3: "🎨 *Vibration 3 – The Creative Communicator*\n\nYour name radiates creativity, charm, and self-expression. "
           "You bring lightness, joy, and inspiration wherever you go. "
           "This vibration is deeply connected to art, words, and emotional expression.\n\n💫 *Message:* Speak your truth—your voice is your gift to the world.",

        4: "🏡 *Vibration 4 – The Builder*\n\nYour name carries a stable, grounded energy. "
           "You are dependable, disciplined, and here to create lasting foundations—whether in family, career, or community. "
           "This vibration values honesty, loyalty, and structure.\n\n💫 *Message:* Your soul thrives when you build something meaningful step by step.",

        5: "💃 *Vibration 5 – The Free Spirit*\n\nYour name vibrates with freedom, adventure, and adaptability. "
           "You are a seeker of experiences and change. Life under this vibration is never stagnant—it’s full of lessons, surprises, and growth.\n\n💫 *Message:* Embrace flexibility—your soul learns through exploration and new horizons.",

        6: "💞 *Vibration 6 – The Nurturer*\n\nYour name carries the loving, healing energy of service and care. "
           "You are drawn to creating harmony in relationships, family, and community. "
           "This vibration is deeply connected to responsibility and compassion.\n\n💫 *Message:* Your purpose flows through love, beauty, and emotional balance.",

        7: "🔮 *Vibration 7 – The Spiritual Seeker*\n\nYour name resonates with wisdom, introspection, and deep intuition. "
           "You are naturally drawn to learning, reflection, and uncovering life’s hidden truths. "
           "This vibration connects you strongly with your inner world.\n\n💫 *Message:* Trust the quiet moments—your soul speaks through stillness.",

        8: "💼 *Vibration 8 – The Manifestor of Power*\n\nYour name vibrates with ambition, success, and material mastery. "
           "You are here to create abundance and influence while balancing integrity with achievement. "
           "This vibration carries lessons in leadership and responsibility.\n\n💫 *Message:* Step into your power—your soul is ready to create lasting impact.",

        9: "🌈 *Vibration 9 – The Humanitarian*\n\nYour name carries the energy of compassion, wisdom, and emotional depth. "
           "You are here to serve, heal, and inspire others with your heart-centered presence. "
           "This vibration is deeply spiritual and artistic.\n\n💫 *Message:* Your soul shines brightest when you give selflessly and trust the flow of love.",

        11: "⚡ *Master Vibration 11 – The Spiritual Messenger*\n\nYour name holds a powerful, intuitive vibration. "
             "It reflects a soul that came to awaken and inspire others. "
             "You carry heightened sensitivity, insight, and a divine connection to higher truths.\n\n💫 *Message:* Your presence alone uplifts others—trust your light and share it bravely.",

        22: "🏗 *Master Vibration 22 – The Master Builder*\n\nYour name carries a rare, powerful vibration capable of manifesting big visions. "
             "You are here to combine spiritual wisdom with practical action to create something meaningful for the world.\n\n💫 *Message:* Dream boldly—your soul can turn visions into reality.",

        33: "🌟 *Master Vibration 33 – The Teacher of Love*\n\nYour name vibrates with unconditional love, healing, and compassion. "
             "You are a guiding light meant to nurture and uplift others through your wisdom and presence.\n\n💫 *Message:* You are here to be love in action—your soul is a channel for divine healing."
    }

    meaning = meanings.get(number, "✨ Your name carries a unique, mysterious vibration guiding you toward your soul’s higher purpose.")

    return (
        f"🔤 *Name Vibration Decoder*\n\n"
        f"✨ *Your Name:* {full_name}\n"
        f"📊 *Vibration Number:* {number}\n\n"
        f"{meaning}\n\n"
        f"🌟 *As a Premium member, you can also explore your **Angel Numbers, Personal Year Forecast, and Moon Energy** "
        f"to see how your name vibration aligns with your soul journey.*"
    )
