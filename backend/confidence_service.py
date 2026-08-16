def calculate_confidence(
    verdict: str,
    evidence: list[dict]
) -> float:

    if not evidence:
        return 0.0

    support_scores = []
    contradiction_scores = []
    qualification_scores = []

    for item in evidence:

        strength = float(
            item.get("evidence_strength", 0.0)
        )

        quality = float(
            item.get("source_quality", 0.5)
        )

        score = strength * quality

        relationship = item.get(
            "relationship",
            "neutral"
        )

        if relationship == "supports":
            support_scores.append(score)

        elif relationship == "contradicts":
            contradiction_scores.append(score)

        elif relationship == "qualifies":
            qualification_scores.append(score)

    support_total = sum(support_scores)
    contradiction_total = sum(
        contradiction_scores
    )

    total_evidence = (
        support_total
        + contradiction_total
    )

    if total_evidence == 0:
        return 0.0

    if verdict == "supported":

        agreement = (
            support_total
            / total_evidence
        )

        average_quality = (
            support_total
            / len(support_scores)
            if support_scores
            else 0
        )

        confidence = (
            agreement * 0.6
            + average_quality * 0.4
        )

    elif verdict == "refuted":

        agreement = (
            contradiction_total
            / total_evidence
        )

        average_quality = (
            contradiction_total
            / len(contradiction_scores)
            if contradiction_scores
            else 0
        )

        confidence = (
            agreement * 0.6
            + average_quality * 0.4
        )

    else:
        confidence = 0.5

    return round(
        max(0.0, min(confidence, 1.0)),
        2
    )