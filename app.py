import streamlit as st
from pathlib import Path
import pandas as pd

from database.store import CandidateStore
from matching.ranking import rank_candidates
from agents.investigation_agent import generate_investigation_report
from vision.face_engine import FaceEngine
from nlp.text_engine import TextEngine
from matching.metadata import metadata_score
from matching.location import location_score

BASE = Path(__file__).parent
CANDIDATE_DIR = BASE / "candidates"
CANDIDATE_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="FindTrace", page_icon="🔎", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #14252b;
    --muted: #6a7b80;
    --line: #dce6e5;
    --paper: #f7faf8;
    --white: #ffffff;
    --teal: #0d7c76;
    --teal-dark: #07544f;
    --mint: #dff3ec;
}

html, body, [class*="css"] { font-family: 'Manrope', sans-serif; }
.stApp { background: var(--paper); color: var(--ink); }
[data-testid="stHeader"] { background: rgba(247, 250, 248, 0.88); }
[data-testid="stSidebar"] { background: #102f33; border-right: 0; }
[data-testid="stSidebar"] * { color: #e9f3ef; }
[data-testid="stSidebar"] .stCaption { color: #9fc1ba; }
[data-testid="stSidebar"] hr { border-color: rgba(220, 244, 236, .16); }
[data-testid="stSidebar"] [data-testid="stRadio"] label { padding: .52rem .65rem; border-radius: 8px; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background: rgba(255,255,255,.08); }
[data-testid="stSidebar"] [data-testid="stRadio"] > div { gap: .2rem; }

.brand { padding: .35rem 0 1.8rem; }
.brand-mark { display: inline-flex; align-items: center; justify-content: center; width: 34px; height: 34px; margin-right: 9px; border-radius: 9px; background: #c2eee0; color: #0b615a; font-size: 19px; font-weight: 800; vertical-align: middle; }
.brand-name { font-size: 1.27rem; font-weight: 800; letter-spacing: -.03em; vertical-align: middle; }
.brand-sub { margin: .7rem 0 0 43px; color: #9fc1ba; font-size: .75rem; line-height: 1.45; }
.eyebrow { color: var(--teal); font-family: 'DM Mono', monospace; font-size: .72rem; letter-spacing: .1em; text-transform: uppercase; font-weight: 500; margin-bottom: .35rem; }
.page-title { color: var(--ink); font-size: 2rem; font-weight: 800; letter-spacing: -.045em; line-height: 1.1; margin: 0; }
.page-intro { color: var(--muted); font-size: .96rem; margin: .5rem 0 1.55rem; }
.section-label { color: var(--ink); font-size: 1.05rem; font-weight: 800; letter-spacing: -.02em; margin: 1.7rem 0 .7rem; }
.metric-card { min-height: 108px; padding: 1.05rem 1.2rem; border: 1px solid var(--line); border-radius: 12px; background: var(--white); box-shadow: 0 5px 18px rgba(23, 61, 60, .045); }
.metric-label { color: var(--muted); font-size: .75rem; font-weight: 700; text-transform: uppercase; letter-spacing: .07em; }
.metric-value { color: var(--ink); font-size: 1.75rem; font-weight: 800; letter-spacing: -.05em; margin-top: .35rem; }
.metric-note { color: var(--teal); font-size: .72rem; margin-top: .15rem; }
.notice { display: flex; align-items: flex-start; gap: .7rem; padding: .9rem 1rem; border: 1px solid #b9ded3; border-radius: 10px; background: var(--mint); color: #1b504a; font-size: .84rem; line-height: 1.5; }
.notice-icon { font-weight: 800; color: var(--teal); }
.match-card { padding: 1rem; border: 1px solid var(--line); border-radius: 12px; background: var(--white); box-shadow: 0 5px 18px rgba(23, 61, 60, .045); margin-bottom: .75rem; }
.match-rank { color: var(--teal); font-family: 'DM Mono', monospace; font-size: .74rem; }
.match-name { color: var(--ink); font-size: 1.05rem; font-weight: 800; margin: .2rem 0 .55rem; }
.score { color: var(--teal-dark); font-size: 1.45rem; font-weight: 800; letter-spacing: -.04em; text-align: right; }
.score-label { color: var(--muted); font-size: .68rem; text-align: right; text-transform: uppercase; letter-spacing: .07em; }
.bar { height: 6px; background: #e6efed; border-radius: 99px; overflow: hidden; margin: .7rem 0 .8rem; }
.bar-fill { height: 100%; background: var(--teal); border-radius: inherit; }
.evidence { color: var(--muted); font-family: 'DM Mono', monospace; font-size: .68rem; line-height: 1.65; }
.verification { color: #966322; font-size: .73rem; font-weight: 700; margin-top: .6rem; }
.about-panel { padding: 1.3rem 1.45rem; border: 1px solid var(--line); border-radius: 12px; background: var(--white); }
.stButton > button, .stFormSubmitButton > button { border-radius: 8px; font-weight: 700; min-height: 2.65rem; }
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] { background: var(--teal); border-color: var(--teal); }
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover { background: var(--teal-dark); border-color: var(--teal-dark); }
div[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 10px; overflow: hidden; }
div[data-testid="stForm"] { padding: 1.1rem 1.2rem .35rem; border: 1px solid var(--line); border-radius: 12px; background: var(--white); }
div[data-testid="stFileUploaderDropzone"] { border-color: #b9d8d1; background: #f5fbf8; }
</style>
""", unsafe_allow_html=True)


def page_header(eyebrow, title, intro):
    st.markdown(f'<div class="eyebrow">{eyebrow}</div><h1 class="page-title">{title}</h1><div class="page-intro">{intro}</div>', unsafe_allow_html=True)


def metric_card(label, value, note):
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)


def match_card(rank, result):
    overall = result["overall_score"]
    with st.container(border=True):
        image_column, details_column = st.columns([1, 3])
        with image_column:
            image_path = Path(result["image_path"])
            if image_path.exists():
                st.image(str(image_path), width=150)
            else:
                st.caption("Photo unavailable")
        with details_column:
            st.markdown(f"""
            <div class="match-card">
                <div class="match-rank">MATCH 0{rank}</div>
                <div class="match-name">{result['name']}</div>
                <div class="score">{overall:.1f}%</div>
                <div class="score-label">overall relevance</div>
                <div class="bar"><div class="bar-fill" style="width: {max(0, min(100, overall)):.1f}%"></div></div>
                <div class="evidence">FACE {result['face_score'] * 100:.1f}%  /  TEXT {result['text_score'] * 100:.1f}%  /  META {result['metadata_score'] * 100:.1f}%  /  LOCATION {result['location_score'] * 100:.1f}%</div>
                <div class="verification">Potential match - human verification required</div>
            </div>
            """, unsafe_allow_html=True)

@st.cache_resource
def get_store():
    return CandidateStore(BASE / "data" / "findtrace.db")

@st.cache_resource
def get_face_engine():
    return FaceEngine()

@st.cache_resource
def get_text_engine():
    return TextEngine()

store = get_store()

st.sidebar.markdown('<div class="brand"><span class="brand-mark">F</span><span class="brand-name">FindTrace</span><div class="brand-sub">Investigation intelligence<br>for authorized teams</div></div>', unsafe_allow_html=True)
st.sidebar.caption("WORKSPACE")
page = st.sidebar.radio("Navigate", ["Dashboard", "New Case", "Candidate Records", "About"], label_visibility="collapsed")
st.sidebar.markdown("---")
st.sidebar.caption("Human verification is required for every potential match.")

if page == "Dashboard":
    page_header("Operations overview", "Investigation workspace", "Review case activity and system readiness at a glance.")
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Candidate records", store.count(), "Available for matching")
    with c2:
        metric_card("Open cases", store.count_cases(status="Open"), "Awaiting review")
    with c3:
        metric_card("System status", "Ready", "All services operational")
    st.markdown('<div style="height: 1rem"></div><div class="notice"><span class="notice-icon">!</span><span>FindTrace ranks potential matches to support an investigator. It does not confirm identity, and every result requires human verification.</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Recent case activity</div>', unsafe_allow_html=True)
    cases = store.list_cases()
    if cases:
        st.dataframe(pd.DataFrame(cases), width="stretch")
    else:
        st.info("No cases yet. Create your first investigation from New Case.")

elif page == "New Case":
    page_header("New investigation", "Create a case", "Provide the strongest available evidence to generate a ranked shortlist.")
    with st.form("case_form"):
        left, right = st.columns(2)
        with left:
            name = st.text_input("Missing person name (optional)")
            age = st.number_input("Approximate age", min_value=0, max_value=120, value=25)
            gender = st.selectbox("Gender", ["Unknown", "Male", "Female"])
            last_location = st.text_input("Last known location", placeholder="Islamabad, Pakistan")
            date_missing = st.date_input("Date last seen")
        with right:
            description = st.text_area("Physical / clothing description", placeholder="Black shirt, blue jeans, short black hair...")
            photo = st.file_uploader("Upload missing-person photo", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("Create case and search", type="primary", width="stretch")

    if submitted:
        if photo is None:
            st.error("Please upload a clear photo.")
            st.stop()
        if store.count() == 0:
            st.warning("There are no candidate records yet. Add records under Candidate Records first.")
            st.stop()

        case_id = store.create_case(name, int(age), gender, last_location, str(date_missing), description)
        photo_path = BASE / "case_uploads" / f"case_{case_id}.jpg"
        photo_path.write_bytes(photo.getvalue())

        with st.spinner("Analyzing face and searching candidate records..."):
            face_engine = get_face_engine()
            text_engine = get_text_engine()
            query_embedding = face_engine.embedding_from_path(photo_path)
            if query_embedding is None:
                st.error("No usable face was detected. Try a clearer, front-facing image.")
                st.stop()

            candidates = store.get_candidates_with_embeddings()
            text_query = description or ""
            results = []
            for candidate in candidates:
                face_score = face_engine.similarity(query_embedding, candidate["embedding"])
                text_score = text_engine.similarity(text_query, candidate.get("description", ""))
                meta = metadata_score(age, gender, candidate.get("age"), candidate.get("gender"))
                loc = location_score(last_location, candidate.get("location", ""))
                results.append({
                    **candidate,
                    "face_score": face_score,
                    "text_score": text_score,
                    "metadata_score": meta,
                    "location_score": loc,
                })

            ranked = rank_candidates(results)
            store.save_results(case_id, ranked)

        st.markdown(f'<div class="notice"><span class="notice-icon">OK</span><span>Case #{case_id} created. Review the highest-relevance records below.</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Ranked potential matches</div>', unsafe_allow_html=True)
        for i, r in enumerate(ranked[:5], 1):
            match_card(i, r)

        with st.spinner("Generating explainable investigation summary..."):
            report = generate_investigation_report(name, age, gender, last_location, description, ranked[:5])
        st.markdown('<div class="section-label">Investigation summary</div>', unsafe_allow_html=True)
        st.markdown(report)

elif page == "Candidate Records":
    page_header("Evidence library", "Candidate records", "Manage unidentified-person records that can be searched during an investigation.")
    with st.form("candidate_form"):
        name = st.text_input("Record name / identifier", placeholder="UP-0001")
        age = st.number_input("Approximate age", min_value=0, max_value=120, value=25)
        gender = st.selectbox("Gender", ["Unknown", "Male", "Female"], key="candidate_gender")
        location = st.text_input("Location", placeholder="Lahore, Pakistan")
        description = st.text_area("Physical / clothing description")
        photo = st.file_uploader("Candidate face photo", type=["jpg", "jpeg", "png"], key="candidate_photo")
        add = st.form_submit_button("Add candidate record", type="primary", width="stretch")
    if add:
        if not photo or not name:
            st.error("Name/identifier and photo are required.")
        else:
            path = CANDIDATE_DIR / f"{store.next_candidate_id()}_{Path(photo.name).name}"
            path.write_bytes(photo.getvalue())
            with st.spinner("Extracting face embedding..."):
                emb = get_face_engine().embedding_from_path(path)
            if emb is None:
                st.error("No usable face detected in that image.")
            else:
                store.add_candidate(name, int(age), gender, location, description, str(path), emb)
                st.success("Candidate record added.")
    records = store.list_candidates()
    st.markdown('<div class="section-label">Stored records</div>', unsafe_allow_html=True)
    if records:
        st.dataframe(pd.DataFrame(records), width="stretch")
    else:
        st.info("No candidate records yet. Add a record above to enable case matching.")

elif page == "About":
    page_header("System notes", "About FindTrace", "A decision-support workspace for authorized investigators and NGOs.")
    st.markdown("""
<div class="about-panel">
<p><strong>FindTrace</strong> is an AI-assisted investigation prototype for authorized investigators and NGOs.</p>
<p><strong>Pipeline:</strong> Face detection/embedding &rarr; vector similarity &rarr; semantic description matching &rarr; metadata/location scoring &rarr; explainable ranking &rarr; human verification.</p>
<p>The prototype intentionally does <strong>not</strong> make an identity-confirmation claim. A high score means a record deserves human review.</p>

<h3>AI components</h3>
<ul>
    <li><strong>InsightFace / ArcFace</strong> &mdash; face representation</li>
    <li><strong>Sentence-BERT</strong> &mdash; semantic text similarity</li>
    <li><strong>FAISS-ready architecture</strong> &mdash; vector retrieval can be enabled as the dataset grows</li>
    <li><strong>Investigation Agent</strong> &mdash; produces an evidence summary from deterministic scores</li>
</ul>

<h3>Privacy</h3>
<p>Use only lawfully obtained, appropriately licensed data. Do not publish real missing-person or unidentified-person images in a public demo without authorization.</p>

</div>
""", unsafe_allow_html=True)
