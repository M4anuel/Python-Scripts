import discord
from discord.ext import commands
from discord import Button, ButtonStyle, SelectOption, SelectMenu
import tokens

client = commands.Bot(command_prefix=commands.when_mentioned_or('!'))


@client.command()
async def select(ctx):
    msg_with_selects = await ctx.send('Click to Select SkinportBot Options', components=[
        [
            SelectMenu(custom_id='_select_it', options=[
                SelectOption(emoji='🆖', label='ignore nothing', value='1',
                             description='Check this to start the bot'),
                SelectOption(emoji='1️⃣', label='Ignore Case Hardened', value='2',
                             description='Check this to ignore Case Hardened'),
                SelectOption(emoji='2️⃣', label='Ignore Dopplers', value='3',
                             description='Check this to ignore Dopplers')],
                       placeholder='Select Skinport-Bot Startoptions', max_values=2)
        ]])

    def check_selection(i: discord.Interaction, select_menu):
        return i.author == ctx.author and i.message == msg_with_selects

    while True:
        interaction, select_menu = await client.wait_for('selection_select', check=check_selection)
        options = [{o} for o in select_menu.values]
        ignore_ch = False
        ignore_dopppler = False
        for i in options:
            if i == {2}:
                ignore_ch = True
            if i == {3}:
                ignore_dopppler = True
        print(ignore_ch, ignore_dopppler)

        embed = discord.Embed(title='currently being processed',
                              color=discord.Color.random())

        await interaction.respond(embed=embed, delete_after=2)


@client.command()
async def buttons(ctx):
    msg_with_buttons = await ctx.send('Hey here are some Buttons', components=[[
        Button(label="Hey i\'m a red Button",
               custom_id="red",
               style=ButtonStyle.red),
        Button(label="Hey i\'m a green Button",
               custom_id="green",
               style=ButtonStyle.green),
        Button(label="Hey i\'m a blue Button",
               custom_id="blue",
               style=ButtonStyle.blurple),
        Button(label="Hey i\'m a grey Button",
               custom_id="grey",
               style=ButtonStyle.grey)
    ]])

    def check_button(i: discord.Interaction, button):
        return i.author == ctx.author and i.message == msg_with_buttons

    while True:
        interaction, button = await client.wait_for('button_click', check=check_button)
        embed = discord.Embed(title='You pressed an Button', description=f'You pressed a {button.custom_id} button.',
                              color=discord.Color.random())
        await interaction.respond(embed=embed)


client.run(tokens.DISCORD_CSFLOAT_BASE_BOT_KEY)
