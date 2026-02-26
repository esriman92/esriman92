import urllib.request
import json
import re

def fetch_hacker_news():
    # Fetch the top 500 story IDs
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        story_ids = json.loads(response.read().decode())

    # Fetch the titles of the top 3 stories
    headlines = []
    for story_id in story_ids[:3]:
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        with urllib.request.urlopen(story_url) as story_response:
            story = json.loads(story_response.read().decode())
            headlines.append(story.get('title', ''))
    
    # Format into a single scrolling string
    return " • ".join(headlines) + " • "

def update_svg(news_text):
    file_path = 'breaking-news.svg'
    
    # Read the current SVG
    with open(file_path, 'r', encoding='utf-8') as file:
        svg_content = file.read()

    # Use Regex to find and replace the text inside our ticker text tag
    # We look for the specific class we assigned to the scrolling text
    pattern = r'(<text y="25" class="base-text ticker-opposite">\s*)(.*?)(\s*</text>)'
    
    # Replace the old hardcoded text with our live news_text
    updated_svg = re.sub(pattern, rf'\1{news_text}\3', svg_content, flags=re.DOTALL)

    # Write the updated content back to the SVG
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_svg)
    print("Successfully injected live news into SVG.")

if __name__ == "__main__":
    live_news = fetch_hacker_news()
    update_svg(live_news)
