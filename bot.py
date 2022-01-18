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
for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f'cmds.{filename[:-3]}')

### bot on ready event ###
@bot.event
async def on_ready():
    print(">>> AcaPunks Bot is online. <<<")

### on member join event ###
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(setting['welcome_channel'])
    await channel.send(f"{member} join!")

### on message event ###
@bot.event
async def on_message(message):
    #check message.author != bot
    if message.author == bot.user:
        return

    #Listen to whitelist channel then copy address
    if (message.channel.id == setting['whitelist_channel']):        
        #Check address
        if message.content.startswith('0x'):  
            msg = message.content
            await message.delete()
            await message.channel.send(f"{message.author.mention} address received.")
            #Go to private address channel
            channel = bot.get_channel(setting['whitelist_private_channel']) 
            await channel.send(f"{message.author.mention}  "+msg)
        else:
            await message.delete()
            await message.channel.send(f"{message.author.mention} Please leave your address only.")   

#Count level and experience
    with open('users.json','r') as f :
        users = json.load(f)
        await update_data(users, message.author)
        await add_experience(users,message.author,5)
        await level_up(users,message.author, message.channel)
    with open('users.json','w') as f :
        json.dump(users,f)
    await bot.process_commands(message)

async def update_data(users, user:discord.Member):
    if not str(user.id) in users:
        users[str(user.id)] ={}
        users[str(user.id)]['experience'] = 0
        users[str(user.id)]['level'] = 1 

async def add_experience(users,user:discord.Member,exp:int):
    users[str(user.id)]['experience'] += exp

async def level_up(users,user,channel):
    experience = users[str(user.id)]['experience']
    lvl_start = users[str(user.id)]['level']
    lvl_end = int(experience**(1/4))
    if lvl_start < lvl_end:
        channel = bot.get_channel(setting['level_channel']) 
        await channel.send('{} has leveled up to level {}'.format(user.mention,lvl_end))
        users[str(user.id)]['level'] = lvl_end
#Count level and experience end   

if __name__ == "__main__":
    bot.run(setting['token'])