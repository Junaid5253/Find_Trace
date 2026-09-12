def generate_investigation_report(name, age, gender, location, description, ranked):
    if not ranked:
        return "No candidates were ranked."
    top = ranked[0]
    lines = [
        "### Preliminary AI Assessment",
        f"The highest-ranked record is **{top['name']}** with an overall score of **{top['overall_score']:.1f}%**.",
        "",
        "**Evidence considered:**",
        f"- Face similarity: **{top['face_score']*100:.1f}%**",
        f"- Description similarity: **{top['text_score']*100:.1f}%**",
        f"- Age/gender consistency: **{top['metadata_score']*100:.1f}%**",
        f"- Location consistency: **{top['location_score']*100:.1f}%**",
        "",
        "**Recommended action:** manually verify the top candidates using authorized records and additional evidence.",
        "",
        "> **Important:** This is a ranking aid, not an identity confirmation. Do not take enforcement or other high-impact action based only on this score.",
    ]
    return "\n".join(lines)
