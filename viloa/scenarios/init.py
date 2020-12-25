from viloa.scenarios.scenario import Scenario
from viloa.utils.snapshot import Snapshot
import os
import json
from datetime import datetime
from viloa.utils.repomixin import RepoMixin
import logging
from viloa import logger
import pathlib
import shutil


class Init(Scenario, RepoMixin):

    def __init__(self, args):
        Scenario.__init__(self, args)
        RepoMixin.__init__(self, args)

    def initialize_repo(self):
        os.mkdir(self.viloa_dir)

    def make_span(self):
        VILOA = self.viloa_dir
        SPAN_VILOA = os.path.join(self.viloa_dir, Init.SKELETON_DIR)
        IGNORE_PATHS = [VILOA, SPAN_VILOA]

        def get_file_dir(root_, file_):
            dir_ = os.path.dirname(os.path.join(root_, file_))
            dir_ = dir_.replace(self.repo, '', 1)
            _, dir_ = os.path.split(dir_)
            dir_ = os.path.join(self.viloa_dir, Init.SKELETON_DIR, dir_)
            return dir_

        for root, dirs, files in os.walk(self.repo):
            if root in IGNORE_PATHS:
                continue
            for file in files:
                file_dir = get_file_dir(root, file)
                pathlib.Path(file_dir).mkdir(parents=True, exist_ok=True)
                dest = os.path.join(root, file)
                target = os.path.join(file_dir, file)
                shutil.copy2(dest, target)

    def run(self):
        if not self.is_initialized():
            self.initialize_repo()
        else:
            logger.warning(f"Repo {self.repo} was initialized previously")
        snap = Snapshot.get_snap(self.repo, self.viloa_dir)
        self.make_span()
        time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        with open(os.path.join(self.viloa_dir, time + ".snap"), "w") as fout:
            fout.write(json.dumps(snap, indent=2))
