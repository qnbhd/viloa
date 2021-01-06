import argparse
import json
import os

from viloa.scenarios.scenario import Scenario
from viloa.utils.repomixin import RepoMixin
from viloa import logger
from viloa.utils.snapshot import Snapshot
from viloa.scenarios.diff import Diff
from datetime import datetime


class Commit(Scenario, RepoMixin):

    def __init__(self, args: argparse.Namespace):
        Scenario.__init__(self, args)
        RepoMixin.__init__(self, args)
        self.differ = Diff(args)

    def run(self):
        if not self.is_initialized():
            logger.error(f"Repo {self.repo} isn't initialized")
            return

        changes = self.differ.get_clear_difference()

        snap = Snapshot.get_snap(self.repo, self.viloa_dir, self.args.message, changes)

        snap_filename = self._get_snap_filename(datetime.now())
        snap_filename = os.path.join(self.viloa_dir, snap_filename)

        with open(snap_filename, "w") as fout:
            fout.write(json.dumps(snap, indent=self.JSON_INDENT_LEVEL))

        self.make_skeleton()

