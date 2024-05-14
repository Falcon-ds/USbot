import discord
from discord.ext import commands
from discord import app_commands
import os
import dotenv
import asyncio

dotenv.load_dotenv()
token = os.getenv("token")
client=commands.Bot(command_prefix="!", intents=discord.Intents.all())
#Я хочу померти, бо дід мене не хоче їбате
MuteRoleId = 1239498371090087967
ServerId = 1233471689619144746
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Відсутні потрібні докази і довідки :rolling_eyes:.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("У ВАС НЕМАЄ ВОДІЙСЬКОГО ПОСВІЧЕННЯ! :angry:")
@client.event
async def on_ready():
    await client.tree.sync(guild=discord.Object(id=ServerId))
@client.tree.command(
    name="ban",
    description="ЗАБАНИТИ НАХУЙ",
    guild=discord.Object(id=ServerId)
              )
@commands.has_permissions(ban_members = True)
async def ban(ctx: discord.Interaction, member: discord.Member, *, reason: str):
    await member.ban(reason = reason)
    await ctx.response.send_message(f'Ви ЗАБАНЕЛИ учасника серверу')

@client.tree.command(
    name="mute",
    description="Замучити користувача",
    guild=discord.Object(id=ServerId)
)
@commands.has_permissions(administrator=True)
async def mute(ctx: discord.Interaction, member: discord.Member, time: int, unit: str, *, reason: str):
    if ctx.user.guild_permissions.mute_members:
        muted_role = discord.utils.get(ctx.guild.roles, id=MuteRoleId)

        await member.send(f'Ви були замучені на {time}{unit} за {reason}.')
        await member.add_roles(muted_role)
        await ctx.response.send_message(f'{member.mention} був замучений на {time}{unit}.')
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

@client.tree.command(
    name="unmute",
    description="Розмучити користувача",
    guild=discord.Object(id=ServerId)
)
async def unmute(ctx: discord.Interaction, member: discord.Member):
    if ctx.user.guild_permissions.mute_members:
        muted_role = discord.utils.get(ctx.guild.roles, id=MuteRoleId)
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.response.send_message(f'{member.mention} був розмучений.')
        else:
            await ctx.response.send_message(f'{member.mention} не замучений.')


client.run(token)
