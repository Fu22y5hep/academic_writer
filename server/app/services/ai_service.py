from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from openai import AsyncOpenAI, OpenAIError
import re
import asyncio
from fastapi import HTTPException

from app.core.config import settings

# Configure OpenAI
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

class AIResponse(BaseModel):
    """Base class for AI responses"""
    success: bool
    error: Optional[str] = None

class WritingSuggestion(AIResponse):
    original_text: str
    suggestion: str
    explanation: str
    confidence: float = 0.0

class GrammarCheck(AIResponse):
    text: str
    corrections: List[Dict[str, Any]]
    improved_text: str

class CitationSuggestion(AIResponse):
    context: str
    suggestions: List[Dict[str, Any]]

async def call_openai_with_retry(messages: List[Dict[str, str]], max_retries: int = 3) -> Dict[str, Any]:
    """Make OpenAI API call with retry logic"""
    for attempt in range(max_retries):
        try:
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                temperature=settings.OPENAI_TEMPERATURE,
                max_tokens=settings.OPENAI_MAX_TOKENS,
                timeout=settings.OPENAI_TIMEOUT
            )
            return response
        except OpenAIError as e:
            if attempt == max_retries - 1:
                raise HTTPException(
                    status_code=503,
                    detail=f"AI service unavailable: {str(e)}"
                )
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

async def get_writing_suggestions(
    text: str,
    context: Optional[str] = None,
    style: str = "academic"
) -> WritingSuggestion:
    """Get AI-powered writing suggestions for improving the text."""
    try:
        prompt = f"""As an academic writing assistant, analyze and improve the following text.
        Style: {style}
        
        Original text:
        {text}
        
        {f'Context: {context}' if context else ''}
        
        Provide specific suggestions to enhance clarity, academic tone, and impact.
        Format your response as JSON with the following structure:
        {{
            "suggestion": "improved text",
            "explanation": "detailed explanation of changes",
            "confidence": float between 0 and 1
        }}"""

        response = await call_openai_with_retry([
            {"role": "system", "content": "You are an expert academic writing assistant."},
            {"role": "user", "content": prompt}
        ])

        # Parse response
        content = response.choices[0].message.content
        # Extract JSON from response
        import json
        result = json.loads(content)

        return WritingSuggestion(
            success=True,
            original_text=text,
            **result
        )

    except Exception as e:
        return WritingSuggestion(
            success=False,
            error=str(e),
            original_text=text,
            suggestion="",
            explanation="",
            confidence=0.0
        )

async def check_grammar_and_style(text: str) -> GrammarCheck:
    """Check grammar, style, and academic tone."""
    try:
        prompt = f"""Analyze the following text for grammar, style, and academic tone.
        Provide corrections and improvements in JSON format:
        
        Text: {text}
        
        Format your response as:
        {{
            "corrections": [
                {{"type": "grammar/style/tone", "location": "...", "issue": "...", "suggestion": "..."}}
            ],
            "improved_text": "complete corrected text"
        }}"""

        response = await call_openai_with_retry([
            {"role": "system", "content": "You are an expert academic editor."},
            {"role": "user", "content": prompt}
        ])

        # Parse response
        content = response.choices[0].message.content
        # Extract JSON from response
        import json
        result = json.loads(content)

        return GrammarCheck(
            success=True,
            text=text,
            **result
        )

    except Exception as e:
        return GrammarCheck(
            success=False,
            error=str(e),
            text=text,
            corrections=[],
            improved_text=text
        )

async def suggest_citations(context: str) -> CitationSuggestion:
    """Suggest relevant academic citations based on the context."""
    try:
        prompt = f"""Based on the following context, suggest relevant academic citations.
        
        Context:
        {context}
        
        Format your response as JSON:
        {{
            "suggestions": [
                {{
                    "title": "paper title",
                    "authors": ["author1", "author2"],
                    "year": year,
                    "relevance": "explanation of relevance",
                    "confidence": float between 0 and 1
                }}
            ]
        }}"""

        response = await call_openai_with_retry([
            {"role": "system", "content": "You are an expert academic researcher."},
            {"role": "user", "content": prompt}
        ])

        # Parse response
        content = response.choices[0].message.content
        # Extract JSON from response
        import json
        result = json.loads(content)

        return CitationSuggestion(
            success=True,
            context=context,
            **result
        )

    except Exception as e:
        return CitationSuggestion(
            success=False,
            error=str(e),
            context=context,
            suggestions=[]
        )

async def enhance_academic_tone(text: str) -> str:
    """Enhance the academic tone of the text while preserving meaning."""
    try:
        prompt = f"""Enhance the academic tone of this text while preserving its meaning.
        
        Text:
        {text}
        
        Format your response as JSON:
        {{
            "enhanced_text": "improved text with academic tone",
            "explanation": "explanation of changes made"
        }}"""

        response = await call_openai_with_retry([
            {"role": "system", "content": "You are an expert academic writing assistant."},
            {"role": "user", "content": prompt}
        ])

        content = response.choices[0].message.content
        result = json.loads(content)
        return result["enhanced_text"]

    except Exception as e:
        return text

async def generate_research_questions(topic: str, context: str) -> List[str]:
    """Generate research questions based on topic and context."""
    try:
        prompt = f"""Generate research questions for the following topic and context.
        
        Topic: {topic}
        Context: {context}
        
        Format your response as JSON:
        {{
            "questions": [
                {{"question": "research question", "rationale": "explanation of importance", "methodology": "suggested research method"}}
            ]
        }}"""

        response = await call_openai_with_retry([
            {"role": "system", "content": "You are an expert academic researcher."},
            {"role": "user", "content": prompt}
        ])

        content = response.choices[0].message.content
        result = json.loads(content)
        return [q["question"] for q in result["questions"]]

    except Exception as e:
        return []

async def create_outline(
    topic: str,
    research_type: str = "qualitative",
    outline_type: str = "detailed"
) -> Dict[str, Any]:
    """Create a research outline based on topic and type."""
    try:
        prompt = f"""Create a {outline_type} academic research outline for the following topic.
        
        Topic: {topic}
        Research Type: {research_type}
        
        Format your response as JSON:
        {{
            "outline": [
                {{"section": "section name", "subsections": ["subsection 1", "subsection 2"], "key_points": ["point 1", "point 2"], "suggested_content": "brief content description"}}
            ],
            "recommendations": ["recommendation 1", "recommendation 2"]
        }}"""

        response = await call_openai_with_retry([
            {"role": "system", "content": "You are an expert academic writing consultant."},
            {"role": "user", "content": prompt}
        ])

        content = response.choices[0].message.content
        result = json.loads(content)
        return {
            "outline": result["outline"],
            "outline_type": outline_type,
            "recommendations": result.get("recommendations", [])
        }

    except Exception as e:
        return {
            "outline": [],
            "outline_type": outline_type,
            "recommendations": [],
            "error": str(e)
        }

async def analyze_literature(text: str) -> Dict[str, Any]:
    """Analyze literature review or research text."""
    try:
        prompt = f"""Analyze this academic text and provide insights.
        
        Text:
        {text}
        
        Format your response as JSON:
        {{
            "key_themes": ["theme 1", "theme 2"],
            "methodology_analysis": "analysis of methods used",
            "theoretical_framework": "identified frameworks",
            "gaps": ["research gap 1", "research gap 2"],
            "recommendations": ["recommendation 1", "recommendation 2"]
        }}"""

        response = await call_openai_with_retry([
            {"role": "system", "content": "You are an expert academic researcher."},
            {"role": "user", "content": prompt}
        ])

        content = response.choices[0].message.content
        result = json.loads(content)
        return {
            "analysis": result,
            "text_length": len(text)
        }

    except Exception as e:
        return {
            "analysis": {},
            "text_length": len(text),
            "error": str(e)
        }

async def suggest_methodology(
    research_question: str,
    research_type: str = "mixed"
) -> Dict[str, Any]:
    """Suggest research methodology based on research question."""
    try:
        prompt = f"""Suggest appropriate research methodology for this research question.
        
        Research Question: {research_question}
        Research Type: {research_type}
        
        Format your response as JSON:
        {{
            "suggested_methods": [
                {{"method": "method name", "rationale": "why this method is appropriate", "implementation": "how to implement", "limitations": ["limitation 1", "limitation 2"]}}
            ],
            "data_collection": ["technique 1", "technique 2"],
            "analysis_approaches": ["approach 1", "approach 2"],
            "validity_considerations": ["consideration 1", "consideration 2"]
        }}"""

        response = await call_openai_with_retry([
            {"role": "system", "content": "You are an expert research methodologist."},
            {"role": "user", "content": prompt}
        ])

        content = response.choices[0].message.content
        result = json.loads(content)
        return {
            "methodology_suggestions": result,
            "research_type": research_type
        }

    except Exception as e:
        return {
            "methodology_suggestions": {},
            "research_type": research_type,
            "error": str(e)
        }

async def generate_abstract(
    title: str,
    content: Dict[str, str],
    max_words: int = 250
) -> str:
    """Generate an academic abstract based on paper content."""
    try:
        prompt = f"""Generate an academic abstract for this paper.
        
        Title: {title}
        Content:
        {json.dumps(content, indent=2)}
        Max Words: {max_words}
        
        Format your response as JSON:
        {{
            "abstract": "generated abstract text",
            "word_count": number,
            "keywords": ["keyword1", "keyword2"]
        }}"""

        response = await call_openai_with_retry([
            {"role": "system", "content": "You are an expert academic editor."},
            {"role": "user", "content": prompt}
        ])

        content = response.choices[0].message.content
        result = json.loads(content)
        return result["abstract"]

    except Exception as e:
        return f"Error generating abstract: {str(e)}"

async def suggest_keywords(
    title: str,
    abstract: str,
    content: Optional[str] = None,
    num_keywords: int = 5
) -> List[str]:
    """Generate academic keywords for the paper."""
    try:
        prompt = f"""Generate academic keywords for this paper.
        
        Title: {title}
        Abstract: {abstract}
        Content: {content if content else 'Not provided'}
        Number of Keywords: {num_keywords}
        
        Format your response as JSON:
        {{
            "keywords": [
                {{
                    "term": "keyword",
                    "relevance": float between 0 and 1,
                    "category": "methodology/concept/theory"
                }}
            ]
        }}"""

        response = await call_openai_with_retry([
            {"role": "system", "content": "You are an expert in academic publishing."},
            {"role": "user", "content": prompt}
        ])

        content = response.choices[0].message.content
        result = json.loads(content)
        return [k["term"] for k in sorted(result["keywords"], key=lambda x: x["relevance"], reverse=True)]

    except Exception as e:
        return []

async def format_citation(
    citation_text: str,
    style: str = "apa"
) -> str:
    """Format a citation according to the specified style guide."""
    try:
        prompt = f"""Format this citation according to {style.upper()} style.
        
        Citation: {citation_text}
        
        Format your response as JSON:
        {{
            "formatted_citation": "properly formatted citation",
            "notes": ["formatting note 1", "formatting note 2"]
        }}"""

        response = await call_openai_with_retry([
            {"role": "system", "content": "You are an expert in academic citation styles."},
            {"role": "user", "content": prompt}
        ])

        content = response.choices[0].message.content
        result = json.loads(content)
        return result["formatted_citation"]

    except Exception as e:
        return citation_text

async def check_style_guide(
    text: str,
    style_guide: str = "apa"
) -> Dict[str, Any]:
    """Check text against academic style guide requirements."""
    try:
        prompt = f"""Check this text against {style_guide.upper()} style guide requirements.
        
        Text: {text}
        
        Format your response as JSON:
        {{
            "issues": [
                {{
                    "type": "formatting/citation/structure",
                    "location": "description of location",
                    "issue": "description of issue",
                    "correction": "suggested correction"
                }}
            ],
            "general_feedback": "overall assessment",
            "compliance_score": float between 0 and 1
        }}"""

        response = await call_openai_with_retry([
            {"role": "system", "content": "You are an expert in academic style guides."},
            {"role": "user", "content": prompt}
        ])

        content = response.choices[0].message.content
        result = json.loads(content)
        return {
            "analysis": result,
            "style_guide": style_guide
        }

    except Exception as e:
        return {
            "analysis": {},
            "style_guide": style_guide,
            "error": str(e)
        }

async def analyze_citations(text: str) -> List[Dict[str, Any]]:
    """Analyze citations in academic text."""
    try:
        prompt = f"""Analyze the citations in this academic text.
        
        Text: {text}
        
        Format your response as JSON:
        {{
            "citations": [
                {{
                    "text": "cited text",
                    "source": "source details",
                    "type": "citation type",
                    "context": "usage context",
                    "suggestions": ["improvement 1", "improvement 2"]
                }}
            ],
            "overall_assessment": "assessment of citation usage",
            "recommendations": ["recommendation 1", "recommendation 2"]
        }}"""

        response = await call_openai_with_retry([
            {"role": "system", "content": "You are an expert in academic citations."},
            {"role": "user", "content": prompt}
        ])

        content = response.choices[0].message.content
        result = json.loads(content)
        return result["citations"]

    except Exception as e:
        return []

async def suggest_transitions(paragraphs: List[str]) -> List[Dict[str, Any]]:
    """Suggest transitions between paragraphs."""
    try:
        suggestions = []
        for i in range(len(paragraphs) - 1):
            prompt = f"""Suggest transitions between these academic paragraphs.
            
            Paragraph 1:
            {paragraphs[i]}
            
            Paragraph 2:
            {paragraphs[i + 1]}
            
            Format your response as JSON:
            {{
                "transition": "suggested transition text",
                "rationale": "explanation of connection",
                "alternatives": ["alternative 1", "alternative 2"]
            }}"""

            response = await call_openai_with_retry([
                {"role": "system", "content": "You are an expert academic writer."},
                {"role": "user", "content": prompt}
            ])

            content = response.choices[0].message.content
            result = json.loads(content)
            suggestions.append({
                "before": paragraphs[i],
                "after": paragraphs[i + 1],
                **result
            })

        return suggestions

    except Exception as e:
        return []

async def check_argument_structure(text: str) -> Dict[str, Any]:
    """Analyze and provide feedback on argument structure."""
    try:
        prompt = """Analyze the argument structure in this text. Provide:
        1. Main claims identification
        2. Evidence assessment
        3. Logical flow analysis
        4. Counter-argument consideration
        5. Suggestions for strengthening arguments
        
        Text:
        {text}
        
        Format your response as JSON:
        {{
            "analysis": "structured analysis",
            "suggestions": ["suggestion 1", "suggestion 2"],
            "strengths": ["strength 1", "strength 2"],
            "weaknesses": ["weakness 1", "weakness 2"]
        }}"""

        response = await call_openai_with_retry([
            {"role": "system", "content": "You are an expert in academic argumentation."},
            {"role": "user", "content": prompt.format(text=text)}
        ])

        content = response.choices[0].message.content
        result = json.loads(content)
        return {
            "analysis": result,
            "text_length": len(text)
        }

    except Exception as e:
        return {
            "analysis": {},
            "text_length": len(text),
            "error": str(e)
        }

async def suggest_evidence(claim: str, field: str) -> List[Dict[str, str]]:
    """Suggest types of evidence to support an academic claim."""
    try:
        prompt = f"""For the following academic claim in the field of {field},
        suggest appropriate types of evidence to support it:
        
        Claim: {claim}
        
        Please suggest:
        1. Empirical evidence types
        2. Theoretical support
        3. Methodological approaches
        4. Potential data sources
        5. Specific examples or cases
        
        Format your response as JSON:
        {{
            "evidence_types": [
                {{
                    "type": "evidence type",
                    "rationale": "explanation of relevance",
                    "examples": ["example 1", "example 2"]
                }}
            ]
        }}"""

        response = await call_openai_with_retry([
            {"role": "system", "content": "You are an expert academic researcher."},
            {"role": "user", "content": prompt}
        ])

        content = response.choices[0].message.content
        result = json.loads(content)
        return result["evidence_types"]

    except Exception as e:
        return []

async def extract_citations(text: str) -> List[Dict[str, str]]:
    """Extract and parse citations from text."""
    try:
        prompt = """Extract and analyze all citations from the following text.
        For each citation, identify:
        1. Citation type (in-text, parenthetical)
        2. Authors
        3. Year
        4. Page numbers (if present)
        5. Context of usage
        
        Text:
        {text}
        
        Format your response as JSON:
        {{
            "citations": [
                {{
                    "text": "cited text",
                    "type": "citation type",
                    "authors": ["author1", "author2"],
                    "year": year,
                    "pages": "page numbers",
                    "context": "usage context"
                }}
            ]
        }}"""

        response = await call_openai_with_retry([
            {"role": "system", "content": "You are an expert in academic citations."},
            {"role": "user", "content": prompt.format(text=text)}
        ])

        content = response.choices[0].message.content
        result = json.loads(content)
        return result["citations"]

    except Exception as e:
        return []
