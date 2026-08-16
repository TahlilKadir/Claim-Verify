from pydantic import BaseModel


class ClaimRequest(BaseModel):
    claim: str


class Source(BaseModel):
    title: str
    url: str
    content: str
    relevance_score: float
    source_type: str


class EvidenceAssessment(BaseModel):
    source_title: str
    relationship: str
    evidence_strength: float
    reasoning: str


class VerificationResult(BaseModel):
    verdict: str
    confidence: float
    claim_scope: str
    explanation: str
    limitations: list[str]
    evidence: list[EvidenceAssessment]
    sources: list[Source]