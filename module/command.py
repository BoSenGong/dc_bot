import os
import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
from tinydb import TinyDB, Query
from tinydb.operations import add

with open('setting.json','r',encoding='utf8') as jfile:
    setting=json.load(jfile)

class Command(Cog_Extension):
    ### command for all users ###
    ### ping ###
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'ping: {round(self.bot.latency*1000)} (ms)')

    ### command for all users ###
    ### level ###
    @commands.command()    
    async def level(self, ctx):
        #check channel
        #if (ctx.message.channel == setting['level_channel']):
        db = TinyDB('./users.json')
        user = Query()
        await print_level(ctx, db, user)

async def print_level(ctx, db, user):
    #set embeded message with user level and exp
    embed = discord.Embed(Title=f"**{ctx.message.author}'s Rang**",Description=f"test1", color=0x0091ff)
    embed.set_thumbnail(url=f"{ctx.message.author.avatar_url}")
    embed.add_field(name=f"**{ctx.message.author}'s Rang**", value="💪  ", inline=False)
    embed.add_field(name="Level", value=f"**{db.search(user.id == ctx.message.author.id)[0]['level']}**", inline=True)
    embed.add_field(name="Experience", value=f"**{db.search(user.id == ctx.message.author.id)[0]['exp']}**",inline=True)
    embed.set_footer(text="Chat more to level up!\n")
    await ctx.message.channel.send(embed=embed)

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
        #then check level

        '''      
            await check_level(users, member, ctx.message.channel)
        with open('users.json','w') as f :
            json.dump(users,f)

async def add_exp(User,member:discord.Member,exp:int):
    users[str(member.id)]['experience'] += exp

async def check_level(users,user:discord.Member,channel:int):
    experience = users[str(user.id)]['experience']
    lvl_start = users[str(user.id)]['level']
    lvl_end = int(experience**(1/4))
    if lvl_start < lvl_end:
        await channel.send('{} has leveled up to level {}'.format(user.mention,lvl_end))
        users[str(user.id)]['level'] = lvl_end
'''

    ### command for admin only ###
    ### parse history messages and give exp ###
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def history(self, ctx):
        print('parsing history messages')

    ### command for admin only ###
    ### contest rating system ###
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rate(self, ctx):
        print('rating command')

def setup(bot):
    bot.add_cog(Command(bot))