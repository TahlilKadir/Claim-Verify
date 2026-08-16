from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.schemas import ClaimRequest, VerificationResult
from services.gemini_service import generate_verification
from services.search_service import search_web
from services.source_service import prepare_source, filter_sources
from services.confidence_service import calculate_confidence


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "ClaimVerify API is running!"}


@app.post("/test-search")
def test_search(request: ClaimRequest):
    results = search_web(request.claim)

    return {
        "query": request.claim,
        "results": results
    }


@app.post("/verify", response_model=VerificationResult)
def verify_claim(request: ClaimRequest):

    search_results = search_web(request.claim)

    prepared_sources = [
        prepare_source(source)
        for source in search_results
    ]

    filtered_sources = filter_sources(
        prepared_sources
    )

    result = generate_verification(
        request.claim,
        filtered_sources
    )

    source_quality_map = {
        source["title"]: source.get(
            "source_quality",
            0.5
        )
        for source in filtered_sources
    }

    evidence = result.get("evidence", [])

    for item in evidence:
        title = item.get("source_title", "")

        item["source_quality"] = source_quality_map.get(
            title,
            0.5
        )

    confidence = calculate_confidence(
        result.get("verdict", "uncertain"),
        evidence
    )

    public_evidence = []

    for item in evidence:
        public_item = {
            key: value
            for key, value in item.items()
            if key != "source_quality"
        }

        public_evidence.append(public_item)

    return {
        **result,
        "confidence": confidence,
        "evidence": public_evidence,
        "sources": filtered_sources
    }
