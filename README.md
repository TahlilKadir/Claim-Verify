ClaimVerify is an AI-powered claim verification platform that analyzes factual statements and determines whether they are supported, refuted, or uncertain based on available evidence. Users can enter a claim and receive a structured verification report containing the verdict, confidence score, explanation, claim scope, limitations, evidence analysis, and source references.

**Features**

Claim Verification — Submit factual claims for AI-assisted analysis.
AI-Powered Analysis — Uses Google Gemini to evaluate claims and available evidence.
Structured Verdicts — Classifies claims as supported, refuted, or uncertain.
Confidence Scoring — Provides a confidence percentage alongside the verdict.
Evidence-Based Explanation — Explains the reasoning behind the result.
Source References — Displays the sources consulted during verification.
Evidence Analysis — Shows how individual sources support or contradict the claim.
Limitations — Highlights factors that should be considered when interpreting the result.
Responsive React Interface — Clean, focused UI designed around the verification workflow.


**Tech Stack**

Frontend:

React
Vite
JavaScript
CSS

Backend:

Python
FastAPI
Uvicorn

AI:

Google Gemini API


**How It Works**

User enters a claim
        ↓
React frontend
        ↓
FastAPI backend
        ↓
Google Gemini
        ↓
Claim + evidence analysis
        ↓
Structured verification result
        ↓
React result interface

The frontend sends the user's claim to the FastAPI backend through an HTTP request. The backend passes the claim to Gemini for analysis and processes the returned information into a structured response. React then dynamically presents the verdict, confidence, reasoning, evidence, limitations, and references.

The goal of ClaimVerify is to explore how LLMs, evidence-based reasoning, and modern web technologies can be combined to create a more transparent approach to evaluating online claims.

ClaimVerify doesn't simply provide an answer — it shows the reasoning, evidence, and sources behind the result.
