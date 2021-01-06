from viloa.scenarios.scenario import Scenario
from viloa.utils.snapshot import Snapshot
import os
import json
from datetime import datetime
from viloa.utils.repomixin import RepoMixin
from viloa import logger


class Init(Scenario, RepoMixin):

    def __init__(self, args):
        Scenario.__init__(self, args)
        RepoMixin.__init__(self, args)

    def initialize_repo(self):
        os.mkdir(self.viloa_dir)

        snap = Snapshot.get_snap(self.repo, self.viloa_dir, "init")
        self.make_skeleton()

        snap_filename = self._get_snap_filename(datetime.now())
        snap_filename = os.path.join(self.viloa_dir, snap_filename)

        with open(snap_filename, "w") as fout:
            fout.write(json.dumps(snap, indent=self.JSON_INDENT_LEVEL))

    def run(self):
        if self.is_initialized():
            logger.warning(f"Repo {self.repo} was initialized previously")
            return

        self.initialize_repo()
