import os

import dspy
from dotenv import load_dotenv


def greet(name: str, uppercase: bool = False) -> str:
    """Core functionality - greeting function"""
    greeting = f"Hello, {name}!"
    return greeting.upper() if uppercase else greeting


def test_lm() -> str:
    load_dotenv()
    lm = dspy.LM(
        model=os.getenv("TOGETHERAI_API_MODEL", ""),
        api_key=os.getenv("TOGETHERAI_API_KEY", ""),
    )
    dspy.configure(lm=lm)
    results = lm("Say this is a test!", temperature=0.7)  # => ['This is a test!']
    return str(results) if results else "No response from LM"
