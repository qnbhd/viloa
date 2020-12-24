import os


class RepoMixin:

    def __init__(self, args):
        self.repo = args.repo
        self.viloa_dir = os.path.join(self.repo, ".viloa")

    def is_initialized(self):
        return os.path.isdir(self.viloa_dir)
