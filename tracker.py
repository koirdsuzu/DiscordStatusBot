import discord
from discord.ext import tasks
import config

class StatusTracker(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)
        self.target_user_id = config.USER_ID
        self.last_status = None

    async def on_ready(self):
        print(f'ログインしました: {self.user}')
        self.track_status.start()

    @tasks.loop(seconds=10)
    async def track_status(self):
        guild = self.get_guild(config.GUILD_ID)
        if not guild:
            print("サーバーが見つかりません。")
            return

        user = guild.get_member(self.target_user_id)
        if not user:
            print("ユーザーが見つかりません。")
            return

        if user.status != self.last_status:
            print(f"ユーザーの状態が変更されました: {user.status}")
            self.last_status = user.status
            if user.status == discord.Status.offline:
                await self.notify_online(guild)

    async def notify_online(self, guild):
        # ユーザーがオフラインになったら通知
        channel = discord.utils.get(guild.text_channels, name="general")
        if channel:
            await channel.send(f"<@{self.target_user_id}> さんがオフラインになりました！")

