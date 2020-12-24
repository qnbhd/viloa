from viloa.scenarios.scenario import Scenario
from viloa.utils.snapshot import Snapshot
import os
import json
from datetime import datetime
from viloa.utils.repomixin import RepoMixin
import logging
from viloa import logger


class Init(Scenario, RepoMixin):

    def __init__(self, args):
        Scenario.__init__(self, args)
        RepoMixin.__init__(self, args)

    def initialize_repo(self):
        os.mkdir(self.viloa_dir)

    def run(self):
        if not self.is_initialized():
            self.initialize_repo()
        else:
            logger.warning(f"Repo {self.repo} was initialized previously")
            return
        snap = Snapshot.get_snap(self.repo, self.viloa_dir)
        time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        with open(os.path.join(self.viloa_dir, time + ".snap"), "w") as fout:
            fout.write(json.dumps(snap, indent=2))
