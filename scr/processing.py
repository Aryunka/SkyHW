from datetime import datetime


def filter_by_state(data, state="EXECUTED"):

    return [item for item in data if item.get("state") == state]


def sort_by_date(data, order="descending"):
    def get_datetime(item):
        return datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%S.%f")

    if order.lower() == "ascending":
        sorted_data = sorted(data, key=get_datetime)
    else:
        sorted_data = sorted(data, key=get_datetime, reverse=True)

    return sorted_data
