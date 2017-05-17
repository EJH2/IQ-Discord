"""
Main bot file.
"""

import asyncio
import sys
import traceback
from collections import Counter

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from discordbot.cogs.utils import config, exceptions, util, formatter
from discordbot.consts import modules, bot_config


class DiscordBot(Bot):
    """
    Bot class.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bot_config = bot_config

        # Set up logging
        self.logger = formatter.setup_logger("Bot")
        self.command_logger = formatter.setup_logger("Commands")
        self.file_logger = formatter.file_logger

        self.logging = bot_config.get("logging", "True")

        self._loaded = False

        self.restarting = config.Config("restart.yaml")
        self.ignored = config.Config("ignored.yaml")

        self.owner_id = None

        self.pm_help = True

        self.commands_used = Counter()

        # As the great Danny once said: "pay no mind to this ugliness."
        self.remove_command("help")
        self.command(**self.help_attrs)(formatter.default_help_command)

    def __del__(self):
        # Silence aiohttp.
        if not self.http.session.closed:
            self.http.session.close()

    async def on_ready(self):
        if self._loaded:
            return

        self.logger.info("Loaded Bot:")
        self.logger.info("Logged in as {0.user.name}#{0.user.discriminator}".format(self))
        self.logger.info("ID is {0.user.id}".format(self))
        self.description = "Hello, this is the help menu for {0.user.name}!".format(self)

        self.logger.info("Downloading application info...")
        app_info = await self.application_info()
        self.owner_id = app_info.owner.id
        self.logger.info("I am owned by {}, setting owner.".format(str(app_info.owner)))

        # Attempt to load Bot modules
        for mod in modules:
            try:
                self.load_extension(mod)
            except Exception as e:
                self.logger.critical("Could not load extension `{}` -> `{}`".format(mod, e))
                self.logger.exception()
            else:
                self.logger.info("Loaded extension {}.".format(mod))

        if self.restarting.get("restarting"):
            await self.get_channel(int(self.restarting.get("restart_channel"))).send("Finished! Hello again ;)")
            self.restarting.delete("restarting")

        self._loaded = True

    async def on_message_edit(self, before, after):
        """
        Checks message edit to see if I screwed up a command...
        """
        await super().on_message(after)

    async def on_command_error(self, ctx, e):
        """
        Catch command errors.
        """
        if isinstance(e, exceptions.Ignored):
            await ctx.message.channel.send("\N{CROSS MARK} This channel is currently being ignored.", delete_after=5)
            return
        elif isinstance(e, commands.errors.NotOwner):
            await ctx.message.channel.send(e, delete_after=5)
        elif isinstance(e, exceptions.ClearanceError):
            await ctx.message.channel.send(e, delete_after=5)
            return
        elif isinstance(e, commands.errors.CommandNotFound):
            return
        elif isinstance(e, exceptions.EmbedError):
            await ctx.message.channel.send("\N{NO ENTRY} This command requires the `Embed Links` "
                                           "permission to execute!", delete_after=5)
            return
        elif isinstance(e, commands.errors.NoPrivateMessage):
            await ctx.message.channel.send("\N{NO ENTRY} That command can not be run in PMs!",
                                           delete_after=5)
        elif isinstance(e, commands.errors.DisabledCommand):
            await ctx.message.channel.send("\N{NO ENTRY} Sorry, but that command is currently disabled!",
                                           delete_after=5)
        elif isinstance(e, commands.errors.CheckFailure):
            await ctx.message.channel.send("\N{CROSS MARK} Check failed. You probably don't have "
                                           "permission to do this.", delete_after=5)
            return
        elif isinstance(e, (commands.errors.BadArgument, commands.errors.MissingRequiredArgument)):
            await ctx.message.channel.send("\N{CROSS MARK} Bad argument: {}".format(" ".join(e.args)), delete_after=5)
        else:
            await ctx.message.channel.send("\N{NO ENTRY} An error happened. This has been logged and reported.",
                                           delete_after=5)
            if isinstance(e, commands.errors.CommandInvokeError):
                traceback.print_exception(type(e), e.__cause__, e.__cause__.__traceback__, file=sys.stderr)
            else:
                traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)

    async def on_command(self, ctx):
        author = str(ctx.author)
        if ctx.guild is not None:
            self.command_logger.info("{0.guild.name} (ID: {0.guild.id}) > {author} (ID: {0.author.id}): {0.message"
                                     ".clean_content}".format(ctx, author=author))
        else:
            self.command_logger.info("Private Messages > {author} (ID: {0.author.id}): {0.message.clean_content}"
                                     .format(ctx, author=author))

    async def on_command_completion(self, ctx):
        self.commands_used[ctx.command.name] += 1
        await asyncio.sleep(5)
        try:
            await ctx.message.delete()
        except discord.DiscordException:
            pass

    def _run(self):
        """
        Convenience function to run the bot with the specified token.
        """
        try:
            super().run(self.bot_config["bot"]["token"])
        except discord.errors.LoginFailure as e:
            self.logger.error("Failed to login to discord: {}".format(e.args[0]))

    def run(self):
        """
        Extra cleanup for _run.
        """
        self._run()
        input("Press any key to continue...")
        sys.exit(2)
