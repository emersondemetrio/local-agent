# Local Agent

A small, 100% local personal assistant built with [pydantic-ai](https://ai.pydantic.dev/) and [Ollama](https://ollama.com/). No API keys, no cloud calls — the model runs on your own machine.

## Features

- Chats in your terminal using a local Ollama model (`qwen3:8b` by default).
- Built-in tools: get the current time, do basic math, and save/read notes.
- Animated loading spinner while the agent loads and while it's thinking.
- Enforces plain-text replies (no Markdown formatting), with a fallback sanitizer.
- Exits cleanly on `quit`, `exit`, or Ctrl+D.

## Project structure

| File             | Purpose                                                              |
| ---------------- | --------------------------------------------------------------------|
| `main.py`        | Model/agent setup and the chat loop.                                |
| `agent_tools.py` | Tool functions exposed to the agent (time, calculator, notes, exit). |
| `extras.py`      | Non-tool helpers: the `Spinner` and plain-text output sanitizing.   |

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) — used to manage the environment and dependencies
- [Ollama](https://ollama.com/) — runs the local model

### 1. Install uv

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or via a package manager, e.g. `brew install uv` on macOS. Verify with:

```bash
uv --version
```

### 2. Install Ollama

macOS:

```bash
brew install ollama
```

Or download the installer for macOS/Windows from [ollama.com/download](https://ollama.com/download).

Linux:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 3. Start Ollama

On macOS/Windows, the installed Ollama app runs a background service automatically. If it's not running, or on Linux, start the server manually:

```bash
ollama serve
```

Leave that running in its own terminal (or as a background service). By default it listens on `http://localhost:11434`, which is what `main.py` connects to.

### 4. Pull the model

In another terminal:

```bash
ollama pull qwen3:8b
```

This downloads the model used by `main.py`. To use a different model, pull it the same way and update the model name in `build_agent()` in `main.py`.

## Setup

Install the project's dependencies with uv (this also creates the `.venv`):

```bash
uv sync
```

## Running the agent

```bash
uv run python main.py
```

You should see a short "Loading agent" spinner, then a prompt:

```
Ollama Local Agent. Type quit to exit (or press Ctrl+D).
You:
```

Type a message and press Enter. The agent will show a "thinking" spinner while it queries the local model, then reply in plain text.

### Exiting

Any of the following end the session cleanly:

- Type `quit` or `exit`
- Press `Ctrl+D`

### Example session

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

## Configuration

An optional `.env` file can be used for environment variables, for example:

```
PYDANTIC_AI_NO_BANNER=1
```

`PYDANTIC_AI_NO_BANNER=1` is already set by `main.py` itself (before `pydantic_ai` is imported) to suppress pydantic-ai's startup banner, so no extra setup is required — the `.env` value is just there if you want to manage it explicitly.

## Troubleshooting

- **Connection errors / "Ollama not reachable"** — make sure `ollama serve` is running and reachable at `http://localhost:11434`. Check with:

  ```bash
  curl http://localhost:11434/api/tags
  ```

- **Model not found** — make sure you've pulled it: `ollama pull qwen3:8b`.
- **Slow first response** — the first request after starting Ollama loads the model into memory, which can take a while depending on your machine.
