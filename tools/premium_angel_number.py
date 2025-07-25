def get_angel_number_meaning(number: str) -> str:
    # Clean the number
    num = ''.join(filter(str.isdigit, number))
    
    # Angel number meanings (rich, emotional, spiritual)
    meanings = {
        "111": (
            "✨ *Angel Number 111 – Alignment & New Beginnings*\n\n"
            "You are in perfect alignment with the universe right now. 111 is a divine reminder that your thoughts are creating your reality rapidly. "
            "It’s a sign to stay positive, focus on your intentions, and trust that new beginnings are unfolding for you. 🌱\n\n"
            "💫 *Message:* Be mindful of your inner dialogue—your soul is manifesting what you focus on."
        ),
        "222": (
            "🌸 *Angel Number 222 – Harmony & Divine Timing*\n\n"
            "Seeing 222 means balance is being restored. Trust that everything is unfolding as it should. It’s a sign of partnerships, relationships, and deep emotional healing. "
            "Your angels are asking you to stay patient and trust the timing of your life. 💞\n\n"
            "💫 *Message:* Keep the faith—what you’ve been waiting for is aligning beautifully."
        ),
        "333": (
            "🎨 *Angel Number 333 – Creativity & Spiritual Support*\n\n"
            "The number 333 is a sacred reminder that your spirit guides are close, offering love and guidance. It encourages you to express yourself creatively and share your light. 🌈\n\n"
            "💫 *Message:* Your angels are with you—use your gifts to uplift yourself and others."
        ),
        "444": (
            "🏡 *Angel Number 444 – Stability & Protection*\n\n"
            "444 is a powerful sign of angelic protection. You are surrounded by loving energy, and your foundations are secure. It’s a reminder to keep going—you’re on the right path. 🧱\n\n"
            "💫 *Message:* You are safe, supported, and divinely guided. Trust the process."
        ),
        "555": (
            "💃 *Angel Number 555 – Change & Transformation*\n\n"
            "Seeing 555 means a major shift is coming. This change will free you from what no longer serves you and open the door to something better. ✈️ "
            "Trust the flow of transformation—it’s aligning you with your highest path.\n\n"
            "💫 *Message:* Embrace the unknown—change is your soul’s gateway to growth."
        ),
        "666": (
            "💞 *Angel Number 666 – Balance & Self-Love*\n\n"
            "Despite its misunderstood reputation, 666 is a loving nudge to return to balance. Focus on self-care, harmony, and nurturing your emotional world. 🌿\n\n"
            "💫 *Message:* Align your heart and mind—peace begins within you."
        ),
        "777": (
            "🔮 *Angel Number 777 – Divine Wisdom & Spiritual Awakening*\n\n"
            "777 is a sacred number of spiritual growth and enlightenment. It’s a sign that you are on the right spiritual path and that miracles are aligning for you. 🌌\n\n"
            "💫 *Message:* Trust your intuition—you are in deep alignment with divine guidance."
        ),
        "888": (
            "💼 *Angel Number 888 – Abundance & Power*\n\n"
            "Seeing 888 is a sign that financial and material blessings are flowing toward you. It’s a number of karma, balance, and infinite potential. 💫\n\n"
            "💫 *Message:* Step into your power and receive the abundance you’ve earned."
        ),
        "999": (
            "🌈 *Angel Number 999 – Completion & Release*\n\n"
            "999 signals the end of a chapter. It’s time to release what no longer serves you and prepare for a new beginning. 🌍\n\n"
            "💫 *Message:* Let go with love—your soul is ready for the next evolution."
        )
    }
    
    # If the exact number exists
    if num in meanings:
        meaning = meanings[num]
    else:
        # Default generic meaning
        meaning = (
            f"✨ *Angel Number {num}*\n\n"
            "This number carries a unique vibration for you. It’s a divine sign that your angels are communicating with you, "
            "guiding you toward clarity and alignment. Trust the feelings you have when you see this number—it’s your higher self speaking.\n\n"
            "💫 *Message:* Pay attention to your intuition and the synchronicities unfolding around you."
        )
    
    return (
        f"🪬 *Angel Number Decoder*\n\n"
        f"{meaning}\n\n"
        f"🌟 *As a Premium member, you can also explore your **Moon Energy, Daily Universal Vibe, and Personal Year Forecast** "
        f"to see how this angelic message fits into your bigger soul journey.*"
    )
