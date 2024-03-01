import discord

from redbot.core import commands, app_commands, Config

embedSuccess = discord.Embed(title="Erfolgreich", description="Es wurden folgende Werte gesetzt:", color=0x0ffc03)
embedFailure = discord.Embed(title="Fehler", color=0xff0000)

class EventMessages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=518963742)
        self.config.register_guild(
            wMessage = "",
            gbMessage = "",
            wMessageChannel = 0,
            gbMessageChannel = 0,
            wEnable = False,
            gbEnable = False,
            wmEntion = False,
            useEmbed = True
        )

        eventmessages = app_commands.Group(name="eventmessage", description="Lasse dir Nachrichten für Events ausgeben")

        @eventmessages.command(name="setup", description="Einrichten der Nachrichten")
        @app_commands.describe(type="Die zu setzende Einstellung", welcome="Konfiguriere die Willkommensnachrichten")
        @app_commands.choices(type=[
            app_commands.Choice(name="Willkommensnachricht", value="wMessage"),
            app_commands.Choice(name="Nachricht beim verlassen", value="gbNessage"),
            app_commands.Choice(name="Willkommensnachricht Channel", value="wMessageChannel")
        ])
        @app_commands.checks.has_permissions(administrator=True)
        async def setup(self, interaction: discord.Interaction, type: app_commands.Choice[str], value: str):
            try:
                print()
            except Exception as error:
                embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
                await interaction.response.send_message(embed=embedFailure, ephemeral=True)

        @commands.Cog.listener()
        async def on_member_join(self, member):
            try:
                print()
            except Exception as error:
                print("on_member_join Fehler: " + str(error))

        @commands.Cog.listener()
        async def on_raw_member_remove(self, data):
            try:
                print()
            except Exception as error:
                print("on_raw_member_remove Fehler: " + str(error))