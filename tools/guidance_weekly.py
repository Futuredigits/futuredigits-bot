# tools/guidance_weekly.py
from datetime import datetime, timedelta
from typing import Literal

from localization import TRANSLATIONS
from tools.day_type_engine import get_day_type, DayType

WeekKind = Literal[
    "pressure_week",
    "opportunity_week",
    "risk_week",
    "conflict_week",
    "preparation_week",
    "transition_week",
    "mixed_week",
]

DAYTYPE_SCORE: dict[DayType, int] = {
    # Higher = "heavier / more caution"
    "risk": 3,
    "conflict": 3,
    "pressure": 2,
    "transition": 2,
    "preparation": 1,
    "quiet_power": 1,
    "opportunity": 0,
}

WEEK_KIND_BY_DOMINANT: dict[DayType, WeekKind] = {
    "pressure": "pressure_week",
    "opportunity": "opportunity_week",
    "risk": "risk_week",
    "conflict": "conflict_week",
    "preparation": "preparation_week",
    "transition": "transition_week",
    "quiet_power": "mixed_week",   # quiet power usually supports others, not “the week theme”
}

def _t(loc: str, key: str, fallback: str = "") -> str:
    return (TRANSLATIONS.get(loc, {}) or {}).get(key) or (TRANSLATIONS.get("en", {}) or {}).get(key) or fallback

def _weekday_label(loc: str, dt: datetime) -> str:
    # Use locale file labels if you have them; fallback to English weekday names
    # Optional keys you can add later: weekday_mon ... weekday_sun
    key_map = ["weekday_mon","weekday_tue","weekday_wed","weekday_thu","weekday_fri","weekday_sat","weekday_sun"]
    key = key_map[dt.weekday()]
    fallback = dt.strftime("%A")
    return _t(loc, key, fallback)

def _start_of_week(now: datetime) -> datetime:
    # Monday as start (0)
    return now - timedelta(days=now.weekday())

def compute_week_plan(date: datetime) -> dict:
    """
    Returns a dict with:
      - days: list[{date, day_type, score}]
      - dominant_type: DayType
      - week_kind: WeekKind
      - best_day: datetime
      - worst_day: datetime
    """
    start = _start_of_week(date)
    days = []
    counts: dict[DayType, int] = {k: 0 for k in DAYTYPE_SCORE.keys()}

    for i in range(7):
        d = start + timedelta(days=i)
        dt: DayType = get_day_type(d)
        score = DAYTYPE_SCORE[dt]
        days.append({"date": d, "day_type": dt, "score": score})
        counts[dt] += 1

    # Dominant type = most frequent; tie-breaker by "heavier" score
    dominant_type = max(
        counts.keys(),
        key=lambda k: (counts[k], DAYTYPE_SCORE[k])
    )

    # If week is very mixed (no type appears >=2), mark as mixed
    max_count = max(counts.values())
    if max_count < 2:
        week_kind: WeekKind = "mixed_week"
    else:
        week_kind = WEEK_KIND_BY_DOMINANT.get(dominant_type, "mixed_week")

    # Best day: lowest score; tie-breaker: opportunity > quiet_power > preparation > transition > pressure > conflict/risk
    priority_best = {
        "opportunity": 0,
        "quiet_power": 1,
        "preparation": 2,
        "transition": 3,
        "pressure": 4,
        "conflict": 5,
        "risk": 6,
    }
    best = min(days, key=lambda x: (x["score"], priority_best[x["day_type"]]))
    worst = max(days, key=lambda x: (x["score"], -priority_best[x["day_type"]]))

    return {
        "days": days,
        "dominant_type": dominant_type,
        "week_kind": week_kind,
        "best_day": best["date"],
        "best_type": best["day_type"],
        "worst_day": worst["date"],
        "worst_type": worst["day_type"],
    }

def get_week_map(*, user_id: int, locale: str, premium: bool = False) -> str:
    loc = (locale or "en").lower()
    now = datetime.now()

    plan = compute_week_plan(now)

    title = _t(loc, "week_title_new", "📅 This Week")
    best_day = _weekday_label(loc, plan["best_day"])
    worst_day = _weekday_label(loc, plan["worst_day"])

    kind = plan["week_kind"]
    key = f"week_{kind}_{'premium' if premium else 'free'}"
    template = _t(loc, key, "")

    if not template:
        # Safe fallback
        template = (
            "🟢 Strong day: *{best_day}*\n"
            "🔴 Caution day: *{worst_day}*"
        )

    text = template.format(best_day=best_day, worst_day=worst_day)

    if premium:
        return f"{title}\n\n{text}"
    else:
        hook = _t(loc, "week_free_hook", "🔒 Premium explains why these days matter for you and what shifts next week.")
        return f"{title}\n\n{text}\n\n{hook}"

