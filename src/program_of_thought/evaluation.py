import logging

import dspy
from dspy.datasets.gsm8k import GSM8K, gsm8k_metric

from .core import ProgramOfThought
from .utils import configure_dspy

logger = logging.getLogger(__name__)


configure_dspy()


def print_info_about_gsm8k():
    dataset = GSM8K()
    print(len(dataset.train), len(dataset.dev))
    example = dataset.train[0]
    print("Question:", example.question)
    print("Answer:", example.answer)


def optimize_program_and_save() -> dspy.Module:
    dspy_program = ProgramOfThought("question -> answer")
    dataset = GSM8K()
    trainset = dataset.train[:2]
    optimizer = dspy.BootstrapFewShot(
        metric=gsm8k_metric, max_bootstrapped_demos=4, max_labeled_demos=4, max_rounds=5
    )
    compiled_dspy_program = optimizer.compile(dspy_program, trainset=trainset)
    compiled_dspy_program.save("./program.json", save_program=False)
    return compiled_dspy_program
