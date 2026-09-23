"""Non-model, non-agent helpers for the local agent: the loading spinner
and plain-text output sanitizing."""

import itertools
import re
import sys
import threading
import time
from contextlib import ContextDecorator


# Loading animation
class Spinner(ContextDecorator):
    """Terminal spinner shown while the agent is busy (loading/thinking).

    Works both as a context manager and as a decorator:

        with Spinner("Loading"):
            slow_setup()

        @Spinner("Thinking")
        def ask(question):
            return agent.run_sync(question)
    """

    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    INTERVAL = 0.08

    def __init__(self, message: str = "Thinking"):
        self.message = message
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._spin, daemon=True)

    def _spin(self) -> None:
        for frame in itertools.cycle(self.FRAMES):
            if self._stop_event.is_set():
                break
            sys.stdout.write(f"\r{frame} {self.message}...")
            sys.stdout.flush()
            time.sleep(self.INTERVAL)

    def __enter__(self) -> "Spinner":
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._stop_event.set()
        self._thread.join()
        # Clear the spinner line so the next print starts clean.
        sys.stdout.write("\r" + " " * (len(self.message) + 15) + "\r")
        sys.stdout.flush()


# End Loading animation


# Plain-text output enforcement
MARKDOWN_INSTRUCTIONS = (
    "Respond in plain text only. Do not use Markdown formatting: no "
    "**bold**, *italics*, `code` spans, code fences, # headings, bullet "
    "or numbered lists, or [links](url). Write normal sentences and "
    "paragraphs as you would in a plain chat message."
)


def strip_markdown(text: str) -> str:
    """Fallback sanitizer: strips common Markdown syntax from model output
    in case the model ignores the plain-text instructions."""
    # Code fences: keep the inner content, drop the ``` markers/language tag.
    text = re.sub(r"```[a-zA-Z0-9_+-]*\n?", "", text)
    text = text.replace("```", "")
    # Inline code
    text = re.sub(r"`([^`]+)`", r"\1", text)
    # Bold / italics (order matters: *** then ** then *)
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"\1", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"__(.+?)__", r"\1", text)
    text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"\1", text)
    # Headings
    text = re.sub(r"^\s{0,3}#{1,6}\s+", "", text, flags=re.MULTILINE)
    # Bullet / numbered list markers -> keep the text, drop the marker
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+[.)]\s+", "", text, flags=re.MULTILINE)
    # Links / images: [text](url) or ![text](url) -> "text (url)"
    text = re.sub(r"!?\[([^\]]*)\]\(([^)]+)\)", r"\1 (\2)", text)
    return text.strip()


# End Plain-text output enforcement
