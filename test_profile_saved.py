import asyncio
from tools.profile_store import get_profile, set_birthdate, set_full_name
from db import redis

async def main():
    uid = 619941697
    await set_birthdate(uid, "04.07.1992")
    await set_full_name(uid, "Dmitrij Test")
    prof = await get_profile(uid)
    print("PROFILE:", prof)

    await redis.aclose()  # ✅ prevents "event loop closed" warning

asyncio.run(main())
