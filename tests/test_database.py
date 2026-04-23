import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import sqlite3
from database import init_db, insert_stories, get_all_stories, get_latest_fetch_time
from fetch import fetch_top_stories

def test_init_db():
    init_db()
    conn = sqlite3.connect("data/hn.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stories'")
    assert cursor.fetchone() is not None
    conn.close()

def test_insert_and_retrieve():
    init_db()
    stories = fetch_top_stories(limit=2)
    insert_stories(stories)
    df = get_all_stories()
    assert len(df) >= len(stories)
    assert get_latest_fetch_time() is not None
