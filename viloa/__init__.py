import logging
import colorama
from functools import wraps

logging.basicConfig(format='[%(asctime)s] - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

colorama.init(autoreset=False)


def set_color(color):
    def worker(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(color, end='')
            func(*args, **kwargs)
            print(colorama.Style.RESET_ALL, end='')

        return wrapper

    return worker

def set_color_new(func=None, *, color=""):

    if func is None:
        return lambda func_: set_color_new(func_, color=color)

    @wraps(func)
    def inner(*args, **kwargs):
        print(color, end='')
        func(*args, **kwargs)
        print(colorama.Style.RESET_ALL, end='')

    return inner


@set_color_new(color=colorama.Fore.GREEN)
def print_green(*args, **kwargs):
    print(*args, **kwargs)


@set_color_new(color=colorama.Fore.YELLOW)
def print_yellow(*args, **kwargs):
    print(*args, **kwargs)


@set_color_new(color=colorama.Fore.RED)
def print_red(*args, **kwargs):
    print(*args, **kwargs)


def print_default(*args, **kwargs):
    print(*args, **kwargs)
    print(colorama.Style.RESET_ALL, end='')
