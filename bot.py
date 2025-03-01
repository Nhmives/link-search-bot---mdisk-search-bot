import os
import sqlite3
from pyrogram import Client, filters

# Load bot credentials from environment variables
API_ID = int(os.getenv("20496814"))
API_HASH = os.getenv("a87c1094edd18650e5dfee0f2bc78bda")
BOT_TOKEN = os.getenv("8157106185:AAFclqf84nHsscIbD8R2V3Xi8w8FkDiObaA")

# List of channels to monitor (Replace with your actual channel IDs)
CHANNELS = [-1002325240013, -1002321506152]

# Initialize bot
bot = Client("movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# SQLite Database setup
conn = sqlite3.connect("movies.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS movies (title TEXT, link TEXT)")
conn.commit()

# Function to store new movie uploads
@bot.on_message(filters.channel)
async def store_movie(client, message):
    if message.document and message.document.file_name:
        title = message.document.file_name.lower()
        link = message.link if message.link else "No link available"

        # Avoid duplicate entries
        cursor.execute("SELECT * FROM movies WHERE title = ?", (title,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO movies VALUES (?, ?)", (title, link))
            conn.commit()
            print(f"Added: {title}")

# Command to search movies
@bot.on_message(filters.private & filters.text)
async def search_movie(client, message):
    query = message.text.lower()
    cursor.execute("SELECT title, link FROM movies WHERE title LIKE ?", ('%' + query + '%',))
    results = cursor.fetchall()

    if results:
        response = "\n".join([f"🎬 **{title}**\n👉 [Download]({link})" for title, link in results])
    else:
        response = "❌ No results found. Try another name."

    await message.reply_text(response, disable_web_page_preview=True)

# Start bot
bot.run()
