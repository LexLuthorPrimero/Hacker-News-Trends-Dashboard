import requests
import time
from database import insert_stories, init_db

def fetch_top_stories(limit=50):
    top_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    ids = requests.get(top_url).json()[:limit]
    stories = []
    for story_id in ids:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story_data = requests.get(story_url).json()
        if story_data and "title" in story_data:
            stories.append({
                "id": story_data["id"],
                "title": story_data.get("title", ""),
                "score": story_data.get("score", 0),
                "time": story_data.get("time", 0),
                "url": story_data.get("url", ""),
                "by": story_data.get("by", ""),
                "descendants": story_data.get("descendants", 0)
            })
        time.sleep(0.2)
    return stories

def update_data():
    init_db()
    stories = fetch_top_stories(limit=100)
    insert_stories(stories)
    print(f"Actualizadas {len(stories)} stories")
    return len(stories)

if __name__ == "__main__":
    update_data()
