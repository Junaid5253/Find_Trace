# 🔎 FindTrace

### AI Missing Person Identification & Investigation System

FindTrace is an AI-assisted system designed to help authorized investigators, police departments, NGOs, and humanitarian organizations identify potential matches between missing-person reports and unidentified-person records.

Instead of relying on a single facial match, FindTrace combines **facial similarity, semantic description similarity, age, gender, geographic location, and investigation context** to rank potential candidates and provide an explainable investigation report.

> ⚠️ **Important:** FindTrace does not confirm a person's identity. Results are potential matches and must always be verified by an authorized human investigator.

---

## 🚀 What FindTrace Does

An investigator can:

1. Create a missing-person case.
2. Enter available information such as:

   * Name
   * Age
   * Gender
   * Last known location
   * Date last seen
   * Physical description
3. Upload a photograph.
4. Analyze the uploaded face using a pretrained face-recognition model.
5. Search candidate records using facial embeddings.
6. Compare additional information between the case and candidates.
7. Rank candidates based on multiple evidence sources.
8. Review the strongest potential matches.
9. Generate an AI-assisted investigation report.
10. Manually verify the results before taking any action.

---

## 🧠 How the AI Pipeline Works

```text
                 Missing Person Case
                         │
                         ▼
                  Uploaded Photo
                         │
                         ▼
              Face Detection & Analysis
                  InsightFace / ArcFace
                         │
                         ▼
                 Face Embedding
                         │
                         ▼
                    FAISS Search
                         │
                         ▼
              Top Candidate Retrieval
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
    Description      Metadata        Location
     Similarity     Age / Gender     Distance
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                  Ranking Engine
                         │
                         ▼
              Top Potential Matches
                         │
                         ▼
              Investigation Agent
                         │
                         ▼
             Explainable AI Report
                         │
                         ▼
                Human Verification
```

---

## 🔬 Matching System

FindTrace uses multiple signals instead of depending entirely on facial similarity.

### 1. Facial Similarity

The system uses **InsightFace with ArcFace-based face embeddings**.

The process is:

```text
Image
  ↓
Face Detection
  ↓
Face Alignment
  ↓
ArcFace Embedding
  ↓
Vector Similarity Search
  ↓
Potential Candidates
```

The generated embeddings are searched using **FAISS** to efficiently retrieve visually similar candidate faces.

---

### 2. Description Similarity

Physical descriptions and investigator notes can contain useful information that cannot be obtained from an image alone.

FindTrace uses **Sentence-BERT (`all-MiniLM-L6-v2`)** to compare descriptions semantically.

For example:

```text
Missing person:
"Young man wearing a black jacket and blue jeans."

Candidate:
"Male wearing dark clothing with denim trousers."
```

The wording is different, but the semantic meaning is similar.

---

### 3. Age & Gender Matching

The ranking system considers the available demographic information.

Age is scored according to the difference between the reported age and candidate age, while gender information is matched when available.

Missing or unknown information does not automatically eliminate a candidate.

---

### 4. Geographic Location Matching

Location can provide important contextual evidence.

FindTrace supports geographic comparison using:

* Human-readable locations
* Geocoding
* Latitude / longitude
* Haversine geographic distance

The system can therefore distinguish between candidates who were found close to the missing person's last known location and those located much farther away.

---

## 📊 Candidate Ranking

Candidates are ranked using a weighted scoring system.

Current scoring structure:

| Evidence               | Weight |
| ---------------------- | -----: |
| Facial similarity      |    60% |
| Description similarity |    10% |
| Age / Gender metadata  |    15% |
| Geographic location    |    15% |

The final score is calculated from the available evidence and displayed to the investigator together with the individual evidence scores.

For example:

```text
Overall Score: 73.13%

Facial Similarity       100%
Description Similarity    0%
Metadata Consistency     87.5%
Location Consistency      0%
```

The score is intended to **prioritize candidates for investigation**, not to establish identity.

---

## 🤖 Investigation Agent

FindTrace includes an AI-assisted investigation layer powered by an LLM.

The investigation agent receives structured evidence from the matching system and helps produce an investigation report containing:

* Strongest potential candidate
* Supporting evidence
* Conflicting evidence
* Relevant observations
* Recommended verification steps
* Investigation summary

The AI does not make the final identity decision.

Every result is presented as a:

> **Potential Match — Human Verification Required**

---

## 🖥️ Application Interface

FindTrace is built as a Streamlit application with dedicated sections for:

### Dashboard

Provides an overview of cases and investigation activity.

### New Case

Allows an investigator to create a missing-person case and upload the available photograph and information.

### Candidate Records

Allows authorized users to create and manage unidentified-person candidate records and their associated information.

### Investigation Results

Displays ranked potential matches with:

* Candidate photograph
* Overall score
* Facial similarity
* Description similarity
* Metadata consistency
* Location consistency
* Evidence indicators

Investigators can open a candidate profile to review additional information before verification.

### About

Provides information about the system, AI pipeline, and responsible-use considerations.

---

## 🛠️ Technology Stack

### Frontend / Interface

* Python
* Streamlit

### Computer Vision

* InsightFace
* ArcFace
* Face embeddings

### Vector Search

* FAISS

### Natural Language Processing

* Sentence Transformers
* `all-MiniLM-L6-v2`

### AI Investigation

* Groq API
* `openai/gpt-oss-120b`

### Backend / Storage

* SQLite
* SQLAlchemy
* Pandas

### Geospatial Analysis

* Google Maps Geocoding API
* Haversine distance calculation

---

## 📁 Project Structure

```text
FindTrace/
│
├── app.py
├── requirements.txt
├── runtime.txt
├── README.md
├── .gitignore
│
├── agents/
│   ├── investigation_agent.py
│   └── prompts.py
│
├── database/
│   └── store.py
│
├── matching/
│   ├── ranking.py
│   ├── metadata.py
│   └── location.py
│
├── nlp/
│   └── text_engine.py
│
├── vision/
│   ├── face_engine.py
│   └── embeddings.py
│
├── utils/
│
├── data/
│
├── case_uploads/
│
└── .streamlit/
    └── secrets.toml
```

---

## 🔐 Privacy & Responsible Use

FindTrace is designed for authorized investigative use.

Because facial recognition and missing-person identification involve highly sensitive information, the system should be used responsibly.

### Important safeguards

* AI results are not identity confirmations.
* Human verification is required.
* Candidate rankings should be treated as investigative leads.
* Personal information should only be accessed by authorized personnel.
* API keys and secrets must never be committed to GitHub.
* Real missing-person data should only be used with appropriate authorization.
* Publicly available images should not be automatically scraped and used without considering licensing, privacy, and legal requirements.

---

## ⚙️ Local Installation

Clone the repository:

```bash
git clone https://github.com/Junaid5253/FindTrace.git
cd FindTrace
```

Create and activate a virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the application:

```powershell
streamlit run app.py
```

---

## 🔑 API Configuration

FindTrace can use external APIs through environment variables or Streamlit secrets.

For local development, create:

```text
.streamlit/
└── secrets.toml
```

Example:

```toml
GROQ_API_KEY = "your_groq_api_key"
GOOGLE_MAPS_API_KEY = "your_google_maps_api_key"
```

Never commit `secrets.toml` to GitHub.

The actual API keys should be configured separately when deploying the application.

---

## ☁️ Deployment

The application is designed with **Streamlit deployment** in mind.

Before deployment:

1. Push the project to GitHub.
2. Connect the repository to Streamlit.
3. Configure required secrets in the deployment settings.
4. Install dependencies from `requirements.txt`.
5. Launch the Streamlit application.

Heavy pretrained models may require additional deployment considerations depending on the hosting environment.

---

## 📈 Evaluation

Potential evaluation metrics for the matching system include:

* Top-1 retrieval accuracy
* Top-5 retrieval accuracy
* Top-10 retrieval accuracy
* Face similarity performance
* Ranking quality
* Average candidate search time

A properly labeled evaluation dataset should be used before making claims about real-world identification performance.

---

## 🔮 Future Improvements

Possible future development includes:

* Interactive geographic maps
* Multiple photographs per case
* Multilingual descriptions
* Urdu language support
* Improved candidate filtering
* More advanced semantic matching
* Better investigation-agent workflows
* Role-based access control
* PostgreSQL support
* Larger-scale vector databases
* Case timeline visualization
* Evidence history and audit logs
* Improved evaluation and calibration of ranking scores

---

## 👨‍💻 Project

**FindTrace — AI Missing Person Identification & Investigation System**

Built as a Generative AI / Agentic AI project exploring the combination of:

**Computer Vision + NLP + Vector Search + Geospatial Analysis + Agentic AI**

GitHub:

**https://github.com/Junaid5253/FindTrace**

---

## ⚠️ Disclaimer

FindTrace is an experimental AI-assisted investigation system developed for research, learning, and hackathon purposes.

It should not be used as the sole basis for identifying a person or making law-enforcement decisions.

All potential matches require appropriate human review and verification.
