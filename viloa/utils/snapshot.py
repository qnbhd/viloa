import hashlib
import os
from collections import namedtuple


class Snapshot:

    def __init__(self):
        self.files = []

    def add_file(self, file):
        self.files.append(file)

    def make(self):
        snap = dict()
        for file in self.files:
            with open(file, "rb") as fin:
                content = fin.read()
                sha1hash = hashlib.sha1(content).hexdigest()
                snap[file] = dict(
                    content=content.decode("utf-8"),
                    hash=sha1hash
                )
        return snap

    @staticmethod
    def get_snap(repo, viloa_dir):
        snapshot = Snapshot()
        for root, dirs, files in os.walk(repo):
            if root == viloa_dir:
                continue
            for file in files:
                path = os.path.join(root, file)
                snapshot.add_file(path)
        return snapshot.make()
