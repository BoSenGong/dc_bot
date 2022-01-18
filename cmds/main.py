import os
import json
import discord
from discord.ext import commands
from core.classes import Cog_Extension

with open('setting.json','r',encoding='utf8') as jfile:
    setting=json.load(jfile)

class Main(Cog_Extension):
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
            with open('users.json','r') as f :
                users = json.load(f)
            embed = discord.Embed(Title=f"**{ctx.message.author}'s Rang**",Description=f"test1", color=0x0091ff)
            embed.set_thumbnail(url=f"{ctx.message.author.avatar_url}")
            embed.add_field(name=f"**{ctx.message.author}'s Rang**", value="💪  ", inline=False)
            embed.add_field(name="Level", value=f"**{users[str(ctx.message.author.id)]['level']}**", inline=True)
            embed.add_field(name="Experience", value=f"**{str(int(users[str(ctx.message.author.id)]['experience']))}**",inline=True)
            embed.set_footer(text="Chat more to level up!\n")
            await ctx.message.channel.send(embed=embed)

    ### commands for all users ###
    ### rank ###
    @commands.command()
    async def rank(self, ctx):
        #check channel
        #if (ctx.message.channel == setting['level_channel']):
            with open('users.json', 'r') as f:
                users = json.load(f)
                
    ### commands for admin only ###
    ### add exp ###
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, member:discord.Member, exp:int):
        with open('users.json', 'r') as f:
             users = json.load(f)
             await add_exp(users, member, exp)
             await check_level(users, member, ctx.message.channel)
        with open('users.json','w') as f :
            json.dump(users,f)

async def add_exp(users,member:discord.Member,exp:int):
    users[str(member.id)]['experience'] += exp

async def check_level(users,user:discord.Member,channel:int):
    experience = users[str(user.id)]['experience']
    lvl_start = users[str(user.id)]['level']
    lvl_end = int(experience**(1/4))
    if lvl_start < lvl_end:
        await channel.send('{} has leveled up to level {}'.format(user.mention,lvl_end))
        users[str(user.id)]['level'] = lvl_end


    ### commands for admin only ###
    ### parse history messages and give exp ###
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def history(self, ctx):
        print('parsing history messages')

    ### commands for admin only ###
    ### contest rating system ###
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rate(self, ctx):
        print('rating command')

def setup(bot):
    bot.add_cog(Main(bot))