from __future__ import annotations

from typing import Optional, Tuple

from tools.profile_store import get_profile
from tools.life_path import calculate_life_path_number


def get_life_path_group(life_path: int) -> str:
    """
    Group Life Path numbers into a few behavior buckets
    so we can personalize Today without overcomplicating the copy.
    """
    if life_path in (1, 8):
        return "lp_group_lead"
    if life_path in (2, 6, 9):
        return "lp_group_sensitive"
    if life_path in (3, 5):
        return "lp_group_expressive"
    if life_path in (4, 7):
        return "lp_group_inner"
    return "lp_group_inner"


async def get_user_life_path_bias(user_id: int) -> Tuple[Optional[int], Optional[str]]:
    """
    Returns:
        (life_path_number, group_key)
    or
        (None, None) if birthdate is missing or invalid
    """
    profile = await get_profile(user_id)
    birthdate = (profile.get("birthdate") or "").strip()

    if not birthdate:
        return None, None

    try:
        life_path = calculate_life_path_number(birthdate)
        group_key = get_life_path_group(int(life_path))
        return int(life_path), group_key
    except Exception:
        return None, None