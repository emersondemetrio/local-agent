"""Non-model, non-agent helpers for the local agent: the loading spinner."""

import itertools
import sys
import threading
import time
from contextlib import ContextDecorator


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
    UPDATE_INTERVAL = 0.08

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
            time.sleep(self.UPDATE_INTERVAL)

    def __enter__(self) -> "Spinner":
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._stop_event.set()
        self._thread.join()
        sys.stdout.write("\r" + " " * (len(self.message) + 15) + "\r")
        sys.stdout.flush()
