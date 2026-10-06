from config import OSU_CLIENT_ID, OSU_CLIENT_SECRET, OSU_CALLBACK_URL, OSU_IRC_PASSWORD, OSU_IRC_NICK, OSU_BOT_CLIENT_ID, OSU_BOT_CLIENT_SECRET
import osu_irc
from ossapi import Ossapi, UserLookupKey, Scope, OssapiAsync
import asyncio

scopes = ["public", "chat.write"]

# api = OssapiAsync(OSU_CLIENT_ID, OSU_CLIENT_SECRET, OSU_CALLBACK_URL, scopes=scopes)
api = OssapiAsync(OSU_BOT_CLIENT_ID, OSU_BOT_CLIENT_SECRET, OSU_CALLBACK_URL, scopes=scopes)
# osuirc = osu_irc.Client(token=OSU_IRC_PASSWORD, nickname=OSU_IRC_NICK)

async def getBotUserID():
    user = await api.user("Hasco")
    print(user.id)

async def sendMessage(content):
    await api.send_pm(20076230, content)

if __name__ == "__main__":
    asyncio.run(getBotUserID())