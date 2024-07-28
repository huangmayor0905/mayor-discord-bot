import discord
import random as rd
from discord.ext import commands
from core.classes import Cog_Extension
from discord import app_commands
import json

with open("config.json", "r", encoding="utf8") as jfile:
    jdata = json.load(jfile)

admin = int(jdata["roles"]["admin"])


class Main(Cog_Extension):
    # Cog 的寫法：
    # @bot.command() -> @commands.command()
    # bot -> self.bot

    # ping
    @commands.command()
    @commands.has_role(admin)
    async def ping(self, ctx):
        await ctx.send(f"The Bot Latency: `{round(self.bot.latency * 1000)}ms`")

    # say hi
    @commands.command()
    async def hi(self, ctx):
        await ctx.send("hi there!")

    # bot say
    @commands.command()
    @commands.has_role(admin)
    async def say(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)

    # bot say in specific channel
    @commands.command()
    @commands.has_role(admin)
    async def say_in(self, ctx, channel: discord.TextChannel, *, msg):
        await ctx.message.delete()
        await channel.send(msg)

    # clear message
    @commands.command()
    @commands.has_role(admin)
    async def clean(self, ctx, num: int):
        await ctx.channel.purge(limit=num + 1)

    # name指令顯示名稱，description指令顯示敘述
    # name的名稱，中、英文皆可，但不能使用大寫英文
    @commands.command()
    async def hello(self, ctx):
        # 回覆使用者的訊息
        await ctx.send("Hello, world!")

    # 特戰隨機地圖
    @commands.command(name="特戰隨機地圖", description="特戰隨機地圖")
    async def random_valorant_map(self, ctx):
        # 回覆使用者的訊息
        await ctx.send("抽到的地圖是：" + rd.choice(jdata["valorant"]["map"]))

    # 特戰隨機角色
    @commands.command(name="特戰隨機角色", description="特戰隨機角色")
    async def random_valorant_agent(self, ctx):
        # 回覆使用者的訊息
        await ctx.send("抽到的角色是：" + rd.choice(jdata["valorant"]["agent"]))

    # 老師說
    @commands.command(name="老師說", description="老師說")
    async def teacher_says(self, ctx):
        # 回覆使用者的訊息
        await ctx.message.delete()
        await ctx.send(rd.choice(jdata["teacher_says"]))


async def setup(bot):
    await bot.add_cog(Main(bot))
