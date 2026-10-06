import os
import sqlite3
import json
from datetime import datetime


def get_secret(key, default=""):
    try:
        import streamlit as st

        return st.secrets.get(key, default)
    except Exception:
        return default


DB_NAME = get_secret("OPRIA_DB_PATH", os.getenv("OPRIA_DB_PATH", "opria.db"))


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def get_database_path():
    return os.path.abspath(DB_NAME)


def get_database_info():
    path = get_database_path()
    exists = os.path.exists(path)

    info = {
        "path": path,
        "exists": exists,
        "size_bytes": os.path.getsize(path) if exists else 0,
        "modified_at": datetime.fromtimestamp(os.path.getmtime(path)).isoformat() if exists else None,
    }

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
    )
    table_names = [row["name"] for row in cursor.fetchall()]

    tables = []
    for table_name in table_names:
        cursor.execute(f"SELECT COUNT(*) AS count FROM {table_name}")
        count = cursor.fetchone()["count"]

        cursor.execute(
            f"""
            SELECT *
            FROM {table_name}
            ORDER BY id DESC
            LIMIT 1
            """
        )
        latest_row = cursor.fetchone()

        tables.append(
            {
                "name": table_name,
                "count": count,
                "latest_row": dict(latest_row) if latest_row else None,
            }
        )

    conn.close()

    info["tables"] = tables
    return info


def fetch_recent_rows(table_name, limit=25):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT *
        FROM {table_name}
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT,
            email TEXT NOT NULL,
            message TEXT,
            language TEXT,
            source TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS business_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            company TEXT,
            email TEXT,
            score INTEGER,
            answers TEXT,
            language TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


def save_contact(
    name,
    company,
    email,
    message,
    language,
    source,
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO contacts (
            name,
            company,
            email,
            message,
            language,
            source,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            company,
            email,
            message,
            language,
            source,
            datetime.utcnow().isoformat(),
        ),
    )

    conn.commit()
    conn.close()


def save_business_check(
    name,
    company,
    email,
    score,
    answers,
    language,
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO business_checks (
            name,
            company,
            email,
            score,
            answers,
            language,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            company,
            email,
            score,
            json.dumps(answers),
            language,
            datetime.utcnow().isoformat(),
        ),
    )

    conn.commit()
    conn.close()


def fetch_recent_contacts(limit=25):
    return fetch_recent_rows("contacts", limit=limit)


def fetch_recent_business_checks(limit=25):
    return fetch_recent_rows("business_checks", limit=limit)