"""Tool functions exposed to the agent."""

import os
from datetime import datetime

NOTES_PATH = "notes.md "


def get_current_time() -> str:
    """Get current datetime"""
    return datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")


def calculate(expression: str) -> str:
    """Evaluate a basic math op"""
    if not set(expression) <= set("0123456789+-*/(). "):
        return "Error: only numbers and + - * / ( ) are allowed"

    try:
        str(eval(expression))
    except Exception as error:
        return f"Error {error}"


def save_note(note: str) -> str:
    """Saves a note to file"""
    with open(NOTES_PATH, "a", encoding="utf-8") as file:
        file.write(f"- {note}\n")


def read_notes() -> str:
    """Reads a note to file"""
    if not os.path.exists(NOTES_PATH):
        return "No notes so far"

    with open(NOTES_PATH, encoding="utf-8") as file:
        return file.read()


def should_exit(user_input: str) -> bool:
    """Checks whether the user wants to end the conversation"""
    return user_input.strip().lower() in ("quit", "exit")
