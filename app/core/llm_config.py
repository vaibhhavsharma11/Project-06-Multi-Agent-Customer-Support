import os


def is_demo_mode() -> bool:
    """Return whether the application should use deterministic demo mode."""

    return os.getenv(
        "DEMO_MODE",
        "true",
    ).lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def get_openai_api_key() -> str:
    """Return the configured OpenAI API key."""

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured."
        )

    return api_key


def get_openai_model() -> str:
    """Return the configured OpenAI model."""

    return os.getenv(
        "OPENAI_MODEL",
        "gpt-4o-mini",
    )