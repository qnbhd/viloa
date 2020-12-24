import json
import os

from viloa.scenarios.scenario import Scenario
from viloa.utils.repomixin import RepoMixin
from datetime import datetime

from viloa.utils.snapshot import Snapshot
from viloa import print_red
from viloa.utils import differencer
from viloa import logger

class Diff(Scenario, RepoMixin):

    def __init__(self, args):
        Scenario.__init__(self, args)
        RepoMixin.__init__(self, args)

    def run(self):
        if not self.is_initialized():
            logger.error(f"Repo {self.repo} isn't initialized")
        last = datetime.utcfromtimestamp(0)
        last_snapshot = None
        for _, _, files in os.walk(self.viloa_dir):
            for file in files:
                without_ext = file.split('.')[0]
                date = datetime.strptime(without_ext, "%d-%m-%Y-%H-%M-%S")
                if date > last:
                    last = date
                    last_snapshot = file
        last_snapshot = os.path.join(self.viloa_dir, last_snapshot)
        cur_snap = Snapshot.get_snap(self.repo, self.viloa_dir)
        diff = None

