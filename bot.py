import discord
from discord.ext import commands
import os
import dotenv
import asyncio
dotenv.load_dotenv()
token = os.getenv("token")
client=commands.Bot(command_prefix="!", intents=discord.Intents.all())
#Я хочу померти, бо дід
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Відсутні потрібні докази і довідки :rolling_eyes:.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("У ВАС НЕМАЄ ВОДІЙСЬКОГО ПОСВІЧЕННЯ! :angry:")

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason = None):
    await member.ban(reason = reason)

@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, time: int, unit = None, *, reason):
    if ctx.author.guild_permissions.manage_roles:
        muted_role = discord.utils.get(ctx.guild.roles, id=1239498371090087967)

        await member.add_roles(muted_role)
        await ctx.send(f'{member.mention} був замучений на {time}{unit}.')
        if unit == "s":
            wait = 1 * time
            await asyncio.sleep(wait)
        elif unit == "m":
            wait = 60 * time
            await asyncio.sleep(wait)
        elif unit == "h":
            wait = 3600 * time
            await asyncio.sleep(wait)
        elif unit == "d":
            wait = 3600 * 24 * time
            await asyncio.sleep(wait)
        await member.remove_roles(muted_role)
async def unmute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.manage_roles:
        muted_role = discord.utils.get(ctx.guild.roles, id=1239498371090087967)
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f'{member.mention} був розмучений.')
        else:
            await ctx.send(f'{member.mention} не замучений.')


client.run(token)
