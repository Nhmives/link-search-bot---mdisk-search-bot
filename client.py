# Don't Remove Credit Tg - @new_updet
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @insightweav

from info import *
from pyrogram import Client

class Bot(Client):   
    def __init__(self):
        super().__init__(   
           "link-search-bot---mdisk-search-bot",
            api_id=API_ID,
            api_hash=API_HASH,           
            bot_token=BOT_TOKEN,
            plugins={"root": "plugins"})
    async def start(self):                        
        await super().start()  
        print("Bot Started 🔧 Powered By @new_updet")   
    async def stop(self, *args):
        await super().stop()
