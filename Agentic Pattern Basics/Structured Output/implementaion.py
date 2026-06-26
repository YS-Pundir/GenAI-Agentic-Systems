# pipeline_support_classifier.py — full structured output pipeline

import json  # Load schema file
import os  # GROQ_API_KEY from environment
from pathlib import Path  # File paths for schema and prompt files

from groq import Groq  # Groq chat API

from safe_parse import safe_parse_model_json  # Defensive parse






# validate_ticket.py — hand-written checks against schema (no extra library)

from typing import Tuple

ALLOWED_CATEGORIES = {"billing", "shipping", "product", "other"}
ALLOWED_PRIORITIES = {"low", "medium", "high"}


def validate_ticket(data: dict, schema: dict) -> Tuple[bool, str]:
    """Return (True, 'ok') or (False, reason) on first failure."""
    for key in schema.get("required", []):
        if key not in data:
            return False, f"Missing required field: {key}"
    if data["category"] not in ALLOWED_CATEGORIES:
        return False, f"Invalid category: {data['category']!r}"
    if data["priority"] not in ALLOWED_PRIORITIES:
        return False, f"Invalid priority: {data['priority']!r}"
    if not isinstance(data["summary"], str) or len(data["summary"].strip()) < 5:
        return False, "summary must be a non-empty string (min 5 chars)."
    if not isinstance(data["needs_human"], bool):
        return False, "needs_human must be boolean."
    return True, "ok"


def validate_or_raise(data: dict, schema: dict) -> dict:
    """Raise ValueError on failure — uniform error handling for callers."""
    ok, message = validate_ticket(data, schema)
    if not ok:
        raise ValueError(message)
    return data


def route_to_ui(ticket: dict) -> dict:
    """Map validated dict to UI props — frontend never parses raw model text."""
    return {
        "title": ticket["summary"],
        "badge": ticket["priority"].upper(),
        "team": ticket["category"],
        "show_draft": not ticket["needs_human"],
        "draft_text": ticket["suggested_reply"],
    }






SCHEMA_PATH = Path("schemas/support_ticket_v1.json")  # Output contract on disk
PROMPT_PATH = Path("prompts/support_agent/v1_system.txt")  # System prompt with JSON rules
MODEL_NAME = "llama-3.3-70b-versatile"  # Model name from your config file


def classify_message(customer_text: str) -> dict:
    """Call model, parse JSON, validate — return trusted dict or raise ValueError."""
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))  # Load schema once per call
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8").strip()  # System prompt text from disk
    client = Groq(api_key=os.environ["GROQ_API_KEY"])  # Key from env, never hard-coded

    response = client.chat.completions.create(
        model=MODEL_NAME,  # Fixed model for consistent output during testing
        messages=[
            {"role": "system", "content": system_prompt},  # JSON contract + behaviour rules
            {"role": "user", "content": customer_text},  # Raw customer message to classify
        ],
        temperature=0.0,  # Low randomness for stable classification
        max_tokens=512,  # Enough room for JSON object
        response_format={"type": "json_object"},  # Groq JSON syntax mode
    )

    raw = response.choices[0].message.content  # Untrusted string until parsed + validated
    parsed = safe_parse_model_json(raw)  # dict or ValueError
    return validate_or_raise(parsed, schema)  # Trusted dict or ValueError


if __name__ == "__main__":
    samples = [
        "Where is my order 4412? It was supposed to arrive yesterday.",
        "I was charged twice for order 8821. Please refund the duplicate.",
    ]
    for msg in samples:
        print(f"\n--- {msg[:40]}... ---")
        ticket = classify_message(msg)  # Full pipeline
        print("Validated:", json.dumps(ticket, indent=2))
        print("UI payload:", route_to_ui(ticket))
