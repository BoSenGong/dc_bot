import os
import json
from core.classes import Cog_Extension
import discord
from discord.ext import commands

with open('setting.json','r',encoding='utf8') as jfile:
    setting=json.load(jfile)

class Event(Cog_Extension):
    ### bot on ready event ###
    @commands.Cog.listener()
    async def on_ready(self):
        print(">>> AcaPunks Bot is online. <<<")

    ### on member join event ###
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(setting['welcome_channel'])
        await channel.send(f"{member} join!")

    ### on message event ###
    @commands.Cog.listener()
    async def on_message(self, message):
        #check message.author != bot
        if message.author == self.bot.user:
            return

        #Listen to whitelist channel then copy address
        if (message.channel.id == setting['whitelist_channel']):        
            #Check address
            if message.content.startswith('0x'):  
                msg = message.content
                await message.delete()
                await message.channel.send(f"{message.author.mention} address received.")
                #Go to private address channel
                channel = self.bot.get_channel(setting['whitelist_private_channel']) 
                await channel.send(f"{message.author.mention}  "+msg)
            else:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Please leave your address only.")   

        #Count level and experience
        with open('users.json','r') as f :
            users = json.load(f)
            await update_data(self,users, message.author)
            await add_experience(self,users,message.author,5)
            await level_up(self,users,message.author, message.channel)
        with open('users.json','w') as f :
            json.dump(users,f)

async def update_data(self,users, user:discord.Member):
    if not str(user.id) in users:
        users[str(user.id)] ={}
        users[str(user.id)]['experience'] = 0
        users[str(user.id)]['level'] = 1 

async def add_experience(self,users,user:discord.Member,exp:int):
    users[str(user.id)]['experience'] += exp

async def level_up(self,users,user,channel):
    experience = users[str(user.id)]['experience']
    lvl_start = users[str(user.id)]['level']
    lvl_end = int(experience**(1/4))
    if lvl_start < lvl_end:
        channel = self.bot.get_channel(setting['level_channel']) 
        await channel.send('{} has leveled up to level {}'.format(user.mention,lvl_end))
        users[str(user.id)]['level'] = lvl_end
#Count level and experience end 
    
def setup(bot):
    bot.add_cog(Event(bot))