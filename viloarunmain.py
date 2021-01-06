import argparse

from viloa.scenarios.commit import Commit
from viloa.scenarios.diff import Diff
from viloa.scenarios.init import Init

INIT_SCENARIO = "init"
DIFF_SCENARIO = "diff"
COMMIT_SCENARIO = "commit"

parser = argparse.ArgumentParser(description="Parse viloa args")
parser.add_argument(
    "--repo",
    required=True,
    help="repo dir to init"
)

subparsers = parser.add_subparsers(
    help='existing scenario list',
    dest="scenario"
)
init = subparsers.add_parser(
    INIT_SCENARIO,
    help="initialize your viloa repository"
)

diff = subparsers.add_parser(
    DIFF_SCENARIO,
    help="get difference between last commit and current changes"
)

commit = subparsers.add_parser(
    COMMIT_SCENARIO,
    help="commit your changes"
)
commit.add_argument(
    "--message",
    help="commit message",
    required=True
)


class Viloa:

    def __init__(self, args: argparse.Namespace):
        self.args = args

    def main(self):
        if self.args.scenario == INIT_SCENARIO:
            initer = Init(self.args)
            initer.run()
        if self.args.scenario == DIFF_SCENARIO:
            differ = Diff(self.args)
            differ.run()
        if self.args.scenario == COMMIT_SCENARIO:
            commiter = Commit(self.args)
            commiter.run()


if __name__ == '__main__':
    arguments = parser.parse_args()
    viloa = Viloa(arguments)
    viloa.main()
