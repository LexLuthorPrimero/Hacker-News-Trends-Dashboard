import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = "data/hn.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY,
            title TEXT,
            score INTEGER,
            time INTEGER,
            url TEXT,
            author TEXT,
            descendants INTEGER,
            fetched_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_stories(stories):
    conn = sqlite3.connect(DB_PATH)
    for story in stories:
        conn.execute('''
            INSERT OR REPLACE INTO stories (id, title, score, time, url, author, descendants, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (story['id'], story['title'], story['score'], story['time'],
              story.get('url', ''), story.get('by', ''), story.get('descendants', 0),
              datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_all_stories():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM stories ORDER BY fetched_at DESC", conn)
    conn.close()
    return df

def get_latest_fetch_time():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT MAX(fetched_at) FROM stories")
    row = c.fetchone()
    conn.close()
    return row[0] if row[0] else None
