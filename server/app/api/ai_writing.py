from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user, check_rate_limit, get_rate_limit_info
from app.models.user import User
from app.services import ai_service
from pydantic import BaseModel

router = APIRouter()

class TextRequest(BaseModel):
    text: str
    context: str = None
    style: str = "academic"

class TopicRequest(BaseModel):
    topic: str
    context: str

class OutlineRequest(BaseModel):
    topic: str
    context: str
    outline_type: str = "research_paper"

class LiteratureRequest(BaseModel):
    text: str

class MethodologyRequest(BaseModel):
    research_type: str
    research_questions: List[str]
    context: str

class AbstractRequest(BaseModel):
    title: str
    content: Dict[str, str]
    max_words: int = 250

class KeywordRequest(BaseModel):
    title: str
    abstract: str
    num_keywords: int = 5

class ReferenceRequest(BaseModel):
    reference_text: str
    style: str = "apa"
    version: str = "7"

class StyleGuideRequest(BaseModel):
    text: str
    style_guide: str = "apa"
    elements: List[str] = ["citations", "headings", "numbers", "abbreviations"]

class TransitionRequest(BaseModel):
    paragraphs: List[str]

class ArgumentRequest(BaseModel):
    text: str

class EvidenceRequest(BaseModel):
    claim: str
    field: str

@router.get("/rate-limit-info")
async def get_current_rate_limit(
    request: Request,
    rate_limit_info: dict = Depends(get_rate_limit_info)
) -> dict:
    """
    Get current rate limit information for the user.
    """
    return rate_limit_info

@router.post("/suggestions")
async def get_writing_suggestions(
    request: Request,
    text_request: TextRequest,
    _: None = Depends(check_rate_limit),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get AI-powered writing suggestions.
    """
    try:
        return await ai_service.get_writing_suggestions(
            text_request.text,
            text_request.context,
            text_request.style
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating suggestions: {str(e)}"
        )

@router.post("/grammar")
async def check_grammar(
    request: Request,
    text_request: TextRequest,
    _: None = Depends(check_rate_limit),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Check grammar and style.
    """
    try:
        return await ai_service.check_grammar_and_style(text_request.text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error checking grammar: {str(e)}"
        )

@router.post("/citations")
async def get_citation_suggestions(
    request: Request,
    text_request: TextRequest,
    _: None = Depends(check_rate_limit),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get citation suggestions.
    """
    try:
        return await ai_service.suggest_citations(text_request.text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error suggesting citations: {str(e)}"
        )

@router.post("/enhance")
async def enhance_tone(
    request: Request,
    text_request: TextRequest,
    _: None = Depends(check_rate_limit),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Enhance academic tone.
    """
    try:
        enhanced_text = await ai_service.enhance_academic_tone(text_request.text)
        return {"enhanced_text": enhanced_text}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error enhancing tone: {str(e)}"
        )

@router.post("/research-questions")
async def generate_questions(
    request: Request,
    topic_request: TopicRequest,
    _: None = Depends(check_rate_limit),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Generate research questions.
    """
    try:
        questions = await ai_service.generate_research_questions(
            topic_request.topic,
            topic_request.context
        )
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating questions: {str(e)}"
        )

@router.post("/outline")
async def generate_outline(
    request: Request,
    outline_request: OutlineRequest,
    _: None = Depends(check_rate_limit),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Generate a structured outline.
    """
    try:
        return await ai_service.generate_outline(
            outline_request.topic,
            outline_request.context,
            outline_request.outline_type
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating outline: {str(e)}"
        )

@router.post("/literature-analysis")
async def analyze_literature(
    request: Request,
    literature_request: LiteratureRequest,
    _: None = Depends(check_rate_limit),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Analyze literature review content.
    """
    try:
        return await ai_service.analyze_literature(literature_request.text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing literature: {str(e)}"
        )

@router.post("/methodology")
async def suggest_methodology(
    request: Request,
    methodology_request: MethodologyRequest,
    _: None = Depends(check_rate_limit),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get methodology suggestions.
    """
    try:
        return await ai_service.suggest_methodology(
            methodology_request.research_type,
            methodology_request.research_questions,
            methodology_request.context
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error suggesting methodology: {str(e)}"
        )

@router.post("/abstract")
async def generate_abstract(
    request: Request,
    abstract_request: AbstractRequest,
    _: None = Depends(check_rate_limit),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Generate an academic abstract.
    """
    try:
        abstract = await ai_service.generate_abstract(
            abstract_request.title,
            abstract_request.content,
            abstract_request.max_words
        )
        return {"abstract": abstract}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating abstract: {str(e)}"
        )

@router.post("/keywords")
async def suggest_keywords(
    request: Request,
    keyword_request: KeywordRequest,
    _: None = Depends(check_rate_limit),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Generate academic keywords.
    """
    try:
        keywords = await ai_service.suggest_keywords(
            keyword_request.title,
            keyword_request.abstract,
            keyword_request.num_keywords
        )
        return {"keywords": keywords}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error suggesting keywords: {str(e)}"
        )

@router.post("/format-reference")
async def format_reference(
    request: Request,
    ref_request: ReferenceRequest,
    _: None = Depends(check_rate_limit),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Format a reference according to a specific style guide.
    """
    try:
        formatted = await ai_service.format_reference(
            ref_request.reference_text,
            ref_request.style,
            ref_request.version
        )
        return {"formatted_reference": formatted}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error formatting reference: {str(e)}"
        )

@router.post("/check-style")
async def check_style(
    request: Request,
    style_request: StyleGuideRequest,
    _: None = Depends(check_rate_limit),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Check text against style guide requirements.
    """
    try:
        return await ai_service.check_style_guide(
            style_request.text,
            style_request.style_guide,
            style_request.elements
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error checking style: {str(e)}"
        )

@router.post("/extract-citations")
async def extract_citations(
    request: Request,
    text_request: TextRequest,
    _: None = Depends(check_rate_limit),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Extract and analyze citations from text.
    """
    try:
        return await ai_service.extract_citations(text_request.text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting citations: {str(e)}"
        )

@router.post("/suggest-transitions")
async def suggest_transitions(
    request: Request,
    transition_request: TransitionRequest,
    _: None = Depends(check_rate_limit),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Suggest transition sentences between paragraphs.
    """
    try:
        return await ai_service.suggest_transitions(transition_request.paragraphs)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error suggesting transitions: {str(e)}"
        )

@router.post("/check-arguments")
async def check_arguments(
    request: Request,
    arg_request: ArgumentRequest,
    _: None = Depends(check_rate_limit),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Analyze argument structure.
    """
    try:
        return await ai_service.check_argument_structure(arg_request.text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error checking arguments: {str(e)}"
        )

@router.post("/suggest-evidence")
async def suggest_evidence(
    request: Request,
    evidence_request: EvidenceRequest,
    _: None = Depends(check_rate_limit),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Suggest evidence types for an academic claim.
    """
    try:
        return await ai_service.suggest_evidence(
            evidence_request.claim,
            evidence_request.field
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error suggesting evidence: {str(e)}"
        )
