import asyncio
import json
import logging
import random
from typing import Any

import twitchio
from twitchio import authentication, eventsub
from twitchio.ext import commands

from config import TWITCH_CLIENT_ID, TWITCH_CLIENT_SECRET, TWITCH_BOT_ID, TWITCH_USER_ID


CLIENT_ID = TWITCH_CLIENT_ID
CLIENT_SECRET = TWITCH_CLIENT_SECRET
BOT_ID = TWITCH_BOT_ID
OWNER_ID = TWITCH_USER_ID

LOGGER: logging.Logger = logging.getLogger(__name__)


class Bot(commands.AutoBot):
    def __init__(self, subs: list[eventsub.SubscriptionPayload]) -> None:
        super().__init__(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            bot_id=BOT_ID,
            owner_id=OWNER_ID,
            prefix="!",
            subscriptions=subs,
            force_subscribe=True,
        )

    async def setup_hook(self) -> None:
        # Add the osu component
        await self.add_component(OsuComponent())

    async def event_ready(self) -> None:
        LOGGER.info("Logged in as: %s", self.user)

    async def event_oauth_authorized(self, payload: authentication.UserTokenPayload) -> None:
        # Stores tokens in .tio.tokens.json by default; can be overriden to use a DB for example
        # Adds the token to our Client to make requests and subscribe to EventSub...
        await self.add_token(payload.access_token, payload.refresh_token)

        if not payload.user_id:
            return

        if payload.user_id == self.bot_id:
            return

        subs: list[eventsub.SubscriptionPayload] = [
            eventsub.ChatMessageSubscription(broadcaster_user_id=payload.user_id, user_id=self.bot_id)
        ]

        resp: twitchio.MultiSubscribePayload = await self.multi_subscribe(subs)
        if resp.errors:
            LOGGER.warning("Failed to subscribe to: %r, for user: %s", resp.errors, payload.user_id)


class OsuComponent(commands.Component):
    @commands.command()
    async def hi(self, ctx: commands.Context[Bot]) -> None:
        """Command that replies to the invoker with Hi <name>!

        !hi
        """
        await ctx.reply(f"Hi {ctx.chatter}!")



def main() -> None:
    twitchio.utils.setup_logging(level=logging.INFO)

    subs: list[eventsub.SubscriptionPayload] = []

    with open(".tio.tokens.json", "rb") as fp:
        tokens = json.load(fp)
        for user_id in tokens:
            if user_id == BOT_ID:
                continue
            
            subs.extend(
                [
                    eventsub.ChatMessageSubscription(broadcaster_user_id=user_id, user_id=BOT_ID)
                ]
            )

    async def runner() -> None:
        async with Bot(subs=subs) as bot:
            await bot.start()

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        LOGGER.warning("Shutting down due to KeyboardInterrupt")


if __name__ == "__main__":
    main()