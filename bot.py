import sqlite3
from pyrogram import Client, filters

# Telegram API credentials
API_ID = "20496814"
API_HASH = "a87c1094edd18650e5dfee0f2bc78bda"
BOT_TOKEN = "8157106185:AAFclqf84nHsscIbD8R2V3Xi8w8FkDiObaA"

# List of channels to search
CHANNELS = [-1002325240013, -1002321506152]  # Replace with your channel IDs

# Initialize bot
bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("user", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# SQLite Database setup
conn = sqlite3.connect("movies.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS movies (title TEXT, link TEXT)")
conn.commit()

# Function to fetch movie links
async def fetch_movies():
    async with user:
        for channel in CHANNELS:
            async for message in user.get_chat_history(channel):
                if message.document:
                    title = message.document.file_name
                    link = message.link
                    cursor.execute("INSERT INTO movies VALUES (?, ?)", (title, link))
                    conn.commit()

# Command to search movies
@bot.on_message(filters.private & filters.text)
async def search_movie(client, message):
    query = message.text.lower()
    cursor.execute("SELECT title, link FROM movies WHERE title LIKE ?", ('%' + query + '%',))
    results = cursor.fetchall()

    if results:
        response = "\n".join([f"{title}\n👉 [Download]({link})" for title, link in results])
    else:
        response = "No results found."

    await message.reply_text(response, disable_web_page_preview=True)

# Start bot
async def main():
    await fetch_movies()  # Fetch latest movie links
    bot.run()

bot.start()
user.run()
