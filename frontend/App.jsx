import { useState } from "react";
import "./App.css";

function App() {
  const [claim, setClaim] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const verifyClaim = async () => {
    if (!claim.trim()) {
      setError("Please enter a claim first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/verify", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          claim: claim.trim(),
        }),
      });

      if (!response.ok) {
        throw new Error("Verification request failed.");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(
        "Could not connect to the verification server. Make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && event.ctrlKey) {
      verifyClaim();
    }
  };

  const getVerdictClass = (verdict) => {
    switch (verdict?.toLowerCase()) {
      case "supported":
        return "supported";

      case "refuted":
        return "refuted";

      default:
        return "uncertain";
    }
  };

  return (
    <div className="app">
      <main className="main">

        {/* Hero */}
        <section className="hero">
          <div className="hero-eyebrow">
            <span className="eyebrow-dot"></span>
            VERIFY BEFORE YOU BELIEVE
          </div>

          <h1>
            Verify a claim.
            <span> Know what the evidence says.</span>
          </h1>

          <p>
            Enter a factual claim and ClaimVerify will search the web,
            evaluate the available evidence, and determine whether the
            claim is supported, refuted, or uncertain.
          </p>
        </section>


        {/* Claim Input */}
        <section className="verification-card">
          <div className="card-header">
            <p
              style={{
                margin: 0,
                fontSize: "1rem",
                fontWeight: 600,
                lineHeight: 1.5,
                textAlign: "center",
                color: "#1c2741",
              }}
            >
              Enter a statement you want ClaimVerify to investigate:
            </p>
          </div>

          <textarea
            id="claim"
            value={claim}
            onChange={(event) => {
              setClaim(event.target.value);
              if (error) setError("");
            }}
            onKeyDown={handleKeyDown}
            placeholder="e.g. Electric vehicles produce fewer greenhouse gas emissions than gasoline cars over their lifetime."
            rows="5"
          />

          <div className="card-footer">
            <span className="character-count">
              {claim.length} characters
            </span>

            <button
              onClick={verifyClaim}
              disabled={loading}
              className="verify-button"
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Verifying
                </>
              ) : (
                <>
                  Verify Claim
                  <span className="button-arrow">→</span>
                </>
              )}
            </button>
          </div>

          {error && <p className="error-message">{error}</p>}
        </section>


        {/* Loading */}
        {loading && (
          <section className="loading-card">
            <div className="loading-icon">
              <span></span>
            </div>

            <div>
              <strong>Analyzing your claim</strong>
              <p>
                Searching sources and evaluating the available evidence...
              </p>
            </div>
          </section>
        )}


        {/* Results */}
        {result && !loading && (
          <section className="result-section">

            {/* Result Header */}
            <div className="result-heading">
              <div>
                <div className="section-eyebrow">
                  VERIFICATION RESULT
                </div>

                <h2>Here's what we found.</h2>
              </div>
            </div>


            {/* Main Result Card */}
            <div className="result-card">

              {/* Result Summary */}
              <div className="result-summary">

                <div className="verdict-area">
                  <div className="result-label">VERDICT</div>

                  <div
                    className={`verdict-badge ${getVerdictClass(
                      result.verdict
                    )}`}
                  >
                    <span className="verdict-dot"></span>
                    {result.verdict}
                  </div>
                </div>

                <div className="confidence-area">
                  <div className="result-label">CONFIDENCE</div>

                  <div className="confidence-row">
                    <div className="confidence-value">
                      {Math.round(result.confidence * 100)}
                      <span>%</span>
                    </div>

                    <div className="confidence-bar">
                      <div
                        style={{
                          width: `${Math.round(
                            result.confidence * 100
                          )}%`,
                        }}
                      ></div>
                    </div>
                  </div>
                </div>

              </div>


              {/* Explanation */}
              <div className="result-content">
                <div className="result-label">
                  EXPLANATION
                </div>

                <p>{result.explanation}</p>
              </div>


              {/* Claim Scope */}
              {result.claim_scope && (
                <div className="result-content scope-content">
                  <div className="result-label">
                    CLAIM SCOPE
                  </div>

                  <p>{result.claim_scope}</p>
                </div>
              )}

            </div>


            {/* Limitations */}
            {result.limitations?.length > 0 && (
              <div className="secondary-card">

                <div className="secondary-card-header">
                  <div className="secondary-icon">
                    !
                  </div>

                  <div>
                    <div className="result-label">
                      LIMITATIONS
                    </div>

                    <h3>
                      Things worth keeping in mind
                    </h3>
                  </div>
                </div>


                <div className="limitations-list">
                  {result.limitations.map((limitation, index) => (
                    <div
                      className="limitation"
                      key={index}
                    >
                      <span></span>

                      <p>{limitation}</p>
                    </div>
                  ))}
                </div>

              </div>
            )}


            {/* Evidence */}
            {result.evidence?.length > 0 && (
              <div className="secondary-card evidence-card">

                <div className="secondary-card-header">

                  <div className="secondary-icon evidence-icon">
                    ✓
                  </div>

                  <div>
                    <div className="result-label">
                      SOURCE ANALYSIS
                    </div>

                    <h3>
                      How the evidence supports the verdict
                    </h3>
                  </div>

                  <span className="source-count">
                    {result.evidence.length} sources
                  </span>

                </div>


                <div className="evidence-list">

                  {result.evidence.map((item, index) => (
                    <div
                      className="evidence-item"
                      key={index}
                    >

                      <div className="evidence-top">

                        <div className="evidence-source">

                          <h4>
                            {item.source_title}
                          </h4>

                          <span
                            className={`relationship ${item.relationship}`}
                          >
                            {item.relationship}
                          </span>

                        </div>


                        {item.evidence_strength !== undefined && (
                          <span className="evidence-strength">
                            {Math.round(
                              item.evidence_strength * 100
                            )}
                            %
                          </span>
                        )}

                      </div>


                      <p>
                        {item.reasoning}
                      </p>

                    </div>
                  ))}

                </div>

              </div>
            )}


            {/* References */}
            {result.sources?.length > 0 && (
              <div className="secondary-card">

                <div className="secondary-card-header">

                  <div className="secondary-icon source-icon">
                    ↗
                  </div>

                  <div>
                    <div className="result-label">
                      REFERENCES
                    </div>

                    <h3>
                      Sources consulted
                    </h3>
                  </div>

                </div>


                <div className="sources-list">

                  {result.sources.map((source, index) => (
                    <a
                      href={source.url}
                      target="_blank"
                      rel="noreferrer"
                      className="source-link"
                      key={index}
                    >

                      <span>
                        {source.title}
                      </span>

                      <span>↗</span>

                    </a>
                  ))}

                </div>

              </div>
            )}

          </section>
        )}

      </main>
    </div>
  );
}

export default App;