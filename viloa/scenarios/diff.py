import json
import os

from viloa.scenarios.scenario import Scenario
from viloa.utils.repomixin import RepoMixin
from datetime import datetime

from viloa.utils.snapshot import Snapshot
from viloa import print_yellow
from viloa.utils.differencer import Differencer
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
        SPAN_VILOA = os.path.join(self.viloa_dir, self.SKELETON_DIR)

        for root, _, files in self.excluded_walk(
            self.viloa_dir, [SPAN_VILOA], [SPAN_VILOA]
        ):
            for file in files:
                snapname, *_ = file.split('.')
                date = datetime.strptime(snapname, "%d-%m-%Y-%H-%M-%S")
                if date > last:
                    last = date
                    last_snapshot = file

        last_snapshot = os.path.join(self.viloa_dir, last_snapshot)
        cur_snap = Snapshot.get_snap(self.repo, self.viloa_dir)
        diff = None
        with open(last_snapshot) as fin:
            last_snap = json.loads(fin.read())
            cur_items = set(cur_snap.items())
            last_items = set(last_snap.items())
            diff = cur_items.difference(last_items)
        if not diff:
            return

        for file, _ in diff:
            print_yellow(f"File {file} was changed")
            filename = file.split(f"{self.repo}\\")[1]
            with open(file) as new_in:
                with open(os.path.join(self.viloa_dir, self.SKELETON_DIR, filename)) as old_in:
                    old = old_in.read()
                    new = new_in.read()
                    essence = Differencer(old, new).process()
                    colored_essence = Differencer.colored_output(essence)
                    for ess in colored_essence:
                        print(ess)
