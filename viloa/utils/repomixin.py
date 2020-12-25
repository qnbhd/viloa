import os


class RepoMixin:

    VILOA_DIR = ".viloa"
    SKELETON_DIR = ".skeleton"
    SNAPSHOT_EXT = ".snap"

    def __init__(self, args=None):
        if args:
            self.repo = args.repo
            self.viloa_dir = os.path.join(self.repo, RepoMixin.VILOA_DIR)

    def is_initialized(self):
        return os.path.isdir(self.viloa_dir)

    @staticmethod
    def excluded_walk(path, excluded_paths=(), excluded_prefixes=()):
        def in_excluded(root_):
            if root_ in excluded_paths:
                return True
            for excl in excluded_prefixes:
                if root_.find(excl) != -1:
                    return True
            return False

        for root, dirs, files in os.walk(path):
            if in_excluded(root):
                continue
            yield root, dirs, files

