import sys
import traceback
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable], Callable]:
    """Декоратор, автоматически логирующий начало и конец выполнения функции, ее результаты или возникшие ошибки."""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok\n"
            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                message = (
                    f"{func.__name__} error: {e.__class__.__name__}\n"
                    f"Inputs: {args}, {kwargs}\n"
                    f"Traceback:\n{''.join(traceback.format_tb(exc_traceback))}"
                )

            if filename is None:
                print(message)
            else:
                with open(filename, "a") as file:
                    file.write(message)

            if "result" in locals():
                return result

        return wrapper

    return decorator


@log(filename="mylog.txt")
def my_function(x, y):
    return x / y


my_function(1, 0)
