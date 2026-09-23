# Local Agent

A small, 100% local personal assistant built with [pydantic-ai](https://ai.pydantic.dev/) and [Ollama](https://ollama.com/). No API keys, no cloud calls.

## Features

- Chats in your terminal using a local Ollama model.
- Tools: current time, basic math, save/read notes.
- Loading spinner while it thinks.
- Replies are schema-enforced plain text, no Markdown.
- Exits clean on `quit`, `exit`, or Ctrl+D.

## Project structure

| File             | Purpose                                      |
| ---------------- | --------------------------------------------- |
| `main.py`        | Model/agent setup and the chat loop.          |
| `agent_tools.py` | Tool functions exposed to the agent.          |
| `extras.py`      | The `Spinner`.                                |
| `schemas.py`     | The plain-text output schema.                 |

## Get running

Install [uv](https://docs.astral.sh/uv/):

```bash
brew install uv
```

Install [Ollama](https://ollama.com/) and pull a model:

```bash
brew install ollama
ollama serve
ollama pull qwen3:8b
```

Install deps and run:

```bash
uv sync
uv run main.py
```

Or use the [Makefile](./Makefile): `make install`, `make run`.

To use a different model, change the model name in `build_agent()` in `main.py`.

## Example

```
You: what time is it?
Agent: It's Tuesday, September 22, 2026 at 11:05 PM.

You: what's 12 * 7?
Agent: 84.

You: save a note to buy milk
Agent: Got it, I saved that note for you.

You: quit
Goodbye!
```

## Dev

Linting/formatting via [ruff](https://docs.astral.sh/ruff/):

```bash
make lint
make format
make check
```

## Config

Optional `.env`:

```
PYDANTIC_AI_NO_BANNER=1
```

Not required, `main.py` sets it itself.

## Reference

[Build a Local AI Agent in 10 Minutes using Python](https://www.youtube.com/watch?v=ByWCsa8DbF8)
