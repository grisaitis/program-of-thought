import argparse
import logging
import sys

from .code_execution import execute_code
from .core import run_program_of_thought
from .evaluation import optimize_program_and_save
from .other import test_lm
from .utils import setup_logging

logger = logging.getLogger(__name__)


def main():
    parser = create_arg_parser()

    args = parser.parse_args()

    setup_logging(args.logging_level)

    logger.debug("Parsed arguments: %s", args)

    if args.command == "ask":
        result = run_program_of_thought(args.prompt)
        print(result)
    elif args.command == "test-lm":
        result = test_lm()
        print(result)
    elif args.command == "eval":
        result = optimize_program_and_save()
        print(result)
    elif args.command == "code-execution":
        if not args.code:
            raise ValueError("Code argument is required for code-execution command.")
        stdout, stderr = execute_code(args.code)
        print("STDOUT:", stdout)
        print("STDERR:", stderr)
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
    subparsers.add_parser("test-lm", help="Test the language model")
    ask_parser = subparsers.add_parser("ask", help="Ask a question")
    ask_parser.add_argument("prompt", type=str, help="Prompt to ask")
    subparsers.add_parser("evaluation")
    parser_code_execution = subparsers.add_parser("code-execution")
    parser_code_execution.add_argument("code")
    return parser


if __name__ == "__main__":
    sys.exit(main())
