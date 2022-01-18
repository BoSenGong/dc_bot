import os
import json
import discord
from discord.ext import commands
from core.classes import Cog_Extension

with open('setting.json','r',encoding='utf8') as jfile:
    setting=json.load(jfile)

class Main(Cog_Extension):
    ###### commands for all users ######
    ### ping ###
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'ping: {round(self.bot.latency*1000)} (ms)')

    ###### commands for all users ######
    ### level ###
    @commands.command()    
    async def level(self, ctx):
        #check channel
        #if (ctx.message.channel == setting['level_channel']):
            with open('users.json','r') as f :
                users = json.load(f)
            #await ctx.message.channel.send('{} has {} exp'.format(ctx.message.author.mention,users[str(ctx.message.author.id)]['experience']))
            embed = discord.Embed(Title=f"**{ctx.message.author}'s Rang**",Description=f"test1", color=0x0091ff)
            embed.set_thumbnail(url=f"{ctx.message.author.avatar_url}")
            embed.add_field(name=f"**{ctx.message.author}'s Rang**", value="💪  ", inline=False)
            embed.add_field(name="Level", value=f"**{users[str(ctx.message.author.id)]['level']}**", inline=True)
            embed.add_field(name="Experience", value=f"**{str(int(users[str(ctx.message.author.id)]['experience']))}**",inline=True)
            embed.set_footer(text="Chat more to level up!\n")
            await ctx.message.channel.send(embed=embed)

    ###### commands for all users ######
    ### rank ###
    @commands.command()
    async def rank(self, ctx):
        #check channel
        #if (ctx.message.channel == setting['level_channel']):
            with open('users.json', 'r') as f:
                users = json.load(f)
                leaderboard = {}
                total=[]
                for user in users:
                    name = int(user)
                    total_amt = users[str(user.id)]['experience']
                    leaderboard[total_amt] = name
                    total.append(total_amt)
                total = sorted(total,reverse=True)
                print(total)

    ###### commands for admin only ######
    ### add exp ###
    @commands.command()
    async def add(self, ctx):
        print('add exp command')

    ###### commands for admin only ######
    ### parse history messages and give exp ###
    @commands.command()
    async def history(self, ctx):
        print('parsing history messages')

    ###### commands for admin only ######
    ### contest rating system ###
    @commands.command()
    async def rate(self, ctx):
        print('rating command')

def setup(bot):
    bot.add_cog(Main(bot))