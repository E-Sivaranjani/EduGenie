import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_FILE, override=True)


def parse_csv(value: str) -> list[str]:
    return [
        item.strip()
        for item in value.split(",")
        if item.strip()
    ]


class Settings:

    def __init__(self):

        self.gemini_api_key = os.getenv(
            "GEMINI_API_KEY",
            ""
        ).strip()

        self.gemini_model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.5-flash-lite"
        ).strip()

        self.local_explanation_enabled = (
            os.getenv(
                "LOCAL_EXPLANATION_ENABLED",
                "false"
            ).lower()
            in {"1", "true", "yes"}
        )

        self.local_explanation_model = os.getenv(
            "LOCAL_EXPLANATION_MODEL",
            "MBZUAI/LaMini-Flan-T5-783M"
        ).strip()

        self.cors_origins = (
            parse_csv(
                os.getenv("CORS_ORIGINS", "*")
            )
            or ["*"]
        )

    @property
    def gemini_configured(self):
        return bool(self.gemini_api_key)


settings = Settings()