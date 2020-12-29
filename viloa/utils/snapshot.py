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

    def _make(
        self, message: str = "", changes: dict = {}
    ) -> Dict[str, str]:
        snap = dict(
            message=message,
            files={}
        )

        for file in self.files:
            with open(file, "rb") as fin:
                content = fin.read()
                file_dict = dict(
                    sha1hash=hashlib.sha1(content).hexdigest()
                )
                file_dict["changes"] = changes.get(file, None) if changes else None
                snap["files"][file] = file_dict
        return snap

    @staticmethod
    def get_snap(
        repo: str, viloa_dir: str, message: str = "", changes: dict = None
    ):
        snapshot = Snapshot()
        SKELETONS_DIR = os.path.join(viloa_dir, RepoMixin.SKELETON_DIR)

        for root, dirs, files in RepoMixin.excluded_walk(
            repo, [viloa_dir], [SKELETONS_DIR]
        ):
            for file in files:
                path = os.path.join(root, file)
                snapshot.add_file(path)

        return snapshot._make(message, changes)
