def calculate_expression_number(name: str) -> int:
    name = name.upper()
    letters = {
        'A': 1, 'J': 1, 'S': 1,
        'B': 2, 'K': 2, 'T': 2,
        'C': 3, 'L': 3, 'U': 3,
        'D': 4, 'M': 4, 'V': 4,
        'E': 5, 'N': 5, 'W': 5,
        'F': 6, 'O': 6, 'X': 6,
        'G': 7, 'P': 7, 'Y': 7,
        'H': 8, 'Q': 8, 'Z': 8,
        'I': 9, 'R': 9
    }

    total = sum(letters.get(ch, 0) for ch in name if ch.isalpha())

    def reduce(n):
        if n in {11, 22, 33}:
            return n
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n

    return reduce(total)


def get_expression_result(number: int) -> str:
    results = {
        1: "🔥 *Expression 1 – The Trailblazer*\n\nYou were born to lead, initiate, and stand on your own. With natural confidence and originality, you have the strength to overcome obstacles and break new ground. You may resist authority — because you were born to be it. You thrive when taking bold action aligned with your vision.",
        2: "🌸 *Expression 2 – The Peacemaker*\n\nYour soul speaks the language of sensitivity, grace, and collaboration. You’re not here to dominate — you’re here to unify. Your gifts lie in intuition, diplomacy, and creating emotional safety. People feel calmer around you. Harmony is your calling, and love is your true power.",
        3: "🎭 *Expression 3 – The Creative Voice*\n\nYou’re blessed with expressive charm, humor, and a vivid imagination. Communication is your gift — whether through words, art, or performance. You’re here to uplift and inspire through joy. When you trust your unique voice, you become a beacon of light to others.",
        4: "🏗 *Expression 4 – The Foundation Builder*\n\nYour talents lie in structure, practicality, and discipline. You are the one who turns dreams into tangible form. Others rely on your consistency and clear thinking. You thrive in systems, plans, and step-by-step growth. Your legacy is built through hard work and honesty.",
        5: "✈️ *Expression 5 – The Adventurer*\n\nFreedom, variety, and exploration are embedded in your soul. You’re quick-thinking, adaptable, and born to experience life in its full spectrum. Routine is your prison — movement is your medicine. You express best when life is flowing and new stories are unfolding.",
        6: "💞 *Expression 6 – The Compassionate Healer*\n\nYou are called to serve, protect, and create beauty. With a strong sense of responsibility and a loving heart, you attract others who need your care. You thrive in roles of service, family, healing, and artistry. Love, loyalty, and harmony are the essence of your gift.",
        7: "🔮 *Expression 7 – The Inner Sage*\n\nYour nature is analytical, spiritual, and deeply intuitive. You are here to ask the big questions and search for higher truths. Often introspective and private, you find strength in solitude. Wisdom is your true expression — share it when ready.",
        8: "💼 *Expression 8 – The Manifestor of Power*\n\nYou possess the inner drive, ambition, and strategic mind to achieve great things. Business, influence, and leadership are natural expressions of your purpose. Money is a tool, not a master. When you lead with integrity, success becomes service.",
        9: "🌈 *Expression 9 – The Inspired Humanitarian*\n\nYou carry the soul of an artist, healer, and visionary. Compassion, beauty, and global consciousness flow through your energy. You’re here to serve and elevate humanity through wisdom, art, and emotional depth. Release the past — your heart is your compass.",
        11: "⚡ *Expression 11 – The Spiritual Illuminator*\n\nYou are here to awaken others. Your gifts lie in insight, inspiration, and intuitive brilliance. You may walk a path of extremes — but you were born to rise above. When you embrace your light, you become a channel for divine truth.",
        22: "🏛 *Expression 22 – The Master Architect*\n\nYou were born with extraordinary potential. Practical and visionary, you have the ability to create lasting systems that uplift others. This number carries both burden and blessing — but when you focus your energy, you can shape the world.",    
        33: "🌟 *Expression 33 – The Divine Teacher*\n\nYours is the highest path of service and unconditional love. You are here to nurture, heal, and uplift through wisdom, compassion, and creativity. When you surrender ego and embrace selfless purpose, your presence becomes transformative."
    }


    text = results.get(number, "⚠️ An error occurred while calculating your Expression Number.")
    return text + "\n\n🔓 *Want deeper insight? Try Expression or Destiny in Premium Tools!*"
