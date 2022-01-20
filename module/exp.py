import os
import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
from tinydb import TinyDB, Query
from tinydb.operations import add

with open('setting.json','r',encoding='utf8') as jfile:
    setting=json.load(jfile)

class Exp(Cog_Extension):
    ### command for all users ###
    ### ping ###
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'ping: {round(self.bot.latency*1000)} (ms)')

    ### on message event ###
    @commands.Cog.listener()
    async def on_message(self, message):
        #check message.author != bot
        if message.author == self.bot.user:
            return
        #Listen to whitelist channel then copy address to private
        if (message.channel.id == setting['whitelist_channel']):
            await copy_address(self, message)
        #Count level and experience
        db = TinyDB('./users.json')
        user = Query()
        if not db.search(user.id == message.author.id):
            #insert a new user with id
            db.insert({"id": message.author.id, "exp":0,"level":1}) 
        else:
            #old user add exp with message length
            db.update(add("exp",len(message.content)), user.id == message.author.id)
            await check_level(db, user, message.author, message.channel)

    ### command for all users ###
    ### level ###
    @commands.command()    
    async def level(self, ctx):
        #check channel
        #if (ctx.message.channel == setting['level_channel']):
        db = TinyDB('./users.json')
        user = Query()
        await print_level(ctx, db, user)



    ### command for all users ###
    ### rank ###
    @commands.command()
    async def rank(self, ctx):
        #check channel
        #if (ctx.message.channel == setting['level_channel']):
            with open('users.json', 'r') as f:
                users = json.load(f)
                
    ### command for admin only ###
    ### add exp ###
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, member:discord.Member, exp:int):
        db = TinyDB('./users.json')
        user=Query()
        db.update(add("exp",exp), user.id == member.id)
        await check_level(db, user, member, ctx.message.channel)

    '''      
            await check_level(users, member, ctx.message.channel)
            with open('users.json','w') as f :
                json.dump(users,f)

    async def add_exp(User,member:discord.Member,exp:int):
        users[str(member.id)]['experience'] += exp
    '''

    

    ### command for admin only ###
    ### parse history messages and give exp ###
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def history(self, ctx):
        pass

async def check_level(db , user, member:discord.Member, channel:int):
    exp = db.search(user.id == member.id)[0]['exp']
    lvl_start = db.search(user.id == member.id)[0]['level']
    lvl_end = int(exp**(1/4))
    if lvl_start < lvl_end:
        await channel.send('{} has leveled up to level {}'.format(member.mention,lvl_end))
        db.upsert({'level':lvl_end}, user.id == member.id)

async def print_level(ctx, db, user):
    #set embeded message with user level and exp
    embed = discord.Embed(Title=f"**{ctx.message.author}'s Rang**",Description=f"test1", color=0x0091ff)
    embed.set_thumbnail(url=f"{ctx.message.author.avatar_url}")
    embed.add_field(name=f"**{ctx.message.author}'s Rang**", value="💪  ", inline=False)
    embed.add_field(name="Level", value=f"**{db.search(user.id == ctx.message.author.id)[0]['level']}**", inline=True)
    embed.add_field(name="Experience", value=f"**{db.search(user.id == ctx.message.author.id)[0]['exp']}**",inline=True)
    embed.set_footer(text="Chat more to level up!\n")
    await ctx.message.channel.send(embed=embed)

async def copy_address(self, message):
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

def setup(bot):
    bot.add_cog(Exp(bot))