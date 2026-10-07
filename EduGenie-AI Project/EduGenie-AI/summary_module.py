from ai_client import generate_text


async def summarize_text(
    text: str,
    level: str,
    max_words: int
) -> str:

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Student level:
{level}

Maximum target length:
approximately {max_words} words.

Summarize the following educational passage.

Requirements:

- Keep the important facts.
- Remove repetition.
- Use simple language.
- Preserve the original meaning.
- Do not add information that is not present.
- Make it useful for quick revision.
- Use bullet points when helpful.

PASSAGE:

{text}
"""

    return await generate_text(
        prompt,
        temperature=0.2
    )