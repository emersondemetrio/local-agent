"""Structured output schema for the agent's replies.

The `reply` field's `pattern` is enforced by Ollama's grammar-constrained
decoder when the agent is run with `output_type=NativeOutput(PlainTextReply)`
(see main.py). That means Markdown syntax characters can't appear in the
output at all, at generation time, rather than being stripped afterward.
"""

from pydantic import BaseModel, Field

PLAIN_TEXT_PATTERN = r"^[^*#`]*$"


class PlainTextReply(BaseModel):
    """The agent's reply to the user, guaranteed to contain no Markdown
    formatting characters."""

    reply: str = Field(
        pattern=PLAIN_TEXT_PATTERN,
        description="Plain-text answer to show the user. No Markdown formatting.",
    )
