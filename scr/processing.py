from datetime import datetime


def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция, которая принимает список словарей"""

    return [item for item in data if item.get("state") == state]


def sort_by_date(data: list[dict], order: bool = True) -> list[dict]:
    """Функция, которая сортирует список словарей"""

    def get_datetime(item: dict) -> datetime:
        return datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S.%f")

    if order.lower() == "ascending":
        sorted_data = sorted(data, key=get_datetime)
    else:
        sorted_data = sorted(data, key=get_datetime, reverse=True)

    return sorted_data
