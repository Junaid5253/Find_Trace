# FindTrace — AI Missing Person Identification & Investigation System

FindTrace is a Streamlit/Python prototype that helps authorized investigators rank potential matches between a missing-person case and unidentified-person records.

## What it does

1. Upload a missing-person photo and case information.
2. Extract a face embedding with InsightFace/ArcFace.
3. Compare it against stored candidate embeddings.
4. Compare physical descriptions using Sentence-BERT.
5. Score age/gender and location consistency.
6. Produce a ranked shortlist with an evidence breakdown.
7. Generate a human-verification investigation summary.

**Important:** a ranking is not an identity confirmation. The system is designed as a decision-support prototype with a human in the loop.

## Tech stack

- Python 3.11
- Streamlit
- InsightFace / ArcFace (`buffalo_l`)
- Sentence-BERT (`all-MiniLM-L6-v2`)
- SQLite
- NumPy / Pandas / OpenCV

InsightFace's current Python package supports Python 3.10+ and its default FaceAnalysis model pack is `buffalo_l`. The model files have separate licensing terms from the open-source code, so review the current model license before any non-research/commercial deployment.

## Run locally

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

On first use, InsightFace and Sentence-BERT may download model files. A CPU-only machine can take a while.

## Streamlit Cloud

Push the repository to GitHub and deploy `app.py` from Streamlit Community Cloud. Select Python 3.11 in Advanced settings if needed. Keep `requirements.txt` in the repository root.

For a serious deployment, move candidate images/embeddings and case data out of the local filesystem into a persistent database/object store and add proper authentication/authorization.

## Hackathon MVP demo

For the fastest demo:

1. Add 5–20 lawfully sourced or synthetic candidate face records under **Candidate Records**.
2. Create a new case using a different photo of one of those same people.
3. Show the top-ranked result and its face/text/metadata/location evidence.
4. Show the investigation summary and the human-verification warning.

## Next upgrades

- FAISS index for thousands+ of embeddings
- Proper investigator authentication and role-based access
- Persistent cloud storage
- Map/geospatial distance scoring
- Better date reasoning
- LLM-powered investigation agent with tool calls
- Multilingual reports
- Evaluation dashboard: Top-1/Top-5/Top-10 retrieval and false-positive analysis
