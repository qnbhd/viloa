import hashlib
import os

from typing import Dict

from viloa.utils.repomixin import RepoMixin


class Snapshot(RepoMixin):

    def __init__(self):
        RepoMixin.__init__(self)
        self.files = []

    def add_file(self, filename: str):
        self.files.append(filename)

    def make(self) -> Dict[str, str]:
        snap = dict()

        for file in self.files:
            with open(file, "rb") as fin:
                content = fin.read()
                sha1hash = hashlib.sha1(content).hexdigest()
                snap[file] = sha1hash

        return snap

    @staticmethod
    def get_snap(repo: str, viloa_dir: str):
        snapshot = Snapshot()
        SKELETONS_DIR = os.path.join(viloa_dir, RepoMixin.SKELETON_DIR)

        for root, dirs, files in RepoMixin.excluded_walk(
            repo, [viloa_dir], [SKELETONS_DIR]
        ):
            for file in files:
                path = os.path.join(root, file)
                snapshot.add_file(path)

        return snapshot.make()
