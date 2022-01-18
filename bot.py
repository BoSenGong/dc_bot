import os
import json
import discord
from discord.ext import commands

with open('setting.json','r',encoding='utf8') as jfile:
    setting=json.load(jfile)

### bot setting and permission grant ###
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

### load other modules in cmds directory ###
os.chdir(r'C:\discord_bot\whitelist')
for filename in os.listdir('./module'):
    if filename.endswith('.py'):
        bot.load_extension(f'module.{filename[:-3]}')  

if __name__ == "__main__":
    bot.run(setting['token'])