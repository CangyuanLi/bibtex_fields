import argparse

from .clean import clean_file

def get_parser():
    parser = argparse.ArgumentParser(description="Clean bibtex file")
    parser.add_argument(
        "filepath",
        type=str,
        help="path to bibtex file"
    )

    parser.add_argument(
        "style",
        type=str,
        nargs="?",
        help="the journal style, aer or jpe",
        default="aer",
        choices=["aer"]
    )

    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        required=False,
        help="suppresses output"
    )

    return parser

def main():
    args = get_parser().parse_args()
    
    clean_file(
        filepath=args.filepath,
        style=args.style,
        quiet=args.quiet
    )

if __name__ == "__main__":
    main()
