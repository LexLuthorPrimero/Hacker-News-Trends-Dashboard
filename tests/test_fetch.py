import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fetch import fetch_top_stories, update_data

def test_fetch_top_stories():
    stories = fetch_top_stories(limit=5)
    assert len(stories) > 0
    assert 'title' in stories[0]
    assert 'score' in stories[0]

def test_update_data():
    count = update_data()
    assert count > 0
