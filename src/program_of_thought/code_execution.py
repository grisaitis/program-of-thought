import json
import logging
import re
import subprocess
import sys

from dspy.primitives.python_interpreter import PythonInterpreter

logger = logging.getLogger(__name__)


def execute_code(code: str) -> tuple[str | None, str | None]:
    logger.info("Starting Python interpreter.")
    interpreter = PythonInterpreter()
    try:
        logger.info("Executing code:\n%s", code)
        output = json.dumps(interpreter.execute(code))
        logger.info("Code execution output:\n%s", output)
        return output, None
    except Exception as e:
        return None, str(e)


def execute_code_subprocess(code: str) -> tuple[str, str]:
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True
    )
    stdout = result.stdout or ""
    stderr = result.stderr or ""
    return stdout, stderr


def parse_code(code_data) -> tuple[str, str | None]:
    code = code_data.get("generated_code", "").split("---", 1)[0].split("\n\n\n", 1)[0]
    code_match = re.search(r"```python[ \n](.*?)[ \n]```?", code, re.DOTALL)
    code_block = (code_match.group(1) if code_match else code).replace("\\n", "\n")
    if "\n" not in code_block and code_block.count("=") > 1:
        return code, "Error: Code format is not correct."
    lines = code_block.split("\n")
    last_line_match = re.match(r"^(\w+)\s*=", lines[-1].strip())
    if last_line_match and len(lines) > 1:
        code_block += "\n" + last_line_match.group(1)
    else:
        code_block = re.sub(
            r"([a-zA-Z_]\w* *=.*?)(?=[a-zA-Z_]\w* *=)",
            r"\1\n",
            code_block,
        )
        code_block = re.sub(
            r"([a-zA-Z_]\w* *=.*?)([a-zA-Z_]\w*)$",
            r"\1\n\2",
            code_block,
        )
    if not code_block:
        return code, "Error: Empty code after parsing."
    return code_block, None
