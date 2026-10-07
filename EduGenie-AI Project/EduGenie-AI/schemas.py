from pydantic import BaseModel, ConfigDict, Field


class QARequest(BaseModel):

    model_config = ConfigDict(
        str_strip_whitespace=True
    )

    question: str = Field(
        ...,
        min_length=2,
        max_length=5000
    )

    level: str = Field(
        default="beginner",
        max_length=50
    )


class ExplainRequest(BaseModel):

    model_config = ConfigDict(
        str_strip_whitespace=True
    )

    topic: str = Field(
        ...,
        min_length=2,
        max_length=300
    )

    level: str = Field(
        default="beginner",
        max_length=50
    )

    context: str = Field(
        default="",
        max_length=3000
    )


class QuizRequest(BaseModel):

    model_config = ConfigDict(
        str_strip_whitespace=True
    )

    text: str = Field(
        ...,
        min_length=20,
        max_length=15000
    )

    level: str = Field(
        default="beginner",
        max_length=50
    )

    question_count: int = Field(
        default=3,
        ge=1,
        le=10
    )


class SummaryRequest(BaseModel):

    model_config = ConfigDict(
        str_strip_whitespace=True
    )

    text: str = Field(
        ...,
        min_length=30,
        max_length=20000
    )

    level: str = Field(
        default="beginner",
        max_length=50
    )

    max_words: int = Field(
        default=120,
        ge=30,
        le=500
    )


class LearningPathRequest(BaseModel):

    model_config = ConfigDict(
        str_strip_whitespace=True
    )

    topic: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    level: str = Field(
        default="beginner",
        max_length=50
    )

    weeks: int = Field(
        default=6,
        ge=1,
        le=24
    )


class TextResponse(BaseModel):

    result: str


class QuizQuestion(BaseModel):

    question: str

    options: list[str] = Field(
        min_length=4,
        max_length=4
    )

    correct_answer: str

    explanation: str


class QuizResponse(BaseModel):

    questions: list[QuizQuestion]


class LearningPathItem(BaseModel):

    stage: str

    topics: list[str]

    duration: str

    resources: list[str]

    practice: str


class LearningPathResponse(BaseModel):

    topic: str

    level: str

    weeks: int

    roadmap: list[LearningPathItem]

    study_tips: list[str]