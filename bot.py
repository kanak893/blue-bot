import os

import discord
import random
from simple_settings import settings
from discord.ext import commands
from utilities.GoogleSearch import GoogleSearch
from database.Mongo import MongoUtil

TOKEN = settings.DISCORD_TOKEN
from utilities.logger import Logger

logger = Logger().get_logger()

bot = commands.Bot(command_prefix='!')


@bot.command(name='google', help='Fetches Top 5 links from the google.')
async def query_google(ctx, query):
    try:
        user = ctx.author.name
        logger.info(f"User has searched for query {query}")
        logger.info(f"message in gsearch = {ctx.message.content}")
        search_results = GoogleSearch().search(query=query)
        MongoUtil().upsert_query_results(user=user, query=query)
        logger.info(f"result fetched for user {ctx.message.author}  is {search_results}")
        await ctx.send(search_results)
    except Exception as e:
        logger.error(f"Error in searching google through bot {str(e)}")


@bot.command(name='recent', help='Fetches recent keywords matching the query.')
async def query_google(ctx, query: str):
    try:
        user = ctx.author.name
        response = MongoUtil().fetch_recent_result(user=user, query=query)
        if not response:
            response = "No recent searches found."
        await ctx.send(response)
    except Exception as e:
        logger.error(f"Error in searching google through bot {str(e)}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('You are missing argument query.')


@bot.event
async def on_message(message):
    try:
        if message.author == bot.user:
            return
        logger.info(f" author = {message.author}  user = {bot.user}")
        if message.content == 'hi':
            logger.info(f"message = {message.content}")
            response = "hey"
            await message.channel.send(response)

        # To process commands after the event.
        await bot.process_commands(message)
    except Exception as e:
        logger.error(f"Error in parsing message {str(e)}")


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


if __name__ == "__main__":
    # test mongo connection.
    MongoUtil().get_mongo_client()
    bot.run(TOKEN)
