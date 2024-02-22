from discord import member
from discord.utils import get
from discord.ext import commands
import requests
import discord
import asyncio
import tokens

client = commands.Bot(command_prefix="!")

participants = []
@client.event
async def on_ready():
    print('ready')


@client.command()
async def start10man(ctx):
    role_names = ("10man")
    roles = tuple(get(ctx.guild.roles, name=n) for n in role_names)
    for m in ctx.guild.members:
        try:
            await member.remove_roles(*roles)
        except:
            print(f"Couldn't remove roles from {m}")
    text = "Currently participating are:\n"
    for x in range(len(participants)):
        text = text + "\n" + participants[x]
    description = f" {ctx.message.author.mention} is trying to get a 10 man going. \n" \
                  f"to participate in the 10 man, press <:10man:955110124719075429> \n \n" \
                  f"{text}\n" \
                  f"\nto start a new 10 man type ```!start10man```"
    embed = discord.Embed(title="10 Man", description=description)
    message = await ctx.send("@everyone", embed=embed)
    await message.add_reaction('<:10man:955110124719075429>')
    while True:
        text = "Currently participating are:\n"
        for x in range(len(participants)):
            if "M4anuel's TestBot" not in participants[x]:
                text = text + "\n" + participants[x]
        description = f" {ctx.message.author.mention} is trying to get a 10 man going. \n" \
                      f"to participate in the 10 man, press <:10man:955110124719075429> \n \n" \
                      f"{text}\n" \
                      f"\nto start a new 10 man type ```!start10man```"
        embed = discord.Embed(title="10 Man", description=description)
        await asyncio.sleep(1)
        await message.edit(embed=embed)


@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == message_id:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = await(await client.fetch_guild(payload.guild_id)).fetch_member(payload.user_id)
            if member is not None:
                await member.add_roles(role)
            else:
                print("member not found")
            if member.name not in participants:
                participants.append(member.name)
                for x in range(len(participants)):
                    print(participants[x])
        else:
            print("role not found")


@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == message_id:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = await(await client.fetch_guild(payload.guild_id)).fetch_member(payload.user_id)
            if member is not None:
                await member.remove_roles(role)
            else:
                print("member not found")
            if member.name in participants:
                participants.remove(member.name)
                for x in range(len(participants)):
                    print(participants[x])
        else:
            print("role not found")


client.run(tokens.DISCORD_10MAN_BOT_KEY)
