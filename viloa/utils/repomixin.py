import os
import pathlib
import shutil
from datetime import datetime


class RepoMixin:
    VILOA_DIR = ".viloa"
    SKELETON_DIR = ".skeleton"
    SNAPSHOT_EXT = ".snap"
    JSON_INDENT_LEVEL = None

    def __init__(self, args=None):
        if args:
            self.repo = args.repo
            self.viloa_dir = os.path.join(self.repo, RepoMixin.VILOA_DIR)

    def is_initialized(self) -> bool:
        return os.path.isdir(self.viloa_dir)

    @staticmethod
    def excluded_walk(path, excluded_paths=(), excluded_prefixes=()):
        def in_excluded(root_):
            if root_ in excluded_paths:
                return True
            for excluded in excluded_prefixes:
                if root_.find(excluded) != -1:
                    return True
            return False

        for root, dirs, files in os.walk(path):
            if in_excluded(root):
                continue
            yield root, dirs, files

    def _get_snap_filename(self, time: datetime) -> str:
        return time.strftime("%d-%m-%Y-%H-%M-%S") + self.SNAPSHOT_EXT

    def _get_file_dir(self, root_: str, file_: str) -> str:
        dirname = os.path.dirname(os.path.join(root_, file_))
        dirname = dirname.replace(self.repo, '', 1)
        _, dirname = os.path.split(dirname)
        dirname = os.path.join(self.viloa_dir, self.SKELETON_DIR, dirname)
        return dirname

    def make_span(self):
        VILOA = self.viloa_dir
        SPAN_VILOA = os.path.join(self.viloa_dir, self.SKELETON_DIR)
        IGNORE_PATHS = [VILOA, SPAN_VILOA]

        for root, dirs, files in self.excluded_walk(self.repo, IGNORE_PATHS, IGNORE_PATHS):
            for file in files:
                dirname = self._get_file_dir(root, file)
                pathlib.Path(dirname).mkdir(parents=True, exist_ok=True)
                dest = os.path.join(root, file)
                target = os.path.join(dirname, file)
                shutil.copy2(dest, target)
