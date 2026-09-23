import os

# Must be set before pydantic_ai is imported so it suppresses the
# framework's startup banner.
os.environ.setdefault("PYDANTIC_AI_NO_BANNER", "1")

from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider

from agent_tools import calculate, get_current_time, read_notes, save_note, should_exit
from extras import MARKDOWN_INSTRUCTIONS, Spinner, strip_markdown


@Spinner("Loading agent")
def build_agent() -> Agent:
    model = OllamaModel(
        "qwen3:8b",
        provider=OllamaProvider(base_url="http://localhost:11434/v1"),
    )

    agent = Agent(
        model,
        tools=[get_current_time, calculate, read_notes, save_note],
        instructions=(
            "You are a helpful personal assistant running 100% locally. "
            "Use your tools whenever they can help answer the questions. "
            "Keep your answers short and friendly. " + MARKDOWN_INSTRUCTIONS
        ),
    )

    @agent.output_validator
    def ensure_plain_text(output: str) -> str:
        return strip_markdown(output)

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
            print(f"Agent: {result.output}")
        except (EOFError, KeyboardInterrupt):
            # Ctrl+D raises EOFError, Ctrl+C raises KeyboardInterrupt.
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
