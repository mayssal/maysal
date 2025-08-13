import argparse
import json
import os
from datetime import datetime
from typing import Dict, List

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from app.config import load_config


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS persons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    notes TEXT,
    face_embedding TEXT,
    voice_embedding TEXT,
    created_at TEXT,
    updated_at TEXT
);
"""


class DatabaseClient:
    def __init__(self, database_url: str):
        self.engine: Engine = create_engine(database_url, future=True)

    def init_db(self):
        with self.engine.begin() as conn:
            conn.exec_driver_sql(SCHEMA_SQL)

    @staticmethod
    def _serialize_embedding(vec: List[float]) -> str:
        return ",".join(f"{x:.8f}" for x in vec)

    @staticmethod
    def _deserialize_embedding(txt: str) -> List[float]:
        if not txt:
            return []
        return [float(x) for x in txt.split(",") if x]

    def insert_person(
        self,
        full_name: str,
        email: str = None,
        phone: str = None,
        address: str = None,
        notes: str = None,
        face_embedding: List[float] = None,
        voice_embedding: List[float] = None,
    ) -> int:
        now = datetime.utcnow().isoformat()
        face_txt = self._serialize_embedding(face_embedding) if face_embedding else None
        voice_txt = self._serialize_embedding(voice_embedding) if voice_embedding else None
        with self.engine.begin() as conn:
            res = conn.execute(
                text(
                    """
                    INSERT INTO persons (full_name, email, phone, address, notes, face_embedding, voice_embedding, created_at, updated_at)
                    VALUES (:full_name, :email, :phone, :address, :notes, :face_embedding, :voice_embedding, :created_at, :updated_at)
                    """
                ),
                dict(
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    address=address,
                    notes=notes,
                    face_embedding=face_txt,
                    voice_embedding=voice_txt,
                    created_at=now,
                    updated_at=now,
                ),
            )
            last_id = res.lastrowid if hasattr(res, "lastrowid") else None
        return last_id or -1

    def fetch_candidates(self) -> List[Dict]:
        with self.engine.begin() as conn:
            res = conn.execute(text("SELECT id, full_name, email, phone, address, notes, face_embedding, voice_embedding FROM persons"))
            rows = res.fetchall()
        candidates: List[Dict] = []
        for r in rows:
            face_emb = self._deserialize_embedding(r[6]) if r[6] else []
            voice_emb = self._deserialize_embedding(r[7]) if r[7] else []
            meta = {
                "full_name": r[1],
                "email": r[2],
                "phone": r[3],
                "address": r[4],
                "notes": r[5],
            }
            candidates.append({
                "id": r[0],
                "full_name": r[1],
                "meta": meta,
                "face_embedding": face_emb,
                "voice_embedding": voice_emb,
            })
        return candidates


def main():
    parser = argparse.ArgumentParser(description="BioMatch DB util")
    parser.add_argument("--init-db", action="store_true", help="Créer le schéma de base")
    parser.add_argument("--config", type=str, default=None)
    args = parser.parse_args()

    config = load_config(args.config)
    db = DatabaseClient(config["database"]["url"])

    if args.init_db:
        db.init_db()
        print("Schéma initialisé.")


if __name__ == "__main__":
    main()