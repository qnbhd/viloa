from difflib import ndiff

import colorama


class Differencer:
    ADD_COM = '+'
    DEL_COM = '-'
    EQUAL_COM = ' '
    CONCRETE_COM = '?'

    CUT_POS = 2

    def __init__(self, old, new):
        self.old = old
        self.new = new

    def process(self):
        ndiff_result = list(
            ndiff(self.old.splitlines(), self.new.splitlines())
        )

        line = 0
        difference = []

        for i, change in enumerate(ndiff_result):
            command, *_ = change
            text = change.replace('\n', '')[Differencer.CUT_POS:]

            if command == Differencer.CONCRETE_COM:
                continue

            if command == Differencer.ADD_COM:
                previous_change = difference[-1]
                _line, prev_command, _ens = previous_change
                if prev_command != Differencer.DEL_COM:
                    line += 1
            else:
                line += 1

            result = [line, command, text]
            difference.append(result)

        return difference

    @staticmethod
    def get_print_color(com):
        DEFAULT = ""
        if com == Differencer.ADD_COM:
            return colorama.Fore.GREEN
        elif com == Differencer.DEL_COM:
            return colorama.Fore.RED
        else:
            return DEFAULT

    @staticmethod
    def colored_output(result):
        colored_result = []

        for line, command, ens in result:
            color = Differencer.get_print_color(command)
            colored_result.append(f"{line}: {command} {color + ens}")

        return colored_result
