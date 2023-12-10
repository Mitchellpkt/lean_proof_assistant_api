import os
import time
from typing import List, Dict, Any

from dotenv import load_dotenv
from openai import OpenAI
from loguru import logger

MAX_BATCH_SIZE = 2048  # Maximum number of texts allowed in a batch

tools: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "verify_lean_proof",
            "description": "Verify the correctness of a Lean proof",
            "parameters": {
                "type": "object",
                "properties": {
                    "proof": {
                        "type": "string",
                        "description": "The content of the Lean proof to verify",
                        "maxLength": 10000,
                    }
                },
                "required": ["proof"],
            },
        },
    }
]
initial_instruction: str = "You will be provided with a proof request, and your task is to (1) write lean code for that proof, (2) return a the code in a JSON format for 'function calling', (3) interpret the response from the API and iterate if necessary. You are dedicated and will keep trying until you achieve success."
chat_model: str = "gpt-4-1106-preview"
temp: float = 0.7
seed: int = 42
verbose: bool = True
max_successive_tries: int = 5


def main():
    # Get the credentials:
    load_dotenv()
    api_key: str = os.environ.get("LLM_API_KEY")

    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key)
    logger.info(f"Client initialized with API key ...{api_key[6:]}\n")

    # Ask user for a system prompt, but have the instruction above be the default
    logger.info(f"Initial system instruction: {initial_instruction}\n")

    # Configure the initial interaction
    # Get a prompt from the user
    time.sleep(0.1)
    prompt: str = input("Enter a prompt: ")
    logger.info("(sending)")

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": initial_instruction},
        {"role": "user", "content": prompt},
    ]

    break_tool_loop: bool = False
    tries: int = 0
    while not break_tool_loop:
        if tries >= max_successive_tries:
            logger.critical(
                f"Could not get working code after {tries} tries; breaking out of loop"
            )
            break_tool_loop = True

        chat_completion = client.chat.completions.create(
            messages=messages,
            model=chat_model,
            seed=seed,
            temperature=temp,
            tools=tools,
        )

        finish_reason: str = chat_completion.choices[0].finish_reason
        if finish_reason == "tool_calls":
            tool_call_id: str = chat_completion.choices[0].message.tool_calls[0].id
            call_string: str = (
                chat_completion.choices[0].message.tool_calls[0].function.arguments
            )
            messages.append(
                {
                    "role": "assistant",
                    "content": call_string,
                    "tool_call_id": tool_call_id,
                    "name": "verify_lean_proof",
                }
            )
            if verbose:
                logger.info(
                    f"{chat_model} requested tool call (ID:{tool_call_id}) {call_string}"
                )

            proof_response = ...  # Here submit the lean proof
            if verbose:
                logger.info(f"Response from proof assistant: {proof_response}")

            messages.append(
                {
                    "role": "tool",
                    "content": proof_response,
                    "name": "verify_lean_proof",
                    "tool_call_id": tool_call_id,
                }
            )
            tries += 1
        elif finish_reason == "stop":
            message_content: str = chat_completion.choices[0].message.content
            messages += [{"role": "assistant", "content": message_content}]
            logger.info(f"GPT: {message_content}")
            break_tool_loop = True
            tries = 0  # reset counter


if __name__ == "__main__":
    main()
