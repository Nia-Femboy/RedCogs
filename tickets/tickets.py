from typing import Optional
import discord

from .common.buttons import TicketButton

from redbot.core import commands, app_commands, Config
from zammad_py import ZammadAPI

buttonLabel = ""

class Tickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=518963742)
        self.config.register_guild(
            host="",
            user="",
            password="",
            embedTitle="Ticket",
            embedDescription="Drücke auf den Button um ein neues Ticket zu erstellen",
            embedFooter="",
            embedFooterURL="",
            buttonLabel="Neues Ticket erstellen",
            tickets={}
    )

    tickets = app_commands.Group(name="ticket", description="Ticket commands")

    @tickets.command(name="setup", description="Konfiguriere das System")
    @app_commands.describe(option="Welche Option soll geändert werden?", wert="Der Wert welcher gesetzt werden soll")
    @app_commands.choices(option=[
        app_commands.Choice(name="Hostname", value="host"),
        app_commands.Choice(name="Username", value="user"),
        app_commands.Choice(name="Password", value="password"),
        app_commands.Choice(name="Embed Title", value="embedTitle"),
        app_commands.Choice(name="Embed Description", value="embedDescription"),
        app_commands.Choice(name="Embed Footer", value="embedFooter"),
        app_commands.Choice(name="Embed Footer URL", value="embedFooterURL")
    ])
    async def setup(self, interaction: discord.Interaction, option: app_commands.Choice[str], wert: str):
        try:
            match option:

                case "host":

                    await self.config.guild(interaction.guild).host.set_raw(wert)

                case "user":

                    await self.config.guild(interaction.guild).user.set_raw(wert)

                case "password":

                    await self.config.guild(interaction.guild).password.set_raw(wert)

                case "embedTitle":

                    await self.config.guild(interaction.guild).embedTitle.set_raw(wert)

                case "embedDescription":

                    await self.config.guild(interaction.guild).embedDescription.set_raw(wert)

                case "embedFooter":

                    await self.config.guild(interaction.guild).embedFooter.set_raw(wert)

                case "embedFooterURL":

                    await self.config.guild(interaction.guild).embedFooterURL.set_raw(wert)

        except Exception as error:
            print(error)

    @tickets.command(name="create", description="Erstelle ein neues Ticket")
    async def create(self, interaction: discord.Interaction):
        try:

            embed = discord.Embed(title=await self.config.guild(interaction.guild).embedTitle(), description=await self.config.guild(interaction.guild).embedDescription())

            await interaction.response.send_message(embed=embed, view=TicketButton())
            await TicketButton.wait()

        except Exception as error:
            print(error)