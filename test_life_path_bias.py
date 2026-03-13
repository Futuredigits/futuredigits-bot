import asyncio
from tools.profile_store import set_birthdate
from tools.life_path_bias import get_user_life_path_bias

async def main():
    uid = 619941697  # your Telegram ID
    await set_birthdate(uid, "04.07.1992")
    lp, group_key = await get_user_life_path_bias(uid)
    print("life_path =", lp)
    print("group_key =", group_key)

asyncio.run(main())