# tools/angel_numbers.py

def decode_angel_number(num: str) -> str:
    meanings = {
        "111": (
            "✨ *111 – Divine Alignment*\n\n"
            "When you see 111, it’s a cosmic sign that your thoughts and intentions are rapidly manifesting into reality. "
            "The universe is amplifying your focus, so keep your mind aligned with what you truly desire. "
            "This is a powerful reminder that your inner world is shaping your outer world.\n\n"
            "💫 *Message for you:* Trust the flow of new beginnings. Stay mindful of your thoughts, for they are seeds becoming form."
        ),
        "222": (
            "🌸 *222 – Harmony & Balance*\n\n"
            "Seeing 222 is a reassurance that you are exactly where you need to be. "
            "It’s a call for patience and trust—relationships, decisions, or situations are aligning in divine timing. "
            "Your angels remind you to stay calm and centered as things unfold naturally.\n\n"
            "💫 *Message for you:* What you seek is already on its way. Keep faith and allow balance to restore itself."
        ),
        "333": (
            "🎭 *333 – Divine Support & Creativity*\n\n"
            "The number 333 signals that your spiritual guides, ancestors, and angels are close. "
            "They’re encouraging you to express yourself fully—through words, art, or action. "
            "It’s a powerful time for creativity and self-discovery.\n\n"
            "💫 *Message for you:* You are never alone. Trust your inner voice and share your light with the world."
        ),
        "444": (
            "🛡 *444 – Angelic Protection*\n\n"
            "When you see 444, it means you are surrounded by divine guardianship. "
            "Your angels are building a protective energy around you, especially if you’ve been feeling vulnerable or uncertain. "
            "This number is a sacred reassurance that you are safe and supported.\n\n"
            "💫 *Message for you:* Stand firm—your foundation is strong, and you are guided every step of the way."
        ),
        "555": (
            "🌍 *555 – Transformation & Freedom*\n\n"
            "The number 555 heralds major shifts. "
            "A new chapter is unfolding, bringing freedom from old limitations. "
            "Though change can feel chaotic, it’s guiding you to growth and expansion.\n\n"
            "💫 *Message for you:* Embrace the unknown. What seems like disruption now is actually divine redirection."
        ),
        "666": (
            "💞 *666 – Realignment & Self-Love*\n\n"
            "Contrary to fear-based interpretations, 666 is about finding balance between the material and spiritual. "
            "It’s a reminder to nurture yourself, release worry, and return to your inner truth.\n\n"
            "💫 *Message for you:* Pause and realign. Shift from fear to love, from anxiety to trust."
        ),
        "777": (
            "🔮 *777 – Spiritual Awakening*\n\n"
            "Seeing 777 is a sacred sign of divine wisdom. "
            "It marks a period of spiritual growth, deep intuition, and inner enlightenment. "
            "Mystical forces are guiding you toward higher understanding.\n\n"
            "💫 *Message for you:* Trust the unseen. You are exactly on your soul’s true path."
        ),
        "888": (
            "💰 *888 – Abundance & Power*\n\n"
            "The number 888 represents material and spiritual abundance. "
            "It signals financial blessings, personal power, and karmic rewards flowing your way. "
            "You’re entering a cycle of balance between giving and receiving.\n\n"
            "💫 *Message for you:* Open your arms to prosperity. What you’ve sown is now ready to harvest."
        ),
        "999": (
            "🌈 *999 – Completion & Release*\n\n"
            "When 999 appears, it means a chapter is ending and a new one is ready to begin. "
            "It’s time to release what no longer serves you, forgive the past, and prepare for renewal.\n\n"
            "💫 *Message for you:* Let go gracefully. Every ending carries the seed of a greater beginning."
        )
    }

    return meanings.get(
        num,
        f"✨ *{num} – A Unique Angel Message*\n\n"
        "This number holds a personal vibration for you. Reflect on what you were thinking or feeling when it appeared—"
        "your angels are nudging you to pay attention to the synchronicity around you."
    )
