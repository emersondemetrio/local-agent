import os

os.environ.setdefault("PYDANTIC_AI_NO_BANNER", "1")

from pydantic_ai import Agent, NativeOutput
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

from agent_tools import calculate, get_current_time, read_notes, save_note, should_exit
from extras import Spinner
from schemas import PlainTextReply


@Spinner("Loading agent")
def build_agent() -> Agent:
    model = OllamaModel(
        "gemma4:e4b",
        provider=OllamaProvider(base_url="http://localhost:11434/v1"),
    )

    agent = Agent(
        model,
        tools=[get_current_time, calculate, read_notes, save_note],
        output_type=NativeOutput(PlainTextReply),
        instructions=(
            "You are a helpful personal assistant running 100% locally. "
            "Use your tools whenever they can help answer the questions. "
            "Do not use emojis. "
            "Keep your answers short and friendly, and write in plain prose."
        ),
    )

    return agent


@Spinner("Agent is thinking")
def ask(agent: Agent, user_input: str, history: list):
    return agent.run_sync(user_input, message_history=history)


def main():
    agent = build_agent()

    print("Ollama Local Agent. Type quit to exit (or press Ctrl+D).")
    history = []

    while True:
        try:
            user_input = input("You: ")

            if should_exit(user_input):
                print("Goodbye!")
                break

            result = ask(agent, user_input, history)

            history = result.all_messages()
            print(f"Agent: {result.output.reply}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
