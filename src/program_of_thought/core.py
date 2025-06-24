def greet(name: str, uppercase: bool = False) -> str:
    """Core functionality - greeting function"""
    greeting = f"Hello, {name}!"
    return greeting.upper() if uppercase else greeting


def program_of_thought(prompt: str) -> str:
    """using dspy to execute a program of thought"""
    return "Placeholder"
