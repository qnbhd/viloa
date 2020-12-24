class Differencer:

    def __init__(self, old, new):
        self.old = old
        self.new = new

    def process(self):
        old_lines = self.old.split('\n')
        new_lines = self.new.split('\n')
        difference = []

        for line, old, new in enumerate(zip(old_lines, new_lines)):
            if old != new:
                difference.append((line, old, new))

        return difference
