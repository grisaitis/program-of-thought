import argparse
import logging
import sys

from .core import test_lm
from .program_of_thought import program_of_thought

logger = logging.getLogger()


def main():
    parser = create_arg_parser()

    args = parser.parse_args()

    logging.basicConfig(
        level=args.logging_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger.debug("Parsed arguments: %s", args)

    if args.command == "ask":
        result = program_of_thought(args.prompt)
        print(result)
    elif args.command == "test-lm":
        result = test_lm()
        print(result)
    else:
        raise ValueError(f"Unknown command: {args.command}")


def create_arg_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="program-of-thought",
        description="Program of Thought CLI",
    )
    parser.add_argument(
        "--logging-level", type=str, default="INFO", help="Python logging level"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # subcommand: test-lm
    subparsers.add_parser("test-lm", help="Test the language model")

    # subcommand: ask
    ask_parser = subparsers.add_parser("ask", help="Ask a question")
    ask_parser.add_argument("prompt", type=str, help="Prompt to ask")

    return parser


if __name__ == "__main__":
    sys.exit(main())
