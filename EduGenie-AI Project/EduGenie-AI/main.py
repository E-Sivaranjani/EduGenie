from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from config import settings

from schemas import (
    QARequest,
    ExplainRequest,
    QuizRequest,
    SummaryRequest,
    LearningPathRequest,
    TextResponse,
    QuizResponse,
    LearningPathResponse
)

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


# =====================================================
# PROJECT PATH
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title="EduGenie API",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# =====================================================
# STATIC FILES
# =====================================================

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)


# =====================================================
# TEMPLATES
# =====================================================

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


# =====================================================
# HOME PAGE
# =====================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "gemini_configured": settings.gemini_configured,
        "model": settings.gemini_model
    }


# =====================================================
# Q&A
# =====================================================

@app.post(
    "/qa",
    response_model=TextResponse
)
async def qa(payload: QARequest):

    answer = await answer_question(
        payload.question,
        payload.level
    )

    return TextResponse(
        result=answer
    )


# =====================================================
# EXPLAIN
# =====================================================

@app.post(
    "/explain",
    response_model=TextResponse
)
async def explain(payload: ExplainRequest):

    answer = await explain_concept(
        payload.topic,
        payload.level,
        payload.context
    )

    return TextResponse(
        result=answer
    )


# =====================================================
# QUIZ
# =====================================================

@app.post(
    "/quiz",
    response_model=QuizResponse
)
async def quiz(payload: QuizRequest):

    return await generate_quiz(
        payload.text,
        payload.level,
        payload.question_count
    )


# =====================================================
# SUMMARY
# =====================================================

@app.post(
    "/summarize",
    response_model=TextResponse
)
async def summarize(payload: SummaryRequest):

    answer = await summarize_text(
        payload.text,
        payload.level,
        payload.max_words
    )

    return TextResponse(
        result=answer
    )


# =====================================================
# LEARNING PATH
# =====================================================

@app.post(
    "/learn/recommendations",
    response_model=LearningPathResponse
)
async def learning_path(
    payload: LearningPathRequest
):

    return await get_learning_recommendations(
        payload.topic,
        payload.level,
        payload.weeks
    )
@app.get("/test-gemini")
async def test_gemini():

    from ai_client import generate_text

    try:

        result = await generate_text(
            "Answer in one short sentence: "
            "What is artificial intelligence?"
        )

        return {
            "status": "success",
            "message": result
        }

    except Exception as error:

        return {
            "status": "error",
            "message": str(error)
        }