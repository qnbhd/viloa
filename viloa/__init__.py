import logging
import colorama
from functools import wraps

logging.basicConfig(format='[%(asctime)s] - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

colorama.init()


def set_color(color):
    def worker(func):
        def wrapper(*args, **kwargs):
            print(color, end='')
            func(*args, **kwargs)

        return wrapper

    return worker


@set_color(colorama.Fore.GREEN)
def print_green(*args, **kwargs):
    print(*args, **kwargs)


@set_color(colorama.Fore.YELLOW)
def print_yellow(*args, **kwargs):
    print(*args, **kwargs)


@set_color(colorama.Fore.RED)
def print_red(*args, **kwargs):
    print(*args, **kwargs)
