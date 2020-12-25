from difflib import ndiff

import colorama
from typing import List


class Differencer:

    def __init__(self, old, new):
        self.old = old
        self.new = new

    def process(self) -> List[str]:
        ADD_COM = '+'
        DEL_COM = '-'
        SKIP_COM = ' '
        CONCRETE_COM = '?'

        def get_print_color(com):
            DEFAULT = ""
            if com == ADD_COM:
                return colorama.Fore.GREEN
            elif com == DEL_COM:
                return colorama.Fore.RED
            else:
                return DEFAULT

        old = self.old.splitlines(1)
        new = self.new.splitlines(1)

        line = 0

        diff = list(ndiff(old, new))
        result = []

        for i in range(len(diff)):
            command = diff[i][0]
            ens = diff[i].replace('\n', '')

            if command == CONCRETE_COM:
                continue
            if command == ADD_COM:
                prev_command = result[-1][1]
                if prev_command != DEL_COM:
                    line += 1
            else:
                line += 1

            color = get_print_color(command)
            result.append([line, command, color + ens])

        final = []

        for line_, _, diff_ in result:
            final.append(f"{line_}: {diff_}")

        return final
