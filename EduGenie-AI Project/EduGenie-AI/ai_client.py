from functools import lru_cache

from google import genai
from google.genai import types

from config import settings


# =====================================================
# CUSTOM ERROR
# =====================================================

class GeminiNotConfiguredError(
    RuntimeError
):
    pass


# =====================================================
# GET GEMINI CLIENT
# =====================================================

@lru_cache(maxsize=1)
def get_client():

    if not settings.gemini_api_key:

        raise GeminiNotConfiguredError(
            "GEMINI_API_KEY is missing. "
            "Please add your Gemini API key "
            "to the .env file."
        )

    try:

        client = genai.Client(
            api_key=settings.gemini_api_key
        )

        return client

    except Exception as error:

        raise RuntimeError(
            f"Unable to create Gemini client: {error}"
        ) from error


# =====================================================
# GENERATE TEXT
# =====================================================

async def generate_text(
    prompt: str,
    *,
    temperature: float = 0.3,
    response_schema=None
) -> str:

    client = get_client()


    # -------------------------------------------------
    # Basic configuration
    # -------------------------------------------------

    config_kwargs = {
        "temperature": temperature,
        "max_output_tokens": 4096
    }


    # -------------------------------------------------
    # Structured JSON response
    # -------------------------------------------------

    if response_schema is not None:

        config_kwargs.update({

            "response_mime_type":
                "application/json",

            "response_schema":
                response_schema

        })


    try:

        response = await client.aio.models.generate_content(

            model=settings.gemini_model,

            contents=prompt,

            config=types.GenerateContentConfig(
                **config_kwargs
            )

        )

    except Exception as error:

        print("\n====================================")
        print("GEMINI API ERROR")
        print("====================================")
        print(type(error).__name__)
        print(str(error))
        print("====================================\n")

        raise RuntimeError(
            f"Gemini API request failed: {error}"
        ) from error


    # -------------------------------------------------
    # Get response text
    # -------------------------------------------------

    text = getattr(
        response,
        "text",
        None
    )


    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )


    return text.strip()