from ai_client import generate_text
from schemas import QuizResponse


def clean_json_block(
    text: str
) -> str:

    text = text.strip()

    if text.startswith("```"):

        lines = text.splitlines()

        if (
            lines
            and lines[0].startswith("```")
        ):
            lines = lines[1:]

        if (
            lines
            and lines[-1].strip() == "```"
        ):
            lines = lines[:-1]

        text = "\n".join(
            lines
        ).strip()

    return text


async def generate_quiz(
    text: str,
    level: str,
    question_count: int
) -> QuizResponse:

    prompt = f"""
You are EduGenie, an educational quiz generator.

Create exactly {question_count}
multiple-choice questions from the
following educational passage.

Student level:
{level}

Rules:

1. Every question must be answerable
   from the passage.
2. Each question must have exactly
   four options.
3. There must be one correct answer.
4. The correct_answer must exactly match
   one of the four options.
5. Include a short explanation.
6. Avoid trick questions.
7. Make distractors plausible.
8. Return only structured JSON.

PASSAGE:

{text}
"""

    raw = await generate_text(
        prompt,
        temperature=0.35,
        response_schema=QuizResponse
    )

    return QuizResponse.model_validate_json(
        clean_json_block(raw)
    )