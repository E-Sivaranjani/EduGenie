from ai_client import generate_text


async def answer_question(
    question: str,
    level: str
) -> str:

    prompt = f"""
You are EduGenie, a friendly educational assistant.

Student level:
{level}

Question:
{question}

Answer the question accurately and concisely.

Requirements:

1. Give the direct answer first.
2. Explain it using simple language.
3. Use examples when useful.
4. Match the student's learning level.
5. Avoid unnecessary technical jargon.
6. Do not invent citations.
7. If something is uncertain, clearly say so.
"""

    return await generate_text(
        prompt,
        temperature=0.25
    )