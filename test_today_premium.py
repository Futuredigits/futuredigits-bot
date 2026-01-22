from localization import load_locales
from tools.guidance_today import get_today_guidance

load_locales()

print(get_today_guidance(user_id=1, locale="en", premium=True))
print()
print(get_today_guidance(user_id=1, locale="ru", premium=True))
