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

        for root, dirs, files in self.excluded_walk(self.repo, IGNORE_PATHS):
            for file in files:
                dirname = self._get_file_dir(root, file)
                pathlib.Path(dirname).mkdir(parents=True, exist_ok=True)
                dest = os.path.join(root, file)
                target = os.path.join(dirname, file)
                shutil.copy2(dest, target)

    def _get_snap_filename(self, time: datetime) -> str:
        return time.strftime("%d-%m-%Y-%H-%M-%S") + self.SNAPSHOT_EXT

    def _get_file_dir(self, root_: str, file_: str) -> str:
        dirname = os.path.dirname(os.path.join(root_, file_))
        dirname = dirname.replace(self.repo, '', 1)
        _, dirname = os.path.split(dirname)
        dirname = os.path.join(self.viloa_dir, Init.SKELETON_DIR, dirname)
        return dirname

    def run(self):
        if not self.is_initialized():
            self.initialize_repo()
        else:
            logger.warning(f"Repo {self.repo} was initialized previously")

        snap = Snapshot.get_snap(self.repo, self.viloa_dir)
        self.make_span()

        snap_filename = self._get_snap_filename(datetime.now())
        snap_filename = os.path.join(self.viloa_dir, snap_filename)

        with open(snap_filename, "w") as fout:
            fout.write(json.dumps(snap, indent=self.JSON_INDENT_LEVEL))
