from ai_client import generate_text
from schemas import LearningPathResponse


async def get_learning_recommendations(
    topic: str,
    level: str,
    weeks: int
) -> LearningPathResponse:

    prompt = f"""
You are EduGenie, a personalized learning
path advisor.

Create a {weeks}-week learning roadmap
for:

Topic:
{topic}

Learner level:
{level}

Build the roadmap progressively from
beginner knowledge toward practical
advanced understanding.

For every stage provide:

- stage name
- topics
- realistic duration
- useful resource types or reputable
  resource names
- practical exercise

Also provide 4 to 6 study tips.

Do not invent URLs.

If you mention resources, use names such as:

- official documentation
- textbooks
- reputable learning platforms
- well-known educational channels

Return structured JSON.
"""

    raw = await generate_text(
        prompt,
        temperature=0.35,
        response_schema=LearningPathResponse
    )

    result = LearningPathResponse.model_validate_json(
        raw
    )

    result.topic = topic
    result.level = level
    result.weeks = weeks

    return result