import json
import sqlite3
from datetime import datetime, timezone


def _connect(db_path):
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(db_path):
    with _connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                created_at TEXT NOT NULL,
                average_people_count REAL NOT NULL,
                peak_people_count INTEGER NOT NULL,
                risk_level TEXT NOT NULL,
                duration_seconds REAL NOT NULL,
                timeline_json TEXT NOT NULL
            )
        """)


def save_analysis(db_path, filename, result):
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with _connect(db_path) as conn:
        cursor = conn.execute("""
            INSERT INTO analyses (
                filename, created_at, average_people_count,
                peak_people_count, risk_level, duration_seconds, timeline_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            filename,
            created_at,
            result["average_people_count"],
            result["peak_people_count"],
            result["risk_level"],
            result["duration_seconds"],
            json.dumps(result["timeline"])
        ))
        return cursor.lastrowid


def get_recent_analyses(db_path, limit=20):
    with _connect(db_path) as conn:
        rows = conn.execute("""
            SELECT id, filename, created_at, average_people_count,
                   peak_people_count, risk_level, duration_seconds
            FROM analyses
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()
    return [dict(row) for row in rows]
