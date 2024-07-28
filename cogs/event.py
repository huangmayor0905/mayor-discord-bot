from core.classes import Cog_Extension
from discord.ext import commands
import datetime
import discord
import json

with open("config.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)

# 冷卻時間紀錄
last_used = {}


class Event(Cog_Extension):
    # Cog 的寫法：
    # @bot.command() -> @commands.command()
    # bot -> self.bot

    # welcome guild
    @commands.Cog.listener()
    async def on_member_join(self, member):
        wel_channel = self.bot.get_channel(int(jdata["guild"]["welcome_channel"]))
        await wel_channel.send(f"歡迎 {member.mention} 加入！")

    # leave guild
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        leave_channel = self.bot.get_channel(int(jdata["guild"]["leave_channel"]))
        await leave_channel.send(f"{member.mention} 滾遠點")

    # listen message
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        # 如果是影片或圖片，不做任何事
        if before.content == after.content:
            return
        await monitor.send(
            f'{before.author} 將 "{before.content}" 修改成 "{after.content}"'
        )

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        await monitor.send(f'{msg.author} 刪除了 "{msg.content}"')

    # listen voice channel
    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        # 如果是關閉或開啟麥克風或
        # 關閉或開啟音效或
        # 開始或停止共享螢幕
        # 開啟或關閉視訊
        if (
            before.self_mute != after.self_mute
            or before.self_deaf != after.self_deaf
            or before.self_stream != after.self_stream
            or before.self_video != after.self_video
        ):
            return

        if before.channel is None and after.channel is not None:
            print(f"{member} join {after.channel}")
            await monitor.send(f"{member} 加入了 {after.channel}")
        elif before.channel is not None and after.channel is None:
            print(f"{member} leave {before.channel}")
            await monitor.send(f"{member} 離開了 {before.channel}")
        else:
            print(f"{member} move from {before.channel} to {after.channel}")
            await monitor.send(f"{member} 從 {before.channel} 移到 {after.channel}")
        # 檢查離開的頻道是否為專屬語音頻道，並且現在是空的
        if (
            before.channel
            and before.channel.members == []
            and before.channel.name.endswith("的頻道")
        ):
            await before.channel.delete()
            print(f"Deleted empty custom channel: {before.channel.name}")
            await monitor.send(f"刪除了空的頻道：{before.channel.name}")

        # 檢查是否加入了設定的動態語音頻道
        if after.channel and after.channel.id == int(jdata["guild"]["dynamic_channel"]):
            # 創建一個新的語音頻道，名稱為使用者名稱的頻道
            new_channel = await after.channel.guild.create_voice_channel(
                name=f"【{member.display_name}】的頻道",
                category=after.channel.category,
                rtc_region=after.channel.rtc_region,
            )
            # 將使用者移動到新創建的語音頻道
            await member.move_to(new_channel)
            print(
                f"Created and moved {member} to their own channel: {new_channel.name}"
            )
            await monitor.send(f"創建並移動 {member} 到自己的頻道：{new_channel.name}")

    # QQ TT
    @commands.Cog.listener()
    async def on_message(self, msg):
        # 防止機器人自己觸發
        if msg.author == self.bot.user:
            return

        # 防洗頻
        user_id = msg.author.id
        now = datetime.datetime.utcnow()

        # 如果使用者不在字典中，則新增使用者，並設定上次使用時間為 1 分鐘前
        if user_id not in last_used:
            last_used[user_id] = now - datetime.timedelta(minutes=1)

        # 計算時間差
        time_since_last_message = now - last_used[user_id]

        # 如果時間差小於 15 秒，則回覆訊息
        if time_since_last_message < datetime.timedelta(seconds=10):
            await msg.channel.send("請過", ephemeral=True)
            return
        else:
            last_used[user_id] = now

        # 訊息偵測
        if msg.content == "qq" or msg.content == "QQ":
            await msg.channel.send("幫 QQ")
        if msg.content == "tt" or msg.content == "TT":
            await msg.channel.send("幫 TT")
        if (
            msg.content == "ff"
            or msg.content == "FF"
            or msg.content == "gg"
            or msg.content == "GG"
        ):
            await msg.channel.send("gg")
            await msg.channel.send("go next")
            await msg.channel.send("noob")
            await msg.channel.send("ez")
            await msg.channel.send("gg")
            await msg.channel.send(
                "──────▄▌▐▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▌\n───▄▄██▌█ BEEP BEEP\n▄▄▄▌▐██▌█ -22 RR DELIVERY\n███████▌█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▌\n▀(⊙)▀▀▀▀▀▀▀▀▀▀▀▀▀▀(⊙)(⊙)▀▀"
            )
            await msg.channel.send(
                "▒▒▒▒▒▒▒▒▒▄▄▄▒▒▒▒▒▒▒▒▒▒\n▒▒▒▒▒▒▒▒█▒▒▒█▒▒▒▒▒▒▒▒▒\n▒▒▒▒▒▒▒▒█▒▒▒█▒▒▒▒▒▒▒▒▒\n▒▒▒▒▒▒▒▒█▒▒▒█▒▒▒▒▒▒▒▒▒\n▒▒▒▒▒▒▒▒█▒▒▒█▒▒▒▒▒▒▒▒▒\n▒▒▒▒▒▒▒▒█▒▒▒█▒▒▒▒▒▒▒▒▒\n▒▒▒▒▄▄▄▄█▒▒▒█▄▄▄▄▒▒▒▒▒\n▒▒▒█▒▒▒▒█▄▄▄█▒▒▒▒█▒▒▒▒\n▒▒▒█▒▒▒▒█▒▒▒█▒▒▒▒█▒▒▒▒\n▒▒▒▒▀▀▀▀▒▒▒▒▒▀▀▀▀▒▒▒▒▒"
            )


async def setup(bot):
    await bot.add_cog(Event(bot))
