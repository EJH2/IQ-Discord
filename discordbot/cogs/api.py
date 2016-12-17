"""
API Commands
"""

import aiohttp
from discord.ext import commands

from discordbot.bot import DiscordBot


class API:
    def __init__(self, bot: DiscordBot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def api(self, ctx):
        """Gives information on various APIs.

            Currently available APIs: steam, discord
        """

        if ctx.invoked_subcommand is None:
            await self.bot.say("{0.subcommand_passed}, isn\t ".format(ctx))

    @api.command()
    async def steam(self):
        """
        Steam API
        """
        url = "https://steamgaug.es/api/v2"
        with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp = await resp.json()
        if resp["ISteamClient"]["online"] == 1:
            steam_client = "Online"
        else:
            steam_client = "Offline"
        if resp["SteamCommunity"]["online"] == 1:
            steam_community = "Online"
        else:
            steam_community = "Offline"
        if resp["SteamStore"]["online"] == 1:
            steam_store = "Online"
        else:
            steam_store = "Offline"
        if resp["ISteamUser"]["online"] == 1:
            steam_user = "Online"
        else:
            steam_user = "Offline"
        if resp["IEconItems"]["440"]["online"] == 1:
            steam_tf2_items = "Online"
        else:
            steam_tf2_items = "Offline"
        if resp["IEconItems"]["570"]["online"] == 1:
            steam_dota2_items = "Online"
        else:
            steam_dota2_items = "Offline"
        if resp["IEconItems"]["730"]["online"] == 1:
            steam_csgo_items = "Online"
        else:
            steam_csgo_items = "Offline"
        if resp["ISteamGameCoordinator"]["440"]["online"] == 1:
            steam_tf2_games = "Online"
        else:
            steam_tf2_games = "Offline"
        if resp["ISteamGameCoordinator"]["570"]["online"] == 1:
            steam_dota2_games = "Online"
        else:
            steam_dota2_games = "Offline"
        if resp["ISteamGameCoordinator"]["730"]["online"] == 1:
            steam_csgo_games = "Online"
        else:
            steam_csgo_games = "Offline"
        x = "Steam Statuses:\n" \
            "	Steam Client: \"{0}\"\n" \
            "	Steam Community: \"{1}\"\n" \
            "	Steam Store: \"{2}\"\n" \
            "	Steam Users: \"{3}\"\n" \
            "	Item Servers:\n" \
            "        TF2: \"{4}\"\n" \
            "        DOTA 2: \"{5}\"\n" \
            "        CS:GO: \"{6}\"\n" \
            "	Game Coordinator:\n" \
            "        TF2: \"{7}\"\n" \
            "        DOTA 2: \"{8}\"\n" \
            "        CS:GO: \"{9}\"".format(
            steam_client, steam_community, steam_store, steam_user, steam_tf2_items, steam_dota2_items,
            steam_csgo_items, steam_tf2_games, steam_dota2_games, steam_csgo_games)
        await self.bot.say("```xl\n{}\n```".format(x))

    @api.command()
    async def discord(self):
        """
        Discord API
        """
        url = "https://srhpyqt94yxb.statuspage.io/api/v2/summary.json"
        with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp = await resp.json()
        x = "Discord Statuses:\n" \
            "	Overall Status: \"{13}\"\n" \
            "    API: \"{0}\"\n" \
            "	Gateway: \"{1}\"\n" \
            "    CloudFlare: \"{2}\"\n" \
            "    Voice: \"{3}\"\n" \
            "        Amsterdam: \"{4}\"\n" \
            "        Frankfurt: \"{5}\"\n" \
            "        London: \"{6}\"\n" \
            "        Singapore: \"{7}\"\n" \
            "        Sydney: \"{8}\"\n" \
            "        US Central: \"{9}\"\n" \
            "        US East: \"{10}\"\n" \
            "        US South: \"{11}\"\n" \
            "        US West: \"{12}\"".format(
            resp["components"][1]["status"], resp["components"][2]["status"], resp["components"][4]["status"],
            resp["components"][7]["status"], resp["components"][0]["status"], resp["components"][3]["status"],
            resp["components"][5]["status"], resp["components"][6]["status"], resp["components"][8]["status"],
            resp["components"][9]["status"], resp["components"][10]["status"], resp["components"][11]["status"],
            resp["components"][12]["status"], resp["status"]["description"])
        await self.bot.say("```xl\n{}\n```".format(x))


def setup(bot: DiscordBot):
    bot.add_cog(API(bot))