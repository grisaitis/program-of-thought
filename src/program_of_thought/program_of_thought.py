import logging
import os

import dspy
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class GenerateAnswer(dspy.Signature):
    question = dspy.InputField()
    answer = dspy.OutputField()


class ProgramOfThought(dspy.Module):
    """Implements program of throught approach for generating responses.

    Note to self: dspy.Modules implement an inference strategy. I think they work with
    any signature, but I'm not sure.
    """

    pass


def program_of_thought(prompt: str) -> str:
    """
    Generates a response using the Program of Thought approach.

    Args:
        prompt (str): The input prompt to process.
    Returns:
        str: The generated response.
    """
    logger.info("Generating response for prompt: %s", prompt)
    load_dotenv()
    lm = dspy.LM(
        model=os.getenv("TOGETHERAI_API_MODEL", ""),
        api_key=os.getenv("TOGETHERAI_API_KEY", ""),
    )
    dspy.configure(lm=lm)

    pot = dspy.ProgramOfThought(GenerateAnswer)
    return pot(question=prompt).answer
