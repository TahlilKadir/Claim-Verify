import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_verification(claim: str, sources: list) -> dict:
    evidence_text = ""

    for index, source in enumerate(sources, start=1):
        evidence_text += f"""
SOURCE {index}
Title: {source.get("title", "Unknown")}
URL: {source.get("url", "Unknown")}
Source type: {source.get("source_type", "general")}
Source quality: {source.get("source_quality", 0.5)}
Search relevance: {source.get("relevance_score", 0.0)}

Content:
{source.get("content", "")}

"""

    prompt = f"""
You are an evidence-based claim verification assistant.

Your task is to evaluate a claim using ONLY the provided sources.

CLAIM:
{claim}

SOURCES:
{evidence_text}

First determine what the available evidence actually establishes.

Pay particular attention to broad or ambiguous wording.
Do not assume that evidence supporting one aspect of a claim proves
every possible interpretation of that claim.

Return ONLY valid JSON using exactly this structure:

{{
    "verdict": "supported | refuted | uncertain",
    "claim_scope": "What specific interpretation or aspect of the claim the evidence supports or refutes.",
    "explanation": "Brief explanation of the overall conclusion.",
    "limitations": [
        "Important limitation or qualification."
    ],
    "evidence": [
        {{
            "source_title": "Source title",
            "relationship": "supports | contradicts | qualifies | neutral",
            "evidence_strength": 0.0,
            "reasoning": "Brief explanation of what this source contributes."
        }}
    ]
}}

Rules:

- verdict must be exactly one of: supported, refuted, uncertain
- confidence must be between 0.0 and 1.0
- relationship must be exactly one of: supports, contradicts, qualifies, neutral
- Use "qualifies" when a source adds an important limitation, condition, exception, or nuance without directly supporting or contradicting the overall claim.
- evidence_strength must be between 0.0 and 1.0
- Use ONLY the supplied source content
- Do not use outside knowledge
- Do not invent facts
- Do not invent sources
- Do not assume that agreement between sources automatically means certainty
- Consider whether multiple sources may be repeating the same information
- Broad claims should receive lower confidence when the evidence only establishes a narrower interpretation
- If the evidence is insufficient or contradictory, use "uncertain"
- If the claim is substantially supported but requires an important qualification, keep "supported" but explain the qualification
- Confidence should reflect the strength and scope of the available evidence
- Do not automatically use 1.0 confidence
- Keep explanations concise
- Include an empty limitations array if there are no meaningful limitations
- Do not include markdown
- Do not include anything outside the JSON object
- Consider source quality when evaluating evidence strength
- A high search relevance score does not mean the source is authoritative
- Social media posts and user-generated content should generally receive less evidentiary weight unless they are themselves the primary evidence for the claim
- Government and academic sources may be strong evidence, but do not treat their source type as proof of correctness
- Evaluate the actual content of every source
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return json.loads(response.text)