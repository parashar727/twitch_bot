from config import OSU_CLIENT_ID, OSU_CLIENT_SECRET, OSU_CALLBACK_URL, OSU_IRC_PASSWORD, OSU_IRC_NICK
import osu_irc
from ossapi import Ossapi, UserLookupKey, Scope
import asyncio

scopes = [Scope.PUBLIC, Scope.CHAT_WRITE]

api = Ossapi(OSU_CLIENT_ID, OSU_CLIENT_SECRET, OSU_CALLBACK_URL, scopes=scopes)
# osuirc = osu_irc.Client(token=OSU_IRC_PASSWORD, nickname=OSU_IRC_NICK)

# async def sendMessage(content="Hello Hasco"):
#     await osuirc.sendPM(Us=OSU_IRC_NICK, content=content)

def getBotUserID():
    user = api.user("Mikuia")
    print(user.id)

async def sendMessage(content):
    await api.send_pm(6566547, content)

if __name__ == "__main__":
    getBotUserID()