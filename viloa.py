import argparse

from viloa.scenarios.diff import Diff
from viloa.scenarios.init import Init

INIT_SCENARIO = "init"
DIFF_SCENARIO = "diff"

parser = argparse.ArgumentParser(description="Parse viloa args")
subparsers = parser.add_subparsers(
    help='sub-command help',
    dest="scenario"
)
parser.add_argument(
    "--repo",
    required=True,
    help="repo dir to init"
)

init = subparsers.add_parser(
    INIT_SCENARIO,
    help="init command"
)

diff = subparsers.add_parser(
    DIFF_SCENARIO,
    help="diff command"
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


if __name__ == '__main__':
    arguments = parser.parse_args()
    viloa = Viloa(arguments)
    viloa.main()
