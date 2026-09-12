def metadata_score(query_age, query_gender, candidate_age, candidate_gender):
    """
    Calculate metadata similarity using age and gender.

    Returns:
        float: score between 0.0 and 1.0

    Age:
        Exact / very close ages receive higher scores.
        Larger differences gradually reduce the score.

    Gender:
        Matching gender = 1.0
        Unknown gender = 0.5
        Mismatch = 0.0
    """

    # -----------------------------
    # Gender score
    # -----------------------------

    query_gender = str(query_gender or "Unknown").strip().lower()
    candidate_gender = str(candidate_gender or "Unknown").strip().lower()

    if query_gender == "unknown" or candidate_gender == "unknown":
        gender_score = 0.5

    elif query_gender == candidate_gender:
        gender_score = 1.0

    else:
        gender_score = 0.0

    # -----------------------------
    # Age score
    # -----------------------------

    if query_age is None or candidate_age is None:
        age_score = 0.5

    else:
        try:
            query_age = float(query_age)
            candidate_age = float(candidate_age)

            if query_age <= 0 or candidate_age <= 0:
                age_score = 0.5

            else:
                age_difference = abs(query_age - candidate_age)

                # Very close ages
                if age_difference <= 1:
                    age_score = 1.0

                elif age_difference <= 3:
                    age_score = 0.9

                elif age_difference <= 5:
                    age_score = 0.75

                elif age_difference <= 8:
                    age_score = 0.55

                elif age_difference <= 12:
                    age_score = 0.30

                else:
                    age_score = 0.10

        except (ValueError, TypeError):
            age_score = 0.5

    # -----------------------------
    # Final metadata score
    # -----------------------------

    score = (
        0.50 * gender_score
        + 0.50 * age_score
    )

    return round(score, 4)