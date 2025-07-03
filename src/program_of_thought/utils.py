import logging
import os

import dspy
from dotenv import load_dotenv


def setup_logging(level: str):
    logging.basicConfig(
        level="WARNING",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logging.getLogger("program_of_thought").setLevel(level)


def configure_dspy():
    load_dotenv()
    lm = dspy.LM(
        model=os.getenv("TOGETHERAI_API_MODEL", ""),
        api_key=os.getenv("TOGETHERAI_API_KEY", ""),
    )
    dspy.configure(lm=lm)
