from difflib import ndiff

import colorama
from typing import List, Union, Any


class Differencer:
    ADD_COM = '+'
    DEL_COM = '-'
    SKIP_COM = ' '
    CONCRETE_COM = '?'

    def __init__(self, old, new):
        self.old = old
        self.new = new

    def process(self) -> List[List[Union[int, str]]]:
        old = self.old.splitlines()
        new = self.new.splitlines()

        line: int = 0

        diff = list(ndiff(old, new))
        result = []

        for i in range(len(diff)):
            command: str = diff[i][0]
            ens: str = diff[i].replace('\n', '')

            if command == Differencer.CONCRETE_COM:
                continue
            if command == Differencer.ADD_COM:
                prev_command = result[-1][1]
                if prev_command != Differencer.DEL_COM:
                    line += 1
            else:
                line += 1

            result.append([line, command, ens])

        return result

    @staticmethod
    def colored_output(result):
        def get_print_color(com):
            DEFAULT = ""
            if com == Differencer.ADD_COM:
                return colorama.Fore.GREEN
            elif com == Differencer.DEL_COM:
                return colorama.Fore.RED
            else:
                return DEFAULT

        final = []

        for line, command, ens in result:
            color = get_print_color(command)
            colored_ens = f"{line}: {color + ens}"
            final.append(colored_ens)

        return final
