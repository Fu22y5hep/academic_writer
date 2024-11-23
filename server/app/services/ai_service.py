from typing import List, Dict, Any, Optional
import openai
from pydantic import BaseModel
import re

from app.core.config import settings

# Configure OpenAI
openai.api_key = settings.OPENAI_API_KEY

class WritingSuggestion(BaseModel):
    original_text: str
    suggestion: str
    explanation: str
    confidence: float

class GrammarCheck(BaseModel):
    text: str
    corrections: List[Dict[str, Any]]
    improved_text: str

class CitationSuggestion(BaseModel):
    context: str
    suggestions: List[Dict[str, Any]]

async def get_writing_suggestions(
    text: str,
    context: Optional[str] = None,
    style: str = "academic"
) -> WritingSuggestion:
    """
    Get AI-powered writing suggestions for improving the text.
    """
    prompt = f"""As an academic writing assistant, analyze and improve the following text.
    Style: {style}
    
    Original text:
    {text}
    
    {f'Context: {context}' if context else ''}
    
    Provide specific suggestions to enhance clarity, academic tone, and impact."""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert academic writing assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    
    suggestion = response.choices[0].message.content
    
    return WritingSuggestion(
        original_text=text,
        suggestion=suggestion,
        explanation="AI-generated writing improvement suggestions",
        confidence=response.choices[0].finish_reason == "stop"
    )

async def check_grammar_and_style(text: str) -> GrammarCheck:
    """
    Check grammar, style, and academic tone.
    """
    prompt = """Review the following academic text for grammar, style, and tone.
    Identify any issues and suggest improvements.
    
    Text to review:
    {text}
    
    Provide corrections and improvements in a clear, structured format."""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert academic editor."},
            {"role": "user", "content": prompt.format(text=text)}
        ],
        temperature=0.3,
    )
    
    # Parse the response into structured corrections
    analysis = response.choices[0].message.content
    corrections = [
        {
            "type": "grammar",
            "suggestion": analysis,
            "confidence": response.choices[0].finish_reason == "stop"
        }
    ]
    
    return GrammarCheck(
        text=text,
        corrections=corrections,
        improved_text=analysis
    )

async def suggest_citations(context: str) -> CitationSuggestion:
    """
    Suggest relevant academic citations based on the context.
    """
    prompt = """Based on the following academic text, suggest relevant papers or sources
    that could be cited to strengthen the arguments or provide additional context.
    
    Text:
    {context}
    
    Provide suggestions in a structured format with titles, authors, and brief explanations
    of relevance."""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert academic researcher."},
            {"role": "user", "content": prompt.format(context=context)}
        ],
        temperature=0.7,
    )
    
    # Parse the response into structured suggestions
    suggestions = [
        {
            "suggestion": response.choices[0].message.content,
            "confidence": response.choices[0].finish_reason == "stop"
        }
    ]
    
    return CitationSuggestion(
        context=context,
        suggestions=suggestions
    )

async def enhance_academic_tone(text: str) -> str:
    """
    Enhance the academic tone of the text while preserving meaning.
    """
    prompt = """Enhance the academic tone of the following text while preserving its
    original meaning. Make it more formal and scholarly, but ensure it remains clear
    and accessible.
    
    Original text:
    {text}
    
    Provide the enhanced version with improved academic tone."""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert academic writing assistant."},
            {"role": "user", "content": prompt.format(text=text)}
        ],
        temperature=0.5,
    )
    
    return response.choices[0].message.content

async def generate_research_questions(topic: str, context: str) -> List[str]:
    """
    Generate potential research questions based on a topic and context.
    """
    prompt = """Generate thoughtful and academically rigorous research questions based on
    the following topic and context. Consider different angles, methodologies, and
    theoretical frameworks.
    
    Topic: {topic}
    Context: {context}
    
    Provide a list of potential research questions with brief explanations of their
    significance."""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert academic researcher."},
            {"role": "user", "content": prompt.format(topic=topic, context=context)}
        ],
        temperature=0.8,
    )
    
    # Parse response into list of questions
    questions = response.choices[0].message.content.split("\n")
    return [q.strip() for q in questions if q.strip()]

async def generate_outline(
    topic: str,
    context: str,
    outline_type: str = "research_paper"
) -> Dict[str, Any]:
    """
    Generate a structured outline for academic writing.
    """
    outline_templates = {
        "research_paper": """
        1. Introduction
           - Background
           - Research Problem
           - Research Questions
           - Significance
        2. Literature Review
           - Theoretical Framework
           - Current Research
           - Research Gaps
        3. Methodology
           - Research Design
           - Data Collection
           - Analysis Methods
        4. Results
           - Key Findings
           - Data Analysis
        5. Discussion
           - Interpretation
           - Implications
           - Limitations
        6. Conclusion
           - Summary
           - Future Research
        """,
        "thesis": """
        1. Introduction
           - Research Context
           - Problem Statement
           - Research Objectives
           - Thesis Structure
        2. Literature Review
           - Theoretical Background
           - Critical Analysis
           - Research Gap
        3. Methodology
           - Research Philosophy
           - Research Approach
           - Methods and Tools
           - Data Collection
        4. Results and Analysis
           - Data Presentation
           - Analysis
           - Key Findings
        5. Discussion
           - Theoretical Implications
           - Practical Implications
           - Limitations
        6. Conclusion
           - Research Summary
           - Contributions
           - Future Research
        """
    }

    prompt = f"""Generate a detailed academic outline for the following topic:
    Topic: {topic}
    Context: {context}
    Type: {outline_type}

    Base Structure:
    {outline_templates.get(outline_type, outline_templates["research_paper"])}

    Please provide a detailed outline with:
    1. Clear section headers
    2. Relevant subsections
    3. Key points to address
    4. Suggested content for each section"""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert academic writing consultant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    
    return {
        "outline": response.choices[0].message.content,
        "outline_type": outline_type,
        "topic": topic
    }

async def analyze_literature(text: str) -> Dict[str, Any]:
    """
    Analyze literature review content and provide suggestions.
    """
    prompt = """Analyze this literature review section and provide:
    1. Synthesis of key themes
    2. Identification of research gaps
    3. Suggestions for additional sources
    4. Critique of current arguments
    5. Potential theoretical frameworks

    Text:
    {text}"""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert academic researcher."},
            {"role": "user", "content": prompt.format(text=text)}
        ],
        temperature=0.7,
    )
    
    return {
        "analysis": response.choices[0].message.content,
        "text_length": len(text)
    }

async def suggest_methodology(
    research_type: str,
    research_questions: List[str],
    context: str
) -> Dict[str, Any]:
    """
    Suggest appropriate research methodologies.
    """
    prompt = f"""Based on the following research details, suggest appropriate methodologies:
    
    Research Type: {research_type}
    Research Questions:
    {chr(10).join(f'- {q}' for q in research_questions)}
    
    Context:
    {context}
    
    Please provide:
    1. Recommended research methods
    2. Data collection approaches
    3. Analysis techniques
    4. Potential limitations
    5. Alternative approaches
    6. Sampling strategies
    7. Validity considerations"""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert research methodologist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    
    return {
        "methodology_suggestions": response.choices[0].message.content,
        "research_type": research_type
    }

async def generate_abstract(
    title: str,
    content: Dict[str, str],
    max_words: int = 250
) -> str:
    """
    Generate an academic abstract from paper content.
    """
    prompt = f"""Generate an academic abstract for the following paper:
    
    Title: {title}
    
    Content:
    - Introduction: {content.get('introduction', '')}
    - Methods: {content.get('methods', '')}
    - Results: {content.get('results', '')}
    - Conclusion: {content.get('conclusion', '')}
    
    Requirements:
    1. Maximum {max_words} words
    2. Include research purpose
    3. Highlight methodology
    4. Summarize key findings
    5. State main conclusions
    6. Follow academic style"""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert academic editor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
    )
    
    return response.choices[0].message.content

async def suggest_keywords(
    title: str,
    abstract: str,
    num_keywords: int = 5
) -> List[str]:
    """
    Generate relevant academic keywords.
    """
    prompt = f"""Generate {num_keywords} relevant academic keywords for:
    
    Title: {title}
    Abstract: {abstract}
    
    Requirements:
    1. Include broad field terms
    2. Include specific methodology terms
    3. Include key concepts
    4. Consider SEO and discoverability
    5. Follow academic conventions"""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in academic publishing."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
    )
    
    keywords = response.choices[0].message.content.split("\n")
    return [k.strip() for k in keywords if k.strip()]

async def format_reference(
    reference_text: str,
    style: str = "apa",
    version: str = "7"
) -> str:
    """
    Format a reference according to specified citation style.
    Supports APA, MLA, Chicago, Harvard, and Vancouver styles.
    """
    style_guides = {
        "apa": f"APA {version}th Edition",
        "mla": f"MLA {version}th Edition",
        "chicago": f"Chicago Manual of Style {version}th Edition",
        "harvard": "Harvard Referencing Style",
        "vancouver": "Vancouver Citation Style"
    }

    prompt = f"""Format the following reference according to {style_guides.get(style.lower(), "APA 7th Edition")}:

    Reference:
    {reference_text}

    Please ensure:
    1. Correct ordering of elements
    2. Proper punctuation
    3. Correct capitalization
    4. Proper formatting of author names
    5. Accurate date formatting"""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in academic citation styles."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )
    
    return response.choices[0].message.content.strip()

async def check_style_guide(
    text: str,
    style_guide: str = "apa",
    elements: List[str] = ["citations", "headings", "numbers", "abbreviations"]
) -> Dict[str, Any]:
    """
    Check text against academic style guide requirements.
    """
    prompt = f"""Review the following text for compliance with {style_guide.upper()} style guide,
    focusing on: {', '.join(elements)}.
    
    Text:
    {text}
    
    For each element, provide:
    1. Style guide rule
    2. Current usage
    3. Suggested corrections
    4. Explanation
    
    Format the response as a structured analysis."""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in academic style guides."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
    )
    
    return {
        "analysis": response.choices[0].message.content,
        "style_guide": style_guide,
        "elements_checked": elements
    }

async def extract_citations(text: str) -> List[Dict[str, str]]:
    """
    Extract and parse citations from text.
    """
    prompt = """Extract and analyze all citations from the following text.
    For each citation, identify:
    1. Citation type (in-text, parenthetical)
    2. Authors
    3. Year
    4. Page numbers (if present)
    5. Context of usage

    Text:
    {text}"""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in academic citations."},
            {"role": "user", "content": prompt.format(text=text)}
        ],
        temperature=0.3,
    )
    
    # Parse the response into structured citations
    citations = []
    citation_text = response.choices[0].message.content
    
    # Simple parsing of citation blocks
    citation_blocks = re.split(r'\n\d+\.\s+', citation_text)
    for block in citation_blocks[1:]:  # Skip the first empty block
        citations.append({
            "text": block.strip(),
            "extracted": True
        })
    
    return citations

async def suggest_transitions(
    paragraphs: List[str]
) -> List[Dict[str, str]]:
    """
    Suggest transition sentences between paragraphs.
    """
    suggestions = []
    
    for i in range(len(paragraphs) - 1):
        prompt = f"""Suggest a transition sentence between these two paragraphs:
        
        Paragraph 1:
        {paragraphs[i]}
        
        Paragraph 2:
        {paragraphs[i + 1]}
        
        Requirements:
        1. Maintain academic tone
        2. Create logical flow
        3. Highlight relationship between ideas
        4. Be concise but effective"""

        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert academic writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        suggestions.append({
            "before": paragraphs[i],
            "after": paragraphs[i + 1],
            "suggestion": response.choices[0].message.content.strip()
        })
    
    return suggestions

async def check_argument_structure(text: str) -> Dict[str, Any]:
    """
    Analyze and provide feedback on argument structure.
    """
    prompt = """Analyze the argument structure in this text. Provide:
    1. Main claims identification
    2. Evidence assessment
    3. Logical flow analysis
    4. Counter-argument consideration
    5. Suggestions for strengthening arguments
    
    Text:
    {text}"""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in academic argumentation."},
            {"role": "user", "content": prompt.format(text=text)}
        ],
        temperature=0.6,
    )
    
    return {
        "analysis": response.choices[0].message.content,
        "text_length": len(text)
    }

async def suggest_evidence(claim: str, field: str) -> List[Dict[str, str]]:
    """
    Suggest types of evidence to support an academic claim.
    """
    prompt = f"""For the following academic claim in the field of {field},
    suggest appropriate types of evidence to support it:
    
    Claim: {claim}
    
    Please suggest:
    1. Empirical evidence types
    2. Theoretical support
    3. Methodological approaches
    4. Potential data sources
    5. Specific examples or cases"""

    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert academic researcher."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    
    # Parse suggestions into structured format
    suggestions = []
    suggestion_text = response.choices[0].message.content
    
    # Simple parsing of suggestion blocks
    suggestion_blocks = re.split(r'\n\d+\.\s+', suggestion_text)
    for block in suggestion_blocks[1:]:
        suggestions.append({
            "evidence_type": block.split(':')[0].strip() if ':' in block else "General",
            "suggestion": block.split(':')[1].strip() if ':' in block else block.strip()
        })
    
    return suggestions
