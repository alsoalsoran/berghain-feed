import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Berghain program page
url = "https://www.berghain.berlin/en/program/"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

# List to hold event data
items = []

for event in soup.select("a.program-list__link"):
    title = event.select_one("div.program-list__event-title")
    date = event.select_one("div.program-list__event-date")
    link = "https://www.berghain.berlin" + event['href']

    if not title or not date:
        continue

    pubDate = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")

    items.append(f"""
    <item>
        <title>{title.text.strip()}</title>
        <link>{link}</link>
        <description>{date.text.strip()}</description>
        <pubDate>{pubDate}</pubDate>
    </item>
    """)

rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>Berghain Events</title>
    <link>{url}</link>
    <description>Upcoming events at Berghain</description>
    <lastBuildDate>{datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")}</lastBuildDate>
    {''.join(items)}
</channel>
</rss>
"""

# Write the new XML to berghain.xml
with open("berghain.xml", "w", encoding="utf-8") as f:
    f.write(rss)
