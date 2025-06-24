import argparse
import sys

from .core import greet
from .program_of_thought import program_of_thought


def main():
    parser = create_arg_parser()

    args = parser.parse_args()

    if args.command == "greet":
        result = greet(args.name, args.uppercase)
        print(result)
    elif args.command == "program_of_thought":
        result = program_of_thought(args.prompt)
        print(result)


def create_arg_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="program-of-thought",
        description="Program of Thought CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    greet_parser = subparsers.add_parser("greet", help="Greet a user")
    greet_parser.add_argument("name", type=str, help="Name of the user to greet")
    greet_parser.add_argument(
        "--uppercase", action="store_true", help="Convert greeting to uppercase"
    )

    ask_parser = subparsers.add_parser("ask", help="Ask a question")
    ask_parser.add_argument("prompt", type=str, help="Prompt to ask")

    parser.add_argument(
        "--logging-level",
        type=str,
        default="INFO",
        help="Set logging level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )

    return parser


if __name__ == "__main__":
    sys.exit(main())
