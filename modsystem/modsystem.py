import discord

from redbot.core import commands, app_commands, Config
from datetime import datetime, timedelta

embedSuccess = discord.Embed(title="Erfolgreich", description="Es wurden folgende Werte gesetzt:", color=0x0ffc03)
embedFailure = discord.Embed(title="Fehler", color=0xff0000)
embedLog = discord.Embed(title="Logsystem", color=0xfc7f03)

class Modsystem(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=518963742)
        self.config.register_guild(
            generalLogChannel=0,
            warnLogChannel=0,
            enableWarnLog=False,
            kickLogChannel=0,
            enableKickLog=False,
            banLogChannel=0,
            enableBanLog=False,
            updateLogChannel=0,
            enableUpdateLog=False,
            useGeneralLogChannel=True,
            users={}
        )

    modsystem = app_commands.Group(name="modlog", description="Modlog setup commands")

    @modsystem.command(name="setgenerallogchannel", description="Setze den Allgemeinen Logchannel")
    @app_commands.describe(channelid="Die ChannelID des Allgemeinen Logchannels")
    @app_commands.checks.has_permissions(administrator=True)
    async def setgenerallogchannel(self, interaction: discord.Interaction, channelid: str):
        try:
            if(interaction.guild.get_channel(int(channelid)) is None):
                raise Exception("Channel existiert nicht")
            await self.config.guild(interaction.guild).generalLogChannel.set(int(channelid))
            embedSuccess.add_field(name="General Log Channel", value=channelid, inline=True)
            await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="setwarninglogchannel", description="Setze den Logchannel für warning")
    @app_commands.describe(channelid="Die ChannelID des warning Logchannels")
    @app_commands.checks.has_permissions(administrator=True)
    async def setwarninglogchannel(self, interaction: discord.Interaction, channelid: str):
        try:
            if(interaction.guild.get_channel(int(channelid)) is None):
                raise Exception("Channel existiert nicht")
            await self.config.guild(interaction.guild).warnLogChannel.set(int(channelid))
            embedSuccess.add_field(name="Warning Log Channel", value=channelid, inline=True)
            await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="setkicklogchannel", description="Sete den Logchannel für kicks")
    @app_commands.describe(channelid="Die ChannelID des kick Logchannels")
    @app_commands.checks.has_permissions(administrator=True)
    async def setkicklogchannel(self, interaction: discord.Interaction, channelid: str):
        try:
            if(interaction.guild.get_channel(int(channelid)) is None):
                raise Exception("Channel existiert nicht")
            await self.config.guild(interaction.guild).kickLogChannel.set(int(channelid))
            embedSuccess.add_field(name="Kick Log Channeöl", value=channelid, inline=True)
            await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="setbanlogchannel", description="Setzte den Logchannel für bans")
    @app_commands.describe(channelid="Die ChannelID des Ban Logchannel")
    @app_commands.checks.has_permissions(administrator=True)
    async def setbanlogchannel(self, interaction: discord.Interaction, channelid: str):
        try:
            if(interaction.guild.get_channel(int(channelid)) is None):
                raise Exception("Channel existiert nicht")
            await self.config.guild(interaction.guild).banlogchannel.set(int(channelid))
            embedSuccess.add_field(name="Ban Log Channel", value=channelid)
            await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="setupdatelogchannel", description="Setze den Logchanneö für Client-Updates")
    @app_commands.describe(channelid="Die ChannelID des Client-Update Logchannel")
    @app_commands.checks.has_permissions(administrator=True)
    async def setupdatelogchannel(self, interaction: discord.Interaction, channelid: str):
        try:
            if(interaction.guild.get_channel(int(channelid)) is None):
                raise Exception("Channel existiert nicht")
            await self.config.guild(interaction.guild).updateLogChannel.set(int(channelid))
            embedSuccess.add_field(name="Client-Update Log Channel", value=channelid)
            await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="usemultiplelogchannel", description="Nutze mehrere Logchannel")
    @app_commands.describe(multiplelogchannel="Sollen mehrere Channel genutzt werden?")
    @app_commands.checks.has_permissions(administrator=True)
    async def usemultiplelogchannel(self, interaction: discord.Interaction, multiplelogchannel: bool):
        try:
            if(await self.config.guild(interaction.guild).generalLogChannel() is None):
                raise Exception("Kein gültiger Channel definiert")
            await self.config.guild(interaction.guild).useGeneralLogChannel.set(multiplelogchannel)
            embedSuccess.add_field(name="Nutze General Log Channel", value=multiplelogchannel, inline=True)
            await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="enablebanlog", description="Aktiviere oder deaktiviere das Loggen der Bans")
    @app_commands.describe(activate="Aktivieren oder deaktivieren")
    @app_commands.checks.has_permissions(administrator=True)
    async def enablebanlog(self, interaction: discord.Interaction, activate: bool):
        try:
            if(await self.config.guild(interaction.guild).banlogchannel() is None):
                raise Exception("Kein gültiger Channel definiert")
            await self.config.guild(interaction.guild).enableBanLog.set(activate)
            embedSuccess.add_field(name="Ban Log", value=activate)
            await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="enablekicklog", description="Aktiviere oder deaktiviere das Loggen der Kicks")
    @app_commands.describe(activate="Aktivieren oder deaktivieren")
    @app_commands.checks.has_permissions(administrator=True)
    async def enablekicklog(self, interaction: discord.Interaction, activate: bool):
        try:
            if(await self.config.guild(interaction.guild).kickLogChannel() is None):
                raise Exception("Kein gültiger Channel definiert")
            await self.config.guild(interaction.guild).enableKickLog.set(activate)
            embedSuccess.add_field(name="Kick Log", value=activate)
            await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="enableupdatelog", description="Aktiviere oder deaktiviere das Loggen der Client-Updates")
    @app_commands.describe(activate="Aktivieren oder deaktivieren")
    @app_commands.checks.has_permissions(administrator=True)
    async def enableupdatelog(self, interaction: discord.Interaction, activate: bool):
        try:
            if(await self.config.guild(interaction.guild).updateLogChannel() is None):
                raise Exception("Kein gültiger Channel definiert")
            await self.config.guild(interaction.guild).enableUpdateLog.set(activate)
            embedSuccess.add_field(name="Client-Update Log", value=activate)
            await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure)

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry):
        try:
            #channel = entry.guild.get_channel(1186750967476142111)
            if(entry.action == discord.AuditLogAction.kick and await self.config.guild(entry.guild).enableKickLog() == 1):
                channel = entry.guild.get_channel(await self.config.guild(entry.guild).kickLogChannel())
                if(entry.reason is not None):
                    embedLog.description=entry.target.mention + " wurde von " + entry.user.mention + " mit der Begründung **" + entry.reason + "** gekickt"
                else:
                    embedLog.description=entry.target.mention + " wurde von " + entry.user.mention + " gekickt"
                await channel.send(embed=embedLog)
            elif(entry.action == discord.AuditLogAction.ban and await self.config.guild(entry.guild).enableBanLog() == 1):
                channel = entry.guild.get_channel(await self.config.guild(entry.guild).banLogChannel())
                if(entry.reason is not None):
                    embedLog.description=entry.target.mention + " wurde von " + entry.user.mention + " mit der Begründung **" + entry.reason + "** gebant"
                else:
                    embedLog.description=entry.target.mention + " wurde von " + entry.user.mention + " gebant"
                await channel.send(embed=embedLog)
            elif(entry.action == discord.AuditLogAction.member_update and await self.config.guild(entry.guild).enableUpdateLog() == 1):
                channel = entry.guild.get_channel(await self.config.guild(entry.guild).updateLogChannel())
                print(await self.config.guild(entry.guild).useGeneralLogChannel())
                if(entry.after.timed_out_until is not None):
                    timeout_time = str(timedelta(seconds=round((entry.after.timed_out_until - datetime.now(entry.after.timed_out_until.tzinfo)).total_seconds())))
                    if(entry.reason is not None):
                        embedLog.description=entry.target.mention + " hat von " + entry.user.mention + " einen Timeout für **" + timeout_time + "** mit der Begründung **" + entry.reason + "** bekommen"
                    else:
                        embedLog.description=entry.target.mention + " hat von " + entry.user.mention + " einen Timeout für **" + timeout_time + "** bekommen"
                    await channel.send(embed=embedLog)
                elif(entry.after.timed_out_until is None):
                    timeout_time = str(timedelta(seconds=round((entry.before.timed_out_until - datetime.now(entry.before.timed_out_until.tzinfo)).total_seconds())))
                    embedLog.description=entry.user.mention + " hat den Timeout von " + entry.target.mention + "aufgehoben"
                    embedLog.add_field(name="Verbleibende Zeit", value=timeout_time, inline=True)
                    await channel.send(embed=embedLog)
                    embedLog.clear_fields()
        except Exception as error:
            print(error)