from datetime import datetime


def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Функция возвращает новый список словарей, содержащий только те словари,
    у которых ключ state соответствует указанному значению
    """
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: list[dict], descending: bool = True) -> list[dict]:
    """
    Функция, которая сортирует список словарей
    и возвращать новый список, отсортированный по дате
    """

    def get_datetime(item: dict) -> datetime:
        return datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S.%f")

    sorted_data = sorted(data, key=get_datetime, reverse=descending)

    return sorted_data
