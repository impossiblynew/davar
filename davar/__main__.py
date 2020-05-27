import argparse
from davar.utils import Davar


def main():
    """Allows davar to be used as a commmand line tool
    """
    parser = argparse.ArgumentParser(
        description="Command line tool for the davar experimental intepreted IAL."
    )
    parser.add_argument("davartext", metavar="DAVARTEXT", type=str)
    parser.add_argument(
        "-l", "--lang", required=True, default=None, help="2 character language code.",
    )

    args = parser.parse_args()
    for s in Davar.from_davartext(args.davartext).describe(args.lang):
        print(s)


if __name__ == "__main__":
    main()
