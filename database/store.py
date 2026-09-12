import json
import sqlite3
import numpy as np
from pathlib import Path

class CandidateStore:
    def __init__(self, db_path):
        self.db_path = str(db_path)
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._init()

    def _init(self):
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, age INTEGER, gender TEXT, location TEXT,
            description TEXT, image_path TEXT, embedding TEXT
        );
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, age INTEGER, gender TEXT, location TEXT,
            date_missing TEXT, description TEXT, status TEXT DEFAULT 'Open'
        );
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id INTEGER, candidate_id INTEGER, overall_score REAL,
            face_score REAL, text_score REAL, metadata_score REAL, location_score REAL
        );
        """)
        self.conn.commit()

    def count(self):
        return self.conn.execute("SELECT COUNT(*) FROM candidates").fetchone()[0]

    def count_cases(self, status=None):
        if status:
            return self.conn.execute("SELECT COUNT(*) FROM cases WHERE status=?", (status,)).fetchone()[0]
        return self.conn.execute("SELECT COUNT(*) FROM cases").fetchone()[0]

    def next_candidate_id(self):
        return self.count() + 1

    def add_candidate(self, name, age, gender, location, description, image_path, embedding):
        self.conn.execute("INSERT INTO candidates(name,age,gender,location,description,image_path,embedding) VALUES(?,?,?,?,?,?,?)",
                          (name, age, gender, location, description, image_path, json.dumps(np.asarray(embedding).tolist())))
        self.conn.commit()

    def list_candidates(self):
        rows = self.conn.execute("SELECT id,name,age,gender,location,description,image_path FROM candidates ORDER BY id DESC").fetchall()
        cols = ["id","name","age","gender","location","description","image_path"]
        return [dict(zip(cols, r)) for r in rows]

    def get_candidates_with_embeddings(self):
        rows = self.conn.execute("SELECT id,name,age,gender,location,description,image_path,embedding FROM candidates").fetchall()
        cols = ["id","name","age","gender","location","description","image_path","embedding"]
        out = []
        for r in rows:
            d = dict(zip(cols, r))
            d["embedding"] = np.asarray(json.loads(d["embedding"]), dtype=np.float32)
            out.append(d)
        return out

    def create_case(self, name, age, gender, location, date_missing, description):
        cur = self.conn.execute("INSERT INTO cases(name,age,gender,location,date_missing,description) VALUES(?,?,?,?,?,?)",
                                (name, age, gender, location, date_missing, description))
        self.conn.commit()
        return cur.lastrowid

    def save_results(self, case_id, ranked):
        self.conn.execute("DELETE FROM results WHERE case_id=?", (case_id,))
        for r in ranked:
            self.conn.execute("INSERT INTO results(case_id,candidate_id,overall_score,face_score,text_score,metadata_score,location_score) VALUES(?,?,?,?,?,?,?)",
                              (case_id, r["id"], r["overall_score"], r["face_score"], r["text_score"], r["metadata_score"], r["location_score"]))
        self.conn.commit()

    def list_cases(self):
        rows = self.conn.execute("SELECT id,name,age,gender,location,date_missing,status FROM cases ORDER BY id DESC").fetchall()
        cols = ["id","name","age","gender","location","date_missing","status"]
        return [dict(zip(cols, r)) for r in rows]
