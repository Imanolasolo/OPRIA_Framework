import sqlite3
import json
from datetime import datetime


DB_NAME = "opria.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


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