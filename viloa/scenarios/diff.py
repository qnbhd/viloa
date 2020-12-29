import json
import os

import colorama

from viloa.scenarios.scenario import Scenario
from viloa.utils.repomixin import RepoMixin
from datetime import datetime

from viloa.utils.snapshot import Snapshot
from viloa import print_yellow, print_red, print_default
from viloa.utils.differencer import Differencer
from viloa import logger


class Diff(Scenario, RepoMixin):

    def __init__(self, args):
        Scenario.__init__(self, args)
        RepoMixin.__init__(self, args)

    def run(self):
        if not self.is_initialized():
            logger.error(f"Repo {self.repo} isn't initialized")
            return

        changes = self.get_difference()
        if not changes:
            return
        for file, essence in changes.items():
            print_yellow(f"File {file} was changed")
            colored_essence = Differencer.colored_output(essence)
            for ess in colored_essence:
                print_default(ess)

    def get_difference(self):
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

        def _extract(snap_):
            return {(file_, file_dict_["sha1hash"])
                    for file_, file_dict_ in snap_["files"].items()}

        with open(last_snapshot) as fin:
            last_snap = json.loads(fin.read())
            cur_items = _extract(cur_snap)
            last_items = _extract(last_snap)
            diff = cur_items.difference(last_items)
        if not diff:
            return {}

        changes = {}

        for file, _ in diff:
            filename = file.split(f"{self.repo}\\")[1]
            with open(file) as new_in:
                with open(
                        os.path.join(self.viloa_dir, self.SKELETON_DIR, filename)
                ) as old_in:
                    old = old_in.read()
                    new = new_in.read()
                    essence = Differencer(old, new).process()
                    changes[file] = essence

        return changes

    def get_clear_difference(self):
        changes = self.get_difference()
        cleared = {}
        for file, changes_list in changes.items():
            cleared[file] = []
            for change in changes_list:
                if change[1] == "eq":
                    continue
                cleared[file].append(change)

        return cleared
