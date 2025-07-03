import logging
import os
from typing import Type, Union

import dspy
from dotenv import load_dotenv
from dspy import ensure_signature
from pydantic.fields import FieldInfo

from .code_execution import execute_code, parse_code

logger = logging.getLogger(__name__)


class ProgramOfThought(dspy.Module):
    def __init__(self, signature: Union[str, Type[dspy.Signature]], max_iters=3):
        super().__init__()
        self.signature: Type[dspy.Signature] = ensure_signature(signature)
        self.max_iters = max_iters

        self.input_fields = self.signature.input_fields
        self.output_fields = self.signature.output_fields

        self.generate_code = dspy.ChainOfThought(self._signature_generate_code)
        self.generate_code_again = dspy.ChainOfThought(
            self._signature_generate_code_again
        )
        self.generate_answer = dspy.ChainOfThought(self._signature_generate_answer)

    @property
    def _signature_generate_code(self) -> Type[dspy.Signature]:
        additional_fields = {
            "generated_code": dspy.OutputField(
                prefix="Code:",
                desc="python code that answers the question",
                format=str,
            ),
        }
        subtask_signature: Type[dspy.Signature] = dspy.Signature(
            self.input_fields | additional_fields
        )
        inputs_as_text = ", ".join(
            [f"`{field_name}`" for field_name in subtask_signature.input_fields]
        )
        outputs_as_text = ", ".join(
            [f"`{field_name}`" for field_name in subtask_signature.output_fields]
        )
        final_outputs_as_text = ", ".join(
            [f"`{field_name}`" for field_name in self.output_fields]
        )
        instructions = "\n".join(
            [
                f"You will be given {inputs_as_text} and you will respond with {outputs_as_text}.",
                f"Generating executable Python code that programmatically computes the correct {outputs_as_text}.",
                "After you're done with the computation and think you have the answer, make sure to provide your answer by calling the preloaded function `final_answer()`.",
                f'You should structure your answer in a dict object, like {{"field_a": answer_a, ...}}, evaluates to the correct value mapping for {final_outputs_as_text}.',
            ]
        )
        return subtask_signature.with_instructions(instructions)

    @property
    def _signature_generate_code_again(self) -> Type[dspy.Signature]:
        additional_fields: dict[str, FieldInfo] = {
            "previous_code": dspy.InputField(
                prefix="Previous Code:",
                desc="previously-generated python code that errored",
                format=str,
            ),
            "error": dspy.InputField(
                prefix="Error:",
                desc="error message from previously-generated python code",
            ),
            "generated_code": dspy.OutputField(
                prefix="Code:",
                desc="python code that answers the question",
                format=str,
            ),
        }
        subtask_signature: Type[dspy.Signature] = dspy.Signature(
            self.input_fields | additional_fields
        )
        inputs_as_text = ", ".join(
            [f"`{field_name}`" for field_name in subtask_signature.input_fields]
        )
        outputs_as_text = ", ".join(
            [f"`{field_name}`" for field_name in subtask_signature.output_fields]
        )
        instructions = "\n".join(
            [
                f"You are given {inputs_as_text} due to an error in previous code.",
                f"Your task is to correct the error and provide the new {outputs_as_text}.",
            ]
        )
        return subtask_signature.with_instructions(instructions)

    @property
    def _signature_generate_answer(self) -> Type[dspy.Signature]:
        additional_fields: dict[str, FieldInfo] = {
            "final_generated_code": dspy.InputField(
                prefix="Code:",
                desc="python code that answers the question",
                format=str,
            ),
            "code_output": dspy.InputField(
                prefix="Code Output:",
                desc="output of previously-generated python code",
            ),
        }
        subtask_signature: Type[dspy.Signature] = dspy.Signature(
            self.input_fields | additional_fields | self.output_fields
        )
        inputs_as_text = ", ".join(
            [f"`{field_name}`" for field_name in subtask_signature.input_fields]
        )
        outputs_as_text = ", ".join(
            [f"`{field_name}`" for field_name in subtask_signature.output_fields]
        )
        instructions = "\n".join(
            [
                f"Given the final code {inputs_as_text}, provide the final {outputs_as_text}.",
            ]
        )
        return subtask_signature.with_instructions(instructions)

    def forward(self, **kwargs):
        inputs = {field_name: kwargs[field_name] for field_name in self.input_fields}
        attempt_counter = 1
        code_data = self.generate_code(**inputs)
        code, error, output = self._parse_and_execute(code_data)
        while error is not None:
            if attempt_counter == self.max_iters:
                raise RuntimeError(
                    f"Max attempts reached. Failed to run ProgramOfThought: {error}"
                )
            inputs.update({"previous_code": code, "error": error})
            code_data = self.generate_code_again(**inputs)
            code, error, output = self._parse_and_execute(code_data)
            attempt_counter += 1
        inputs.update({"final_generated_code": code, "code_output": output})
        answer_gen_result = self.generate_answer(**inputs)
        return answer_gen_result

    def _parse_and_execute(
        self, code_data
    ) -> tuple[str | None, str | None, str | None]:
        code, error = parse_code(code_data)
        if error:
            return code, error, None
        else:
            output, error = execute_code(code)
            return code, error, output


def run_program_of_thought(prompt: str) -> str:
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

    pot = ProgramOfThought("question -> answer", max_iters=3)
    return pot(question=prompt).answer
