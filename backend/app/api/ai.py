from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.db import get_db
from app.models import (
    ChatMessage, ChatResponse,
    LearningContentCreate, LearningContentResponse,
    QuizSubmission
)
from app.services import GeminiAIService, LearningService

router = APIRouter(prefix="/api/v1", tags=["AI & Learning"])


# ============ CONVERSATIONAL CHAT ============
@router.post("/chat", response_model=ChatResponse)
async def chat_with_gemini(
    message: ChatMessage,
    session: AsyncSession = Depends(get_db)
):
    """
    Chat with Gemini 2.5 Flash about space events, missions, and learning.
    
    Supports context types: events, weather, missions, learning
    """
    ai_service = GeminiAIService()
    
    response_text, tokens = await ai_service.conversational_chat(
        user_message=message.user_message,
        context_type=message.context_type,
        context_data=None  # TODO: Load from DB based on context_type
    )
    
    return ChatResponse(
        ai_response=response_text,
        tokens_used=tokens
    )


# ============ VISION INTELLIGENCE ============
@router.post("/vision/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    analysis_type: str = "general"
):
    """
    Analyze satellite/telescope images for auroras, storms, launches, anomalies.
    
    Supported types: aurora, storm, launch, anomaly, general
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    image_data = await file.read()
    
    ai_service = GeminiAIService()
    result = await ai_service.analyze_satellite_image(
        image_data=image_data,
        image_format=file.filename.split(".")[-1].lower(),
        analysis_type=analysis_type
    )
    
    return result


# ============ TEXT GENERATION & SUMMARIZATION ============
@router.post("/learning/content", response_model=LearningContentResponse)
async def create_learning_content(
    content: LearningContentCreate,
    session: AsyncSession = Depends(get_db)
):
    """Create new learning content (quiz, infographic, article)."""
    content_data = content.model_dump()
    return await LearningService.create_content(session, content_data)


@router.get("/learning/content", response_model=List[LearningContentResponse])
async def get_learning_content(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    session: AsyncSession = Depends(get_db)
):
    """Get published learning content, optionally filtered by category and difficulty."""
    return await LearningService.get_published_content(
        session, category, difficulty
    )


@router.get("/learning/content/{content_id}", response_model=LearningContentResponse)
async def get_content_detail(
    content_id: int,
    session: AsyncSession = Depends(get_db)
):
    """Get detailed learning content."""
    # TODO: Implement with proper error handling
    pass


@router.post("/learning/summarize")
async def summarize_content(
    content: dict,
    target_audience: str = "students"
):
    """
    Convert raw data into student-friendly explanations.
    
    Audiences: students, educators, general_public
    """
    ai_service = GeminiAIService()
    
    summary = await ai_service.summarize_learning_content(
        raw_content=str(content),
        target_audience=target_audience
    )
    
    return {"summary": summary}


# ============ QUIZ ============
@router.post("/learning/quiz/submit")
async def submit_quiz(
    submission: QuizSubmission,
    session: AsyncSession = Depends(get_db)
):
    """
    Submit quiz answers and get results.
    """
    # TODO: Implement quiz grading logic
    return {
        "score": 0,
        "max_score": 100,
        "passed": False,
        "message": "Quiz submitted"
    }
