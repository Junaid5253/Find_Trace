def rank_candidates(rows):
    """
    Rank potential missing-person matches using multiple evidence signals.

    The ranking combines:
        - Face similarity
        - Description similarity
        - Age/gender metadata
        - Geographic proximity

    Returns candidates sorted from strongest to weakest match.
    """

    weights = {
        "face_score": 0.60,
        "text_score": 0.10,
        "metadata_score": 0.15,
        "location_score": 0.15,
    }

    for r in rows:

        face_score = float(r.get("face_score", 0.0) or 0.0)
        text_score = float(r.get("text_score", 0.0) or 0.0)
        metadata_score_value = float(r.get("metadata_score", 0.0) or 0.0)
        location_score_value = float(r.get("location_score", 0.0) or 0.0)

        # Make sure every component stays within [0, 1]
        face_score = max(0.0, min(1.0, face_score))
        text_score = max(0.0, min(1.0, text_score))
        metadata_score_value = max(0.0, min(1.0, metadata_score_value))
        location_score_value = max(0.0, min(1.0, location_score_value))

        # Weighted overall score
        overall_score = (
            face_score * weights["face_score"]
            + text_score * weights["text_score"]
            + metadata_score_value * weights["metadata_score"]
            + location_score_value * weights["location_score"]
        )

        r["overall_score"] = round(overall_score * 100, 2)

        # Store individual contributions for explainability
        r["score_breakdown"] = {
            "face": round(face_score * weights["face_score"] * 100, 2),
            "description": round(
                text_score * weights["text_score"] * 100, 2
            ),
            "metadata": round(
                metadata_score_value * weights["metadata_score"] * 100, 2
            ),
            "location": round(
                location_score_value * weights["location_score"] * 100, 2
            ),
        }

        # Human-readable evidence
        evidence = []

        if face_score >= 0.85:
            evidence.append("Strong facial similarity")
        elif face_score >= 0.70:
            evidence.append("Moderate facial similarity")

        if text_score >= 0.80:
            evidence.append("Strong description similarity")
        elif text_score >= 0.60:
            evidence.append("Moderate description similarity")

        if metadata_score_value >= 0.85:
            evidence.append("Age/gender information is highly consistent")
        elif metadata_score_value >= 0.65:
            evidence.append("Age/gender information is reasonably consistent")

        if location_score_value >= 0.80:
            evidence.append("Location is geographically close")
        elif location_score_value >= 0.50:
            evidence.append("Location is relatively close")

        r["evidence"] = evidence

    return sorted(
        rows,
        key=lambda x: x["overall_score"],
        reverse=True
    )