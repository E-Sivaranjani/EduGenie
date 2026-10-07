from ai_client import generate_text
from config import settings


_local_pipeline = None


def get_local_pipeline():

    global _local_pipeline

    if _local_pipeline is None:

        from transformers import pipeline

        _local_pipeline = pipeline(
            "text2text-generation",
            model=settings.local_explanation_model
        )

    return _local_pipeline


def local_explain(
    topic: str,
    level: str,
    context: str
):

    if not settings.local_explanation_enabled:
        return None

    try:

        generator = get_local_pipeline()

        prompt = (
            f"Explain {topic} to a "
            f"{level} student using simple "
            f"language. "
            f"Context: "
            f"{context or 'No additional context.'}"
        )

        result = generator(
            prompt,
            max_new_tokens=180,
            do_sample=False
        )

        if result:

            return result[0][
                "generated_text"
            ].strip()

    except Exception:

        return None

    return None


async def explain_concept(
    topic: str,
    level: str,
    context: str = ""
) -> str:

    if settings.local_explanation_enabled:

        local_result = local_explain(
            topic,
            level,
            context
        )

        if local_result:

            return local_result

    prompt = f"""
You are an expert teacher working
for EduGenie.

Explain:

{topic}

Student level:

{level}

Additional context:

{context or "None"}

Use this structure:

1. Simple definition
2. Easy explanation
3. Real-world example
4. Three important points to remember

Requirements:

- Use simple language.
- Avoid unnecessary jargon.
- Make the explanation beginner friendly.
- Keep it concise but complete.
"""

    return await generate_text(
        prompt,
        temperature=0.25
    )