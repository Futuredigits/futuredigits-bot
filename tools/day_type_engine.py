# tools/day_type_engine.py
from datetime import datetime
from typing import Literal

DayType = Literal[
    "pressure",
    "opportunity",
    "risk",
    "conflict",
    "preparation",
    "transition",
    "quiet_power",
]

# --- Universal Day Number ---
def _reduce_to_1_9(n: int) -> int:
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def get_universal_day_number(date: datetime) -> int:
    digits = f"{date.day:02d}{date.month:02d}{date.year}"
    total = sum(int(d) for d in digits)
    return _reduce_to_1_9(total)


# --- Base mapping ---
BASE_DAY_MAP: dict[int, DayType] = {
    1: "opportunity",
    2: "conflict",
    3: "opportunity",
    4: "preparation",
    5: "risk",
    6: "quiet_power",
    7: "quiet_power",
    8: "pressure",
    9: "transition",
}


# --- Weekday modifier ---
# Python weekday(): Monday=0 ... Sunday=6
def apply_weekday_modifier(base: DayType, weekday: int) -> DayType:
    # Monday: pressure / preparation bias
    if weekday == 0 and base in {"preparation", "pressure"}:
        return "pressure"

    # Tuesday: opportunity/action bias
    if weekday == 1 and base == "preparation":
        return "opportunity"

    # Wednesday: transition overlay
    if weekday == 2 and base in {"opportunity", "pressure"}:
        return "transition"

    # Thursday: opportunity + money tone (still opportunity)
    if weekday == 3 and base == "opportunity":
        return "opportunity"

    # Friday: risk / conflict amplification
    if weekday == 4 and base in {"risk", "conflict"}:
        return "risk"

    # Saturday: soften pressure/risk
    if weekday == 5 and base in {"pressure", "risk"}:
        return "quiet_power"

    # Sunday: slow opportunity
    if weekday == 6 and base == "opportunity":
        return "preparation"

    return base


def get_day_type(date: datetime) -> DayType:
    universal = get_universal_day_number(date)
    base_type = BASE_DAY_MAP[universal]
    weekday = date.weekday()
    return apply_weekday_modifier(base_type, weekday)
