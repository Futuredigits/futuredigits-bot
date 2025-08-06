def calculate_life_path_number(date_str: str) -> int:
    try:
        day, month, year = map(int, date_str.split('.'))
    except ValueError:
        raise ValueError("Invalid date format. Use DD.MM.YYYY.")
    
    digits = [int(d) for d in f"{day:02d}{month:02d}{year}"]
    total = sum(digits)

    def reduce_to_life_path(n):
        if n in {11, 22, 33}:
            return n
        while n > 9:
            n = sum(int(d) for d in str(n))
        return n

    return reduce_to_life_path(total)


from localization import get_text

def get_life_path_result(number: int, user_id: int) -> str:
    result = get_text("result_life_path", user_id).get(str(number), "⚠️ Life Path result not found.")
    cta = get_text("cta_try_more", user_id)
    return f"{result}\n\n{cta}"

