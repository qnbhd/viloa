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

        changes = self.get_clear_difference()
        if not changes:
            return
        for file, essence in changes.items():
            print_yellow(f"File {file} was changed")
            colored_essence = Differencer.colored_output(essence)
            for ess in colored_essence:
                print_default(ess)

    def _find_last_snapshot(self):
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
        return os.path.join(self.viloa_dir, last_snapshot)

    @staticmethod
    def _get_changed_files(last_snapshot, current_snapshot):
        def extract(snap_):
            return {(file_, file_dict_["sha1hash"])
                    for file_, file_dict_ in snap_["files"].items()}

        cur_items = extract(current_snapshot)
        last_items = extract(last_snapshot)
        diff = cur_items.difference(last_items)
        return diff

    def _get_stripped_filename(self, file):
        return file.split(f"{self.repo}\\")[1]

    def get_difference(self):
        last_snapshot_file = self._find_last_snapshot()
        current_snapshot = Snapshot.get_snap(self.repo, self.viloa_dir)

        with open(last_snapshot_file) as last:
            last_snapshot = json.loads(last.read())
            changed_files = self._get_changed_files(
                last_snapshot, current_snapshot
            )

        changes = dict()
        for file, _ in changed_files:
            filename = self._get_stripped_filename(file)
            skeleton = os.path.join(self.viloa_dir, self.SKELETON_DIR, filename)
            with open(file) as new_in:
                with open(skeleton) as old_in:
                    old = old_in.read()
                    new = new_in.read()
                    essence = Differencer(old, new).process()
                    changes[file] = essence

        return changes

    @staticmethod
    def _is_skip(change):
        return change[1] == " "

    def get_clear_difference(self):
        changes = self.get_difference()
        cleared = dict()
        for file, changes_list in changes.items():
            cleared[file] = list()
            for change in changes_list:
                if self._is_skip(change):
                    continue
                cleared[file].append(change)

        return cleared
