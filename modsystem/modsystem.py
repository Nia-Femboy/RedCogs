import discord
import re
import requests
import os
import io

from discord.utils import MISSING
from discord.ext import tasks

from redbot.core import commands, app_commands, Config
from datetime import datetime, timedelta, timezone
from PIL import Image

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
            enableWarn=False,
            kickLogChannel=0,
            enableKickLog=False,
            banLogChannel=0,
            enableBanLog=False,
            updateLogChannel=0,
            enableUpdateLog=False,
            useGeneralLogChannel=True,
            joinLogChannel=0,
            enableJoinLog=False,
            deleteMessageLogChannel=0,
            enableDeleteMessageLog=False,
            enableVoiceLog=False,
            warnWeight=0,
            warnKickWeight=0,
            warnBanWeight=0,
            warnDynamicReset=False,
            warnDynamicResetTime=0,
            warnDynamicResetCount=0,
            warnResetTime=0,
            warnUsePublicChannel=False,
            warnPublicChannel=0,
            warnUseDM=True,
            modRole=0,
            warnFirstMultiplicator=1,
            warnSecondMultiplicator=1,
            warnThirdMultiplicator=1,
            softBanChannel=0,
            softBanLogChannel=0,
            deleteLinks=False,
            linkPattern=r"https?:\/\/.*\..{2,}",
            saveDeletedPics=False,
            users={},
            invites={}
        )

    modsystem = app_commands.Group(name="modlog", description="Modlog setup commands")

    @modsystem.command(name="setupchannel", description="Allgemeines Setup des Systems")
    @app_commands.describe(choice="Bitte den gewünschten Parameter auswählen", channel="Der zu nutzende Channel")
    @app_commands.choices(choice=[
        app_commands.Choice(name="General Logchannel", value="gChannel"),
        app_commands.Choice(name="Warn Logchannel", value="wChannel"),
        app_commands.Choice(name="Kick Logchannel", value="kChannel"),
        app_commands.Choice(name="Ban Logchannel", value="bChannel"),
        app_commands.Choice(name="Update Logchannel", value="uChannel"),
        app_commands.Choice(name="Join Logchannel", value="jChannel"),
        app_commands.Choice(name="Message Logchannel", value="mChannel"),
        app_commands.Choice(name="Softban Channel", value="sbChannel"),
        app_commands.Choice(name="Softban Logchannel", value="sblChannel"),
        app_commands.Choice(name="Warn Public Channel", value="wpChannel")
    ])
    @app_commands.checks.has_permissions(administrator=True)
    async def setupchannel(self, interaction: discord.Interaction, choice: app_commands.Choice[str], channel: discord.TextChannel):
        try:

            if(interaction.guild.get_channel(channel.id) is None):
                        raise Exception("Channel existiert nicht")

            match choice.value:

                case "gChannel":

                    await self.config.guild(interaction.guild).generalLogChannel.set(channel.id)
                    embedSuccess.add_field(name="General Log Channel", value=f"<#{channel.id}>")

                case "wChannel":

                    await self.config.guild(interaction.guild).warnLogChannel.set(channel.id)
                    embedSuccess.add_field(name="Warning Log Channel", value=f"<#{channel.id}>")

                case "kChannel":

                    await self.config.guild(interaction.guild).kickLogChannel.set(channel.id)
                    embedSuccess.add_field(name="Kick Log Channeöl", value=f"<#{channel.id}>")

                case "bChannel":

                    await self.config.guild(interaction.guild).banLogChannel.set(channel.id)
                    embedSuccess.add_field(name="Ban Log Channel", value=f"<#{channel.id}>")

                case "uChannel":

                    await self.config.guild(interaction.guild).updateLogChannel.set(channel.id)
                    embedSuccess.add_field(name="Client-Update Log Channel", value=f"<#{channel.id}>")

                case "jChannel":

                    await self.config.guild(interaction.guild).joinLogChannel.set(channel.id)
                    embedSuccess.add_field(name="Join Log Channel", value=f"<#{channel.id}>")

                case "mChannel":

                    await self.config.guild(interaction.guild).deleteMessageLogChannel.set(channel.id)
                    embedSuccess.add_field(name="Delete Message Log Channel", value=f"<#{channel.id}>")

                case "sbChannel":

                    await self.config.guild(interaction.guild).softBanChannel.set(channel.id)
                    await interaction.response.defer()
                    overwriteHide = discord.PermissionOverwrite()
                    overwriteShow = discord.PermissionOverwrite()
                    overwriteHide.view_channel=False
                    overwriteShow.view_channel=True
                    for user in interaction.guild.members:
                        if(await self.config.guild(interaction.guild).users.get_raw(user.id, 'softBanned')):
                            for dChannel in interaction.guild.channels:
                                if(dChannel.id == channel.id):
                                    await dChannel.set_permissions(user, overwrite=overwriteShow)
                                else:
                                    await dChannel.set_permissions(user, overwrite=overwriteHide)
                    embedSuccess.add_field(name="Softban Channel", value=f"<#{channel.id}>")

                case "sblChannel":

                    await self.config.guild(interaction.guild).softBanLogChannel.set(channel.id)
                    embedSuccess.add_field(name="Softban Log Channel", value=f"<#{channel.id}>")

                case "wpChannel":

                    await self.config.guild(interaction.guild).warnPublicChannel.set(channel.id)
                    embedSuccess.add_field(name="Warn Public Channel", value=f"<#{channel.id}>")

            if(choice.value == "sbChannel"):
                await interaction.followup.send(embed=embedSuccess)
            else:
                await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()

        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    @modsystem.command(name="enable", description="Aktiviere die einzelnen Funktionen")
    @app_commands.describe(choice="Die gewünschte Funktion", status="Ein- oder Ausschalten")
    @app_commands.choices(choice=[
        app_commands.Choice(name="Nutze den Generellen Logchannel", value="useGChannel"),
        app_commands.Choice(name="Warnfunktion", value="warn"),
        app_commands.Choice(name="Kicklog", value="kLog"),
        app_commands.Choice(name="Banlog", value="bLog"),
        app_commands.Choice(name="Updatelog", value="uLog"),
        app_commands.Choice(name="Joinlog", value="jLog"),
        app_commands.Choice(name="Messagelog", value="mLog"),
        app_commands.Choice(name="Voicelog", value="vLog"),
        app_commands.Choice(name="Message Link Detection", value="mLinks"),
        app_commands.Choice(name="Speichere gelöschte Bilder lokal", value="sdPics")
    ])
    @app_commands.checks.has_permissions(administrator=True)
    async def enable(self, interaction: discord.Interaction, choice: app_commands.Choice[str], status: bool):
        try:

            match choice.value:

                case "useGChannel":

                    if(status):
                        if(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is None):
                            raise Exception("Kein gültiger Channel definiert")
                        else:
                            await self.config.guild(interaction.guild).useGeneralLogChannel.set(status)
                            embedSuccess.add_field(name="Nutze General Log Channel", value=status, inline=True)
                    else:
                        await self.config.guild(interaction.guild).useGeneralLogChannel.set(status)
                        embedSuccess.add_field(name="Nutze General Log Channel", value=status, inline=True)

                case "warn":

                    if(status):
                        if((interaction.guild.get_channel(int(await self.config.guild(interaction.guild).warnLogChannel())) is not None) or (await self.config.guild(interaction.guild).useGeneralLogChannel() and interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is not None)):
                            if(await self.config.guild(interaction.guild).warnResetTime() > 0 and await self.config.guild(interaction.guild).warnDynamicReset() == False):
                                await self.config.guild(interaction.guild).enableWarn.set(status)
                                Modsystem.remove_warn_points.change_interval(minutes=await self.config.guild(interaction.guild).warnResetTime())
                                if(Modsystem.remove_warn_points.is_running == False):
                                    Modsystem.remove_warn_points.start(self)
                                    print("Warnsystem aktiviert")
                                embedSuccess.add_field(name="Aktiviere Warn funktion", value=status)
                            elif(await self.config.guild(interaction.guild).warnDynamicReset() and await self.config.guild(interaction.guild).warnDynamicResetTime() > 0):
                                await self.config.guild(interaction.guild).enableWarn.set(status)
                                Modsystem.remove_warn_points.change_interval(minutes=await self.config.guild(interaction.guild).warnDynamicResetTime())
                                if(Modsystem.remove_warn_points.is_running == False):
                                    Modsystem.remove_warn_points.start(self)
                                    print("Warnsystem aktiviert")
                                embedSuccess.add_field(name="Aktiviere Warn funktion", value=status)
                            else:
                                raise Exception("Die Resettime muss größer 0 sein")
                        elif(await self.config.guild(interaction.guild).warnUseChannel() and interaction.guild.get_channel(int(await self.config.guild(interaction.guild).warnLogChannel())) is None):
                            raise Exception("Kein gültiger Channel definiert")
                        elif(await self.config.guild(interaction.guild).useGeneralLogChannel() and interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is None):
                            raise Exception("Kein gültiger genereller Channel definiert")
                    else:
                        await self.config.guild(interaction.guild).enableWarn.set(status)
                        Modsystem.remove_warn_points.cancel()
                        embedSuccess.add_field(name="Aktiviere Warn funktion", value=status)

                case "kLog":

                    if(status):
                        if(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is not None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                            await self.config.guild(interaction.guild).enableKickLog.set(status)
                            embedSuccess.add_field(name="Kick Log", value=status)
                        elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).kickLogChannel())) is not None and await self.config.guild(interaction.guild).useGeneralLogChannel() == False):
                            await self.config.guild(interaction.guild).enableKickLog.set(status)
                            embedSuccess.add_field(name="Client-Update Log", value=status)
                        elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                            raise Exception("Kein gültiger genereller Channel definiert")
                        elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).kickLogChannel())) is None):
                            raise Exception("Kein Gültiger Channel angegeben")
                    else:
                        await self.config.guild(interaction.guild).enableKickLog.set(status)
                        embedSuccess.add_field(name="Kick Log", value=status)

                case "bLog":

                    if(status):
                        if(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is not None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                            await self.config.guild(interaction.guild).enableBanLog.set(status)
                            embedSuccess.add_field(name="Ban Log", value=status)
                        elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).banLogChannel())) is not None and await self.config.guild(interaction.guild).useGeneralLogChannel() == False):
                            await self.config.guild(interaction.guild).enableBanLog.set(status)
                            embedSuccess.add_field(name="Ban Log", value=status)
                        elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                            raise Exception("Kein gültiger genereller Channel definiert")
                        elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).banLogChannel())) is None):
                            raise Exception("Kein Gültiger Channel angegeben")
                    else:
                        await self.config.guild(interaction.guild).enableBanLog.set(status)
                        embedSuccess.add_field(name="Ban Log", value=status)

                case "uLog":

                    if(status):
                        if(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is not None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                            await self.config.guild(interaction.guild).enableUpdateLog.set(status)
                            embedSuccess.add_field(name="Client-Update Log", value=status)
                        elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).updateLogChannel())) is not None and await self.config.guild(interaction.guild).useGeneralLogChannel() == False):
                            await self.config.guild(interaction.guild).enableUpdateLog.set(status)
                            embedSuccess.add_field(name="Client-Update Log", value=status)
                        elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                            raise Exception("Kein gültiger genereller Channel definiert")
                        elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).updateLogChannel())) is None):
                            raise Exception("Kein Gültiger Channel angegeben")
                    else:
                        await self.config.guild(interaction.guild).enableUpdateLog.set(status)
                        embedSuccess.add_field(name="Client-Update Log", value=status)

                case "jLog":

                    if(status):
                        if((interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is not None and await self.config.guild(interaction.guild).useGeneralLogChannel()) or (interaction.guild.get_channel(int(await self.config.guild(interaction.guild).joinLogChannel())) is not None and await self.config.guild(interaction.guild).useGeneralLogChannel() == False)):
                            await self.config.guild(interaction.guild).enableJoinLog.set(status)
                            for invite in await interaction.guild.invites():
                                if(invite.code in await self.config.guild(interaction.guild).invites()):
                                    await self.config.guild(interaction.guild).invites.set_raw(invite.code, value={'count': await self.config.guild(interaction.guild).invites.get_raw(invite.code, 'count'), 'uses': invite.uses})
                                else:
                                    await self.config.guild(interaction.guild).invites.set_raw(invite.code, value={'count': 0, 'uses': invite.uses})
                            embedSuccess.add_field(name="Join Log", value=status)
                        elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                            raise Exception("Kein gültiger genereller Channel definiert")
                        elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).joinLogChannel())) is None):
                            raise Exception("Kein Gültiger Channel angegeben")
                    else:
                        await self.config.guild(interaction.guild).enableJoinLog.set(status)
                        embedSuccess.add_field(name="Join Log", value=status)

                case "mLog":

                    if(status):
                        if(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is not None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                            await self.config.guild(interaction.guild).enableDeleteMessageLog.set(status)
                            embedSuccess.add_field(name="DeleteMessageLog", value=status)
                        elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).deleteMessageLogChannel())) is not None and await self.config.guild(interaction.guild).useGeneralLogChannel() == False):
                            await self.config.guild(interaction.guild).enableDeleteMessageLog.set(status)
                            embedSuccess.add_field(name="Message Log", value=status)
                        elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                            raise Exception("Kein Gültiger genereller Channel definiert")
                        elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).deleteMessageLogChannel())) is None):
                            raise Exception("Kein Gültiger Channel angegeben")
                    else:
                        await self.config.guild(interaction.guild).enableDeleteMessageLog.set(status)
                        embedSuccess.add_field(name="DeleteMessageLog", value=status)

                case "vLog":

                    await self.config.guild(interaction.guild).enableVoiceLog.set(status)
                    embedSuccess.add_field(name="Voice Log", value=status)

                case "mLinks":

                    await self.config.guild(interaction.guild).deleteLinks.set(status)
                    embedSuccess.add_field(name="Message Link Detection", value=status)

                case "sdPics":

                    await self.config.guild(interaction.guild).saveDeletedPics.set(status)
                    embedSuccess.add_field(name="Speichere gelöschte Bilder lokal", value=status)

            await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()

        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    @modsystem.command(name="setupwarn", description="Das setup der Warn-Funktion")
    @app_commands.describe(choice="Der Wert der gesetzt werden soll", wert="Der Wert der Punkte oder Zeitangabe in Minuten", activate="Aktivieren oder Deaktivieren")
    @app_commands.choices(choice=[
        app_commands.Choice(name="Die Basiswarnpunkte welche bei einem Warn vergeben werden", value="warnWeight"),
        app_commands.Choice(name="Die Punkteanzahl bei der der User gekickt werden soll", value="warnKickWeight"),
        app_commands.Choice(name="Die Punkteanzahl bei der der User gebannt werden soll", value="warnBanWeight"),
        app_commands.Choice(name="Dynamischen Reset der Punkte aktivieren", value="warnDynamicReset"),
        app_commands.Choice(name="Die Zeit für den Dynamischen Reset", value="warnDynamicResetTime"),
        app_commands.Choice(name="Die Anzahl der Punkte welche bei dem Dynamischen Reset abgezogen werden sollen", value="warnDynamicResetCount"),
        app_commands.Choice(name="Die  Zeit nach der die Warnpunkte zurückgesetzt werden sollen", value="warnResetTime"),
        app_commands.Choice(name="Nutze DM um dem User den Warn mitzuteilen", value="warnUseDM"),
        app_commands.Choice(name="Nutze öffentlichen Channel", value="warnUseChannel"),
        app_commands.Choice(name="Multiplikator der 1. Stufe", value="warnFirstMultiplicator"),
        app_commands.Choice(name="Multiplikator der 2. Stufe", value="warnSecondMultiplicator"),
        app_commands.Choice(name="Multiplikator der 3. Stufe", value="warnThirdMultiplicator")
    ])
    @app_commands.checks.has_permissions(administrator=True)
    async def setupwarn(self, interaction: discord.Interaction, choice: app_commands.Choice[str], wert: str = None, activate: bool = None):
        try:

            match choice.value:

                case "warnWeight":

                    if(wert == None):
                        raise Exception("Bitte den wert festlegen")
                    await self.config.guild(interaction.guild).warnWeight.set(int(wert))
                    embedSuccess.add_field(name="Warnpunkte", value=int(wert))

                case "warnKickWeight":

                    if(wert == None):
                        raise Exception("Bitte den wert festlegen")
                    await self.config.guild(interaction.guild).warnKickWeight.set(int(wert))
                    embedSuccess.add_field(name="Kickschwelle", value=int(wert))

                case "warnBanWeight":

                    if(wert == None):
                        raise Exception("Bitte den wert festlegen")
                    await self.config.guild(interaction.guild).warnBanWeight.set(int(wert))
                    embedSuccess.add_field(name="Banschwelle", value=int(wert))

                case "warnDynamicReset":

                    if(activate == None):
                        raise Exception("Bitte activate festlegen")
                    if(activate):
                        Modsystem.remove_warn_points.change_interval(minutes=await self.config.guild(interaction.guild).warnDynamicResetTime())
                    else:
                        Modsystem.remove_warn_points.change_interval(minutes=await self.config.guild(interaction.guild).warnResetTime())
                    await self.config.guild(interaction.guild).warnDynamicReset.set(activate)
                    embedSuccess.add_field(name="Dynamischer Reset", value=activate)

                case "warnDynamicResetTime":

                    if(wert == None):
                        raise Exception("Bitte den wert festlegen")
                    if(await self.config.guild(interaction.guild).warnDynamicReset() and await self.config.guild(interaction.guild).enableWarn()):
                        Modsystem.remove_warn_points.change_interval(minutes=int(wert))
                        print(f"Dynamischer Punkteabbau auf {wert} Minuten gesetzt")
                    await self.config.guild(interaction.guild).warnDynamicResetTime.set(int(wert))
                    embedSuccess.add_field(name="Dynamische reset Zeit", value=int(wert))

                case "warnDynamicResetCount":

                    if(wert == None):
                        raise Exception("Bitte den wert festlegen")
                    await self.config.guild(interaction.guild).warnDynamicResetCount.set(int(wert))
                    embedSuccess.add_field(name="Dynamische reset Punkte", value=int(wert))

                case "warnResetTime":

                    if(wert == None):
                        raise Exception("Bitte den wert festlegen")
                    if(await self.config.guild(interaction.guild).warnDynamicReset() == False and await self.config.guild(interaction.guild).enableWarn()):
                        Modsystem.remove_warn_points.change_interval(minutes=int(wert))
                    await self.config.guild(interaction.guild).warnResetTime.set(int(wert))
                    embedSuccess.add_field(name="Resettime", value=int(wert))

                case "warnUseDM":

                    if(activate == None):
                        raise Exception("Bitte activate festlegen")
                    await self.config.guild(interaction.guild).warnUseDM.set(activate)
                    embedSuccess.add_field(name="DM User bei Verwarnung", value=activate)

                case "warnUseChannel":

                    if(activate == None):
                        raise Exception("Bitte activate festlegen")
                    if(activate):
                        if(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).warnPublicChannel()))):
                            await self.config.guild(interaction.guild).warnUsePublicChannel.set(activate)
                            embedSuccess.add_field(name="Es wurde folgender Wert gesetzt:", value=activate)
                        else:
                            raise Exception("Kein gültiger Channel festgelegt")
                    else:
                        await self.config.guild(interaction.guild).warnUseChannel.set(activate)
                        embedSuccess.add_field(name="Nutze Warnchannel", value=activate)
                    
                case "warnFirstMultiplicator":

                    if(wert == None):
                        raise Exception("Bitte einen Wert setzten")
                    await self.config.guild(interaction.guild).warnFirstMultiplicator.set(float(wert.replace(",", ".")))
                    embedSuccess.add_field(name="Multiplikator 1. Stufe", value=float(wert.replace(",", ".")))

                case "warnSecondMultiplicator":

                    if(wert == None):
                        raise Exception("Bitte einen Wert setzten")
                    await self.config.guild(interaction.guild).warnSecondMultiplicator.set(float(wert.replace(",", ".")))
                    embedSuccess.add_field(name="Multiplikator 2. Stufe", value=float(wert.replace(",", ".")))

                case "warnThirdMultiplicator":

                    if(wert == None):
                        raise Exception("Bitte einen Wert setzten")
                    await self.config.guild(interaction.guild).warnThirdMultiplicator.set(float(wert.replace(",", ".")))
                    embedSuccess.add_field(name="Multiplikator 3. Stufe", value=float(wert.replace(",", ".")))

            await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()

        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    @modsystem.command(name="setmodrole", description="Lege die Modrolle fest")
    @app_commands.checks.has_permissions(administrator=True)
    async def setmodrole(self, interaction: discord.Interaction, role: discord.Role):
        try:
            if(interaction.guild.get_role(role.id)):
                await self.config.guild(interaction.guild).modRole.set(role.id)
                embedSuccess.add_field(name="Modrolle", value=role)
                await interaction.response.send_message(embed=embedSuccess)
            else:
                raise Exception("Angegebene Rolle nicht gültig")
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="getconfig", description="Schau dir die aktuelle Config an")
    @app_commands.checks.has_permissions(administrator=True)
    async def showconfig(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(color=0x0ffc03)
            embed.description=(f"# Config\n"
                               f"### Channel:\n"
                               f"Gneral Log-Channel: <#{await self.config.guild(interaction.guild).generalLogChannel()}>\n"
                               f"Warn Log-Channel: <#{await self.config.guild(interaction.guild).warnLogChannel()}>\n"
                               f"Warn Public Channel: <#{await self.config.guild(interaction.guild).warnPublicChannel()}>\n"
                               f"Kick Log-Channel: <#{await self.config.guild(interaction.guild).kickLogChannel()}>\n"
                               f"Ban Log-Channel: <#{await self.config.guild(interaction.guild).banLogChannel()}>\n"
                               f"Update Log-Channel: <#{await self.config.guild(interaction.guild).updateLogChannel()}>\n"
                               f"Join Log-Channel: <#{await self.config.guild(interaction.guild).joinLogChannel()}>\n"
                               f"Delete Message Log-Channel: <#{await self.config.guild(interaction.guild).deleteMessageLogChannel()}>\n"
                               f"Softban Channel: <#{await self.config.guild(interaction.guild).softBanChannel()}>\n"
                               f"Softban Log-Channel: <#{await self.config.guild(interaction.guild).softBanLogChannel()}>\n"
                               f"### Status:\n"
                               f"Warn funktion  aktiviert: **{await self.config.guild(interaction.guild).enableWarn()}**\n"
                               f"Kick-Log: **{await self.config.guild(interaction.guild).enableKickLog()}**\n"
                               f"Ban-Log: **{await self.config.guild(interaction.guild).enableBanLog()}**\n"
                               f"Update-Log: **{await self.config.guild(interaction.guild).enableUpdateLog()}**\n"
                               f"Join-Log: **{await self.config.guild(interaction.guild).enableJoinLog()}**\n"
                               f"Delete  Message-Log: **{await self.config.guild(interaction.guild).enableDeleteMessageLog()}**\n"
                               f"Voice-Log: **{await self.config.guild(interaction.guild).enableVoiceLog()}**\n"
                               f"Verhindere Links: **{await self.config.guild(interaction.guild).deleteLinks()}**\n"
                               f"Speichere gelöschte Bilder: **{await self.config.guild(interaction.guild).saveDeletedPics()}**\n"
                               f"### Warn:\n"
                               f"Warnpunke pro Warn: **{await self.config.guild(interaction.guild).warnWeight()}**\n"
                               f"Nötige Punkte zum Kicken: **{await self.config.guild(interaction.guild).warnKickWeight()}**\n"
                               f"Nötige Punkte zum Bannen: **{await self.config.guild(interaction.guild).warnBanWeight()}**\n"
                               f"Dynamischer Punkteabbau: **{await self.config.guild(interaction.guild).warnDynamicReset()}**\n"
                               f"Dynamischer Punkteabbau Intervall: **{await self.config.guild(interaction.guild).warnDynamicResetTime()}**\n"
                               f"Dynamischer Punkteabbau Punkte: **{await self.config.guild(interaction.guild).warnDynamicResetCount()}**\n"
                               f"Statischer Punkteabbau Intervall: **{await self.config.guild(interaction.guild).warnResetTime()}**\n"
                               f"Nutze Channel für die Verwarnungen: **{await self.config.guild(interaction.guild).warnUseChannel()}**\n"
                               f"Nutze DM für die Verwarnungen: **{await self.config.guild(interaction.guild).warnUseDM()}**\n"
                               f"Stufe 1 Multiplikator: **{await self.config.guild(interaction.guild).warnFirstMultiplicator()}**\n"
                               f"Stufe 2 Multiplikator: **{await self.config.guild(interaction.guild).warnSecondMultiplicator()}**\n"
                               f"Stufe 3 Multiplikator: **{await self.config.guild(interaction.guild).warnThirdMultiplicator()}**\n"
                               f"### General:\n"
                               f"Nutze den generellen Log-Channel: **{await self.config.guild(interaction.guild).useGeneralLogChannel()}**\n"
                               f"### Misc:\n")
            if(interaction.guild.get_role(await self.config.guild(interaction.guild).modRole())):
                embed.description += (f"Modrolle: {interaction.guild.get_role(await self.config.guild(interaction.guild).modRole()).mention}\n")
            else:
                embed.description += (f"Modrolle: **Keine gültige Rolle gesetzt**\n")
            embed.description += (f"Link detection pattern: **{await self.config.guild(interaction.guild).linkPattern()}**\n")
            await interaction.response.send_message(embed=embed)
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    @modsystem.command(name="updateinvitecodes", description="Update die gespeicherten Invite-Codes")
    @app_commands.checks.has_permissions(administrator=True)
    async def updateinvitecodes(self, interaction: discord.Interaction):
        try:
            for invite in await interaction.guild.invites():
                if(await self.config.guild(interaction.guild).invites.get_raw(invite.code) is None):
                    await self.config.guild(interaction.guild).invites.set_raw(invite.code, value={'count': 0, 'uses': invite.uses})
                else:
                    await self.config.guild(interaction.guild).invites.set_raw(invite.code, value={'count': await self.config.guild(interaction.guild).invites.get_raw(invite.code, 'count'), 'uses': invite.uses})
            embedSuccess.add_field(name="Update der Invite-Codes", value="Erfolgreich")
            await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    @app_commands.command(name="warn", description="Verwarne User")
    @app_commands.choices(stufe=([
        app_commands.Choice(name="Leicht", value=1),
        app_commands.Choice(name="Mittel", value=2),
        app_commands.Choice(name="Schwer", value=3)
    ]))
    @app_commands.describe(user="Der User der verwarnt werden soll", reason="Grund der Verwarnung", stufe="Die Schwere der Verwarnung (Optional)", timeout="Die länge des Timeout in Minuten (Optional)")
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str, stufe: app_commands.Choice[int] = 0, timeout: app_commands.Range[int, 1, 40320] = 0):
        try:
            await interaction.response.defer(ephemeral=True)
            if(await self.config.guild(interaction.guild).enableWarn() == False):
                raise Exception("Die Funktion ist momentan nicht aktiviert")
            if(interaction.user.top_role.position < interaction.guild.get_role(await self.config.guild(interaction.guild).modRole()).position):
                raise Exception("Keine Berechtigung diesen Befehl zu nutzen")
            if(interaction.user.top_role.position <= user.top_role.position):
                raise Exception("Du kannst keine Leute verwarnen die einen höheren oder gleichwertigen Rang haben wie du")
            if(user.bot):
                raise Exception("Du kannst keinen Bot verwarnen")
            if(await self.config.guild(interaction.guild).users.get_raw(user.id, 'banned')):
                raise Exception("Warn nicht möglich da der User bereits gebannt ist")
            if(await self.config.guild(interaction.guild).users.get_raw(user.id, 'softBanned')):
                raise Exception("Warn nicht möglich da der User im Softban ist")
            embedResponse = discord.Embed(title="Aktion Erfolgreich", color=0x0ffc03)
            embedPublic = discord.Embed(color=0xfc7f03)
            embedDM = discord.Embed(title=f"{interaction.guild.name}'s Warnsystem", color=0xff0000)
            sendPChannel = False
            sendDMChannel = False
            if(await self.config.guild(interaction.guild).warnUseChannel()):
                sendPChannel = True
            if(await self.config.guild(interaction.guild).warnUseDM()):
                sendDMChannel = True
            userAction = "none"
            currentTime = datetime.now().astimezone(tz=None).strftime('%d-%m-%Y um %H:%M')
            if(await self.config.guild(interaction.guild).users.get_raw(user.id, 'firstWarn') == ""):
                await self.config.guild(interaction.guild).users.set_raw(user.id, 'firstWarn', value=currentTime)
            if(stufe != 0):
                match stufe.value:
                    case 1:
                        multiplikator = await self.config.guild(interaction.guild).warnFirstMultiplicator()
                    case 2:
                        multiplikator = await self.config.guild(interaction.guild).warnSecondMultiplicator()
                    case 3:
                        multiplikator = await self.config.guild(interaction.guild).warnThirdMultiplicator()
                await self.config.guild(interaction.guild).users.set_raw(user.id, value={'displayName': user.display_name,
                                                                                         'username': user.name,
                                                                                         'currentReason': reason,
                                                                                         'currentPoints': await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints') + round(await self.config.guild(interaction.guild).warnWeight() * multiplikator),
                                                                                         'totalPoints': await self.config.guild(interaction.guild).users.get_raw(user.id, 'totalPoints') + round(await self.config.guild(interaction.guild).warnWeight() * multiplikator),
                                                                                         'firstWarn': await self.config.guild(interaction.guild).users.get_raw(user.id, 'firstWarn'),
                                                                                         'lastWarn': currentTime,
                                                                                         'warnCount': await self.config.guild(interaction.guild).users.get_raw(user.id, 'warnCount') + 1,
                                                                                         'kickCount': 0,
                                                                                         'softBanned': False,
                                                                                         'banned': False})
                if(await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints') >= await self.config.guild(interaction.guild).warnKickWeight()):
                    userAction = "kick"
                elif(await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints') >= await self.config.guild(interaction.guild).warnBanWeight()):
                    userAction = "ban"
            else:
                currentPoints = await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints') + await self.config.guild(interaction.guild).warnWeight()
                totalPoints = await self.config.guild(interaction.guild).users.get_raw(user.id, 'totalPoints') + await self.config.guild(interaction.guild).warnWeight()
                await self.config.guild(interaction.guild).users.set_raw(user.id, value={'displayName': user.display_name,
                                                                                                         'username': user.name,
                                                                                                         'currentReason': reason,
                                                                                                         'currentPoints': currentPoints,
                                                                                                         'totalPoints': totalPoints,
                                                                                                         'firstWarn': await self.config.guild(interaction.guild).users.get_raw(user.id, 'firstWarn'),
                                                                                                         'lastWarn': currentTime,
                                                                                                         'warnCount': await self.config.guild(interaction.guild).users.get_raw(user.id, 'warnCount') + 1,
                                                                                                         'kickCount': await self.config.guild(interaction.guild).users.get_raw(user.id, 'kickCount'),
                                                                                                         'softBanned': await self.config.guild(interaction.guild).users.get_raw(user.id, 'softBanned'),
                                                                                                         'banned': False})
                if(await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints') >= await self.config.guild(interaction.guild).warnKickWeight()):
                    userAction = "kick"
                elif(await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints') >= await self.config.guild(interaction.guild).warnBanWeight()):
                    userAction = "ban"
            match userAction:
                case "none":
                    embedResponse.description=(f"{user.mention} wurde erfolgreich verwarnt\n\n"
                                               f"Begründung: **{reason}**\n"
                                               f"Timeout: **{timeout} Minuten**\n"
                                               f"Aktuelle Punkte: **{await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints')}**\n"
                                               f"Fehlende Punkte bis zum Kick: **{await self.config.guild(interaction.guild).warnKickWeight() - await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints')}**\n"
                                               f"Fehlende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints')}**\n")
                    embedLog.description=(f"{user.mention} wurde von {interaction.user.mention} verwarnt\n\n"
                                          f"Begründung: **{reason}**\n"
                                          f"Timeout: **{timeout} Minuten**\n"
                                          f"Aktuelle Punkte: **{await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints')}**\n"
                                          f"Fehlende Punkte bis zum Kick: **{await self.config.guild(interaction.guild).warnKickWeight() - await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints')}**\n"
                                          f"Fehlende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints')}**\n")
                    embedPublic.description=(f"## Verwarnung\n"
                                             f"{user.mention} **wurde verwarnt**\n"
                                             f"### Begründung:\n"
                                             f"**{reason}**")
                    embedDM.description=(f"Du wurdest gerade von **{interaction.user.display_name}** verwarnt\n\n"
                                         f"Begründung: **{reason}**\n"
                                         f"Timeout: **{timeout} Minuten**\n"
                                         f"Punkte: **{await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints')}**\n"
                                         f"Verbleibende Punkte bis zum Kick: **{await self.config.guild(interaction.guild).warnKickWeight() - await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints')}**\n"
                                         f"Verbleibende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints')}**")
                    if timeout != 0:
                        timeou_until = datetime.now().astimezone() + timedelta(minutes=timeout)
                        await user.timeout(timeou_until, reason=reason)
                case "kick":
                    await user.kick(reason=reason)
                    embedResponse.description=(f"{user.mention} wurde mit der Begründung **{reason}** gekickt\n\n"
                                               f"Aktuelle Punkte: **{await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints')}**\n"
                                               f"Kickgrenze: **{await self.config.guild(interaction.guild).warnKickWeight()}**\n"
                                               f"Fehlende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - currentPoints}**\n")
                    embedLog.description=(f"{user.mention} wurde mit der Begründung **{reason}** gekickt\n\n"
                                          f"Aktuelle Punkte: **{await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints')}**\n"
                                          f"Kickgrenze: **{await self.config.guild(interaction.guild).warnKickWeight()}**\n"
                                          f"Fehlende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - currentPoints}**\n")
                    embedPublic.description=(f"## Verwarnung\n"
                                             f"{user.mention} wurde wegen zu vielen Verwarnungen gekickt\n"
                                             f"### Begründung:\n"
                                             f"**{reason}**")
                    embedDM.description=(f"Du wurdest gerade von {interaction.user.display_name} mit der Begründung **{reason}** vom Server gekickt\n\n"
                                         f"Punkte: **{await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints')}**\n"
                                         f"Dies ist dein **{await self.config.guild(interaction.guild).users.get_raw(user.id, 'kickCount')}.** Kick\n"
                                         f"Verbleibende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints')}**\n")
                case "ban":
                    await user.ban(reason=reason, delete_message_days=1)
                    embedResponse.description=(f"{user.mention} wurde mit der Begründung **{reason}** gebannt\n\n"
                                               f"Aktuelle Punkte: **{await self.config.guild(interaction.guild).users.get_raw(user.id, 'currentPoints')}**\n"
                                               f"Anzahl der Kicks: **{await self.config.guild(interaction.guild).users.get_raw(user.id, 'kickCount')}**\n"
                                               f"Bangrenze: **{await self.config.guild(interaction.guild).warnBanWeight()}**")
                    embedLog.description=embedResponse.description
                    embedPublic.description=(f"## Verwarnung\n"
                                             f"{user.mention} wurde wegen zu vielen Verwarnungen gebannt\n"
                                             f"### Begrpndung\n"
                                             f"**{reason}**")
                    embedDM.description=(f"Du wurdest gerade von {interaction.user.display_name} mit der Begründung **{reason}** gebant\n\n")
                        
            if(sendPChannel):
                await interaction.guild.get_channel(int(await self.config.guild(interaction.guild).warnPublicChannel())).send(embed=embedPublic)

            if(sendDMChannel):
                await user.send(embed=embedDM)
                
            if user.avatar is not None:
                embedLog.set_thumbnail(url=user.avatar.url)
            await interaction.guild.get_channel(int(await self.config.guild(interaction.guild).warnLogChannel())).send(embed=embedLog)
            embedLog.set_thumbnail(url=None)
            await interaction.followup.send(embed=embedResponse, ephemeral=True)

        except Exception as error:

            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.followup.send(embed=embedFailure, ephemeral=True)

    @modsystem.command(name="setwarnpoints", description="Setze die Warnpoints für einen User")
    @app_commands.describe(user="User", points="Warnpoints")
    @app_commands.checks.has_permissions(administrator=True)
    async def setwarnpoints(self, interaction: discord.Interaction, user: discord.User, points: int):
        try:
            if(dict(await self.config.guild(interaction.guild).users()).get(str(user.id)) is not None):
                await self.config.guild(interaction.guild).users.set_raw(user.id, 'currentPoints', value=points)
                embedSuccess.add_field(name="CurrentPoints", value=points)
                await interaction.response.send_message(embed=embedSuccess)
                embedSuccess.clear_fields()
            else:
                embed = discord.Embed(title="User nicht in der Datenbank", description=f"{user.mention} **wurde noch nicht verwarnt**", color=0xfc7f03)
                embed.set_thumbnail(url=user.display_avatar.url)
                await interaction.response.send_message(embed=embed)
                embedFailure.set_thumbnail(url=None)
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    @modsystem.command(name="showuserstats", description="Zeigt die aktuellen Daten für einen User oder dich selbst an")
    @app_commands.describe(user="User")
    async def showuserstats(self, interaction: discord.Interaction, user: discord.User = None):
        try:
            await interaction.response.defer(ephemeral=True)
            if(interaction.user.top_role.position < interaction.guild.get_role(await self.config.guild(interaction.guild).modRole()).position):
                if(interaction.user != user):
                    if(user is not None):
                        raise Exception("Du darfst dir nur deine Eigenen Daten anschauen")
            embed = discord.Embed(title=f"Hier sind die aktuellen Daten", color=0xfc7f03)
            if(user is None):
                if(dict(await self.config.guild(interaction.guild).users()).get(str(interaction.user.id)) is not None):
                    currentUserRecord = await self.config.guild(interaction.guild).users.get_raw(interaction.user.id)
                    ban = "Ja" if currentUserRecord.get("banned") == True else "Nein"
                    embed.description=(f"**Es ist aktuell folgendes von {interaction.user.mention} gespeichert:**\n\n"
                                       f"Begründung des letzten Warns: **{currentUserRecord.get('currentReason')}**\n"
                                       f"Aktuelle Punkte: **{currentUserRecord.get('currentPoints')}**\n"
                                       f"Alle jemals erhaltene Punkte: **{currentUserRecord.get('totalPoints')}**\n"
                                       f"Erster Warn am **{currentUserRecord.get('firstWarn')}** erhalten\n"
                                       f"Letzter Warn am **{currentUserRecord.get('lastWarn')}** erhalten\n"
                                       f"Anzahl an Kicks durch Warns: **{currentUserRecord.get('kickCount')}**\n"
                                       f"User gebannt: **{ban}**")
                    embed.set_thumbnail(url=interaction.user.display_avatar.url)
                else:
                    embed.description=f"**Es liegen aktuell keine Daten zu {interaction.user.mention} vor**"
                    embed.set_thumbnail(url=interaction.user.display_avatar.url)
            else:
                if(dict(await self.config.guild(interaction.guild).users()).get(str(user.id)) is not None):
                    currentUserRecord = await self.config.guild(interaction.guild).users.get_raw(user.id)
                    ban = "Ja" if currentUserRecord.get("banned") == True else "Nein"
                    embed.description=(f"**Es ist aktuell folgendes von {user.mention} gespeichert:**\n\n"
                                    f"Begründung des letzten Warns: **{currentUserRecord.get('currentReason')}**\n"
                                    f"Aktuelle Punkte: **{currentUserRecord.get('currentPoints')}**\n"
                                    f"Alle jemals erhaltene Punkte: **{currentUserRecord.get('totalPoints')}**\n"
                                    f"Erster Warn am **{currentUserRecord.get('firstWarn')}** erhalten\n"
                                    f"Letzter Warn am **{currentUserRecord.get('lastWarn')}** erhalten\n"
                                    f"Anzahl an Kicks durch Warns: **{currentUserRecord.get('kickCount')}**\n"
                                    f"User gebannt: **{ban}**")
                    embed.set_thumbnail(url=user.display_avatar.url)
                else:
                    embed.description=f"**Es liegen aktuell keine Daten zu {user.mention} vor**"
                    embed.set_thumbnail(url=user.display_avatar.url)
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.followup.send(embed=embedFailure, ephemeral=True)
            

    @modsystem.command(name="showwarnlist", description="Zeige eine List an mit allen Verwarnungen")
    async def showwarnlist(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True)
            if(interaction.user.top_role.position < interaction.guild.get_role(await self.config.guild(interaction.guild).modRole()).position):
                raise Exception("Du hast keine Berechtigungen diesen Befehl auszuführen")
            embed = discord.Embed(color=0xfc7f03)
            listString = "## Alle aktuellen Verwarnungen\n"
            embedList = []
            for index, userID in enumerate(dict(await self.config.guild(interaction.guild).users()), start=1):
                if(interaction.guild.get_member(int(userID)) is None):
                    listString += (f"{await self.config.guild(interaction.guild).users.get_raw(userID, 'displayName')}\n\n"
                               f"Username: **{await self.config.guild(interaction.guild).users.get_raw(userID, 'username')}**\n"
                               f"Aktuelle Points: **{await self.config.guild(interaction.guild).users.get_raw(userID, 'currentPoints')}**\n"
                               f"Gesamte Points: **{await self.config.guild(interaction.guild).users.get_raw(userID, 'totalPoints')}**\n"
                               f"Anzahl der Kicks: **{await self.config.guild(interaction.guild).users.get_raw(userID, 'kickCount')}**\n")
                else:
                    listString += (f"{interaction.guild.get_member(int(userID)).mention}\n\n"
                                f"Username: **{interaction.guild.get_member(int(userID)).name}**\n"
                                f"Aktuelle Points: **{await self.config.guild(interaction.guild).users.get_raw(userID, 'currentPoints')}**\n"
                                f"Gesamte Points: **{await self.config.guild(interaction.guild).users.get_raw(userID, 'totalPoints')}**\n"
                                f"Anzahl der Kicks: **{await self.config.guild(interaction.guild).users.get_raw(userID, 'kickCount')}**\n")
                if(await self.config.guild(interaction.guild).users.get_raw(userID, 'banned') == False):
                    listString += f"Verbleibende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - await self.config.guild(interaction.guild).users.get_raw(userID, 'currentPoints')}**\n\n\n"
                else:
                    listString += f"**User ist gebannt**\n\n\n"
                if index % 3 == 0:
                    embed.description=listString
                    listString = ""
                    embedList.append(embed.copy())
                    if index % 30 == 0:
                        await interaction.followup.send(embeds=embedList, ephemeral=True)
                        embedList.clear()
            embed.description = listString
            embedList.append(embed.copy())
            await interaction.followup.send(embeds=embedList, ephemeral=True)
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.followup.send(embed=embedFailure, ephemeral=True)

    # @app_commands.command(name="clearuserlist", description="Bereinige die Userliste")
    # @app_commands.checks.has_permissions(administrator=True)
    # async def clearuserlist(self, interaction: discord.Interaction):
    #     try:
            
    #     except Exception as error:
    #         embedFailure.description(f"**Es ist folgender Fehler aufgetreten:**\n\n{error}")

    @app_commands.command(name="softban", description="Softbanne einen User")
    @app_commands.describe(user="Der User der einen Softban bekommen soll")
    async def softban(self, interaction: discord.Interaction, user: discord.Member):
        try:
            await interaction.response.defer(ephemeral=True)
            if(interaction.user.top_role.position < interaction.guild.get_role(await self.config.guild(interaction.guild).modRole()).position):
                raise Exception("Du hast keine Berechtigung für diesen Befehl")
            elif(interaction.user.top_role.position <= user.top_role.position):
                raise Exception("Du kannst keinen User mit einem höheren oder gleichen Rang Softbannen")
            elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).softBanChannel())) is None):
                raise Exception("Kein gültiger Channel gesetzt")
            elif(await self.config.guild(interaction.guild).users.get_raw(user.id, 'softBanned')):
                raise Exception("Dieser User ist bereits im Softban")
            sbChannel = await self.config.guild(interaction.guild).softBanChannel()
            overwriteHide = discord.PermissionOverwrite()
            overwriteShow = discord.PermissionOverwrite()
            overwriteHide.view_channel=False
            overwriteShow.view_channel=True
            for channel in interaction.guild.channels:
                if(channel.id == sbChannel):
                    await channel.set_permissions(user, overwrite=overwriteShow)
                else:
                    await channel.set_permissions(user, overwrite=overwriteHide)
            await self.config.guild(interaction.guild).users.set_raw(user.id, 'softBanned', value=True)
            await user.send(f"Du hast einen Softban auf **{interaction.guild.name}** bekommen")
            embedLog.description=f"{user.mention} hat von {interaction.user.mention} einen **Softban** bekommen"
            if(await self.config.guild(interaction.guild).useGeneralLogChannel()):
                await interaction.guild.get_channel(await self.config.guild(interaction.guild).generalLogChannel()).send(embed=embedLog)
            else:
                await interaction.guild.get_channel(await self.config.guild(interaction.guild).softBanLogChannel()).send(embed=embedLog)
            embedLog.description=f"{user.mention} hat erfolgreich einen Softban erhalten"
            await interaction.followup.send(embed=embedLog)
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.followup.send(embed=embedFailure, ephemeral=True)

    @app_commands.command(name="revokesoftban", description="Nimmt den Softban wieder zurück")
    @app_commands.describe(user="Der User bei dem der Softban wieder zurück genommen werden soll")
    async def revokesoftban(self, interaction: discord.Interaction, user: discord.User):
        try:
            await interaction.response.defer(ephemeral=True)
            if(interaction.user.top_role.position < interaction.guild.get_role(await self.config.guild(interaction.guild).modRole()).position):
                raise Exception("Du hast keine Berechtigung für diesen Befehl")
            elif(interaction.user.top_role.position <= user.top_role.position):
                raise Exception("Du kannst keinen User mit einem höheren oder gleichen Rang Softbannen")
            elif(await self.config.guild(interaction.guild).users.get_raw(user.id, 'softBanned') == False):
                raise Exception("Dieser User hat aktuell keinen Softban")
            for channel in interaction.guild.channels:
                await channel.set_permissions(user, overwrite=None)
            await self.config.guild(interaction.guild).users.set_raw(user.id, 'softBanned', value=False)
            await user.send(f"Dein Softban auf **{interaction.guild.name}** wurde zurückgenommen")
            embedLog.description=f"Der **Softban** von {user.mention} wurde von {interaction.user.mention} aufgehoben"
            if(await self.config.guild(interaction.guild).useGeneralLogChannel()):
                await interaction.guild.get_channel(await self.config.guild(interaction.guild).generalLogChannel()).send(embed=embedLog)
            else:
                await interaction.guild.get_channel(await self.config.guild(interaction.guild).softBanLogChannel()).send(embed=embedLog)
            embedLog.description=f"Der Softban von {user.mention} wurde erfolgreich aufgehoben"
            await interaction.followup.send(embed=embedLog)
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.followup.send(embed=embedFailure, ephemeral=True)
            
    @app_commands.command()
    @app_commands.describe()
    @app_commands.checks.has_permissions(administrator=True)
    async def kick(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        try:
            if(interaction.user.top_role.position < interaction.guild.get_role(int(await self.config.guild(interaction.guild).modRole()))):
                user.kick(reason=reason)
                embedLog.description=f"Es wurde folgender User gebannt: {user.mention}"
                await interaction.response.send_message(embed=embedLog, ephemeral=True)
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)
            
    @app_commands.command()
    @app_commands.describe()
    @app_commands.checks.has_permissions(administrator=True)
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str):
        try:
            if(interaction.user.top_role.position <  interaction.guild.get_role(int(await self.config.guild(interaction.guild).modRole()))):
                raise Exception("Keine Berechtigung")
            user.ban(reason=reason, delete_message_days=1)
            embedLog.description=f"Es wurde folgender User gebannt: {user.mention}"
            await interaction.response.send_message(embed=embedLog, ephemeral=True)
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    @modsystem.command(name="inituser", description="Initialisiere alle fehlenden User")
    @app_commands.checks.has_permissions(administrator=True)
    async def inituser(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True)
            for user in interaction.guild.members:
                if(dict(await self.config.guild(interaction.guild).users()).get(str(user.id)) is None):
                    await Modsystem.init_user(self, user)
            embedLog.description=f"Es wurden alle Fehlenden User erfolgreich angelegt"
            await interaction.followup.send(embed=embedLog)
        except Exception as error:
            embedFailure.description(f"**Es ist folgender Fehler aufgetreten:**\n\n{error}")
            await interaction.followup.send(embed=embedFailure, ephemeral=True)

    @modsystem.command(name="help", description="Hilfe zu allen Commands")
    async def help(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(color=0xfc7f03)
            embed.description=(f"# Hilfemenü\n"
                                   f"### Generelle Befehle:\n"
                                   f"* **/modlog showwarnlist**\n"
                                   f" * Zeigt eine Liste mit allen Usern die eine Verwarnung haben\n"
                                   f"* **/modlog showuserstats**\n"
                                   f" * Zeigt deine aktuellen Warndaten an\n")
            if(interaction.user.top_role.position > interaction.guild.get_role(await self.config.guild(interaction.guild).modRole()).position):
                embed.description=(f"# Hilfemenü\n"
                                   f"### Generelle Befehle\n"
                                   f"* **/modlog showwarnlist**\n"
                                   f" * Zeigt eine Liste mit allen Usern die eine Verwarnung haben\n"
                                   f"* **/modlog showuserstats [user]**\n"
                                   f" * Zeigt deine aktuellen Warndaten an oder lass dir die von andern anzeigen\n"
                                   f"* **/warn <user> <reason> [stufe] [timeout]**\n"
                                   f" * Verwarne den angegebenen User, lege die Scwere fest und gebe ihm einen Timeout\n"
                                   f"* **/softban <user>**\n"
                                   f" * Erteile dem User einen Softban\n"
                                   f"* **/revokesoftban <user>**\n"
                                   f" * Nimm den Softban von dem User wieder zurück\n")
                if(app_commands.checks.has_permissions(administrator=True)):
                    embed.description += (f"### Setup\n"
                                    f"* **/modlog setupchannel <Modul> <ChannelID>**\n"
                                    f" * Setze die zu benutzenden Channel für das ausgewählte Modul\n"
                                    f"* **/modlog enable <Modul> <True/False>**\n"
                                    f" * Aktiviere oder deaktiviere das ausgewählte Modul\n"
                                    f"* **/modlog setupwarn <Setting> <bool/int>**\n"
                                    f" * Konfiguriere das Warn-Modul und setze die Werte für die entsprechenden Settings\n"
                                    f"### Misc\n"
                                    f"* **/modlog setwarnpoints <user> <points>**\n"
                                    f" * Setze für den Angegebenen User die aktuellen Warnpunkte\n"
                                    f"* **/modlog updateinvitecodes**\n"
                                    f" * Update die gespeicherten Invite-Codes falls es Probleme mit dem Joinlog gibt\n"
                                    f"* **/modlog getconfig**\n"
                                    f" * Zeige die Aktuelle Konfiguration\n"
                                    f"* **/modlog inituser**\n"
                                    f" * Initialisiere alle fehlenden User\n"
                                    f"* **/modloge setmodrole <role>**\n"
                                    f" * Setze die Modrolle")
            embed.set_footer(text=f"Das Serverteam von {interaction.guild.name}", icon_url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry):
        try:
            if(entry.action == discord.AuditLogAction.kick and await self.config.guild(entry.guild).enableKickLog()):
                if(await self.config.guild(entry.guild).useGeneralLogChannel()):
                    channel = entry.guild.get_channel(await self.config.guild(entry.guild).generalLogChannel())
                else:
                    channel = entry.guild.get_channel(await self.config.guild(entry.guild).kickLogChannel())
                if(entry.reason is not None):
                    embedLog.description=entry.target.mention + " wurde von " + entry.user.mention + " mit der Begründung **" + entry.reason + "** gekickt"
                else:
                    embedLog.description=entry.target.mention + " wurde von " + entry.user.mention + " ohne Angabe von Gründen gekickt"
                await channel.send(embed=embedLog)
            elif(entry.action == discord.AuditLogAction.ban and await self.config.guild(entry.guild).enableBanLog()):
                if(await self.config.guild(entry.guild).useGeneralLogChannel()):
                    channel = entry.guild.get_channel(await self.config.guild(entry.guild).generalLogChannel())
                else:
                    channel = entry.guild.get_channel(await self.config.guild(entry.guild).banLogChannel())
                if(entry.reason is not None):
                    embedLog.description=entry.target.mention + " wurde von " + entry.user.mention + " mit der Begründung **" + entry.reason + "** gebant"
                else:
                    embedLog.description=entry.target.mention + " wurde von " + entry.user.mention + " ohne Angabe von Gründen gebant"
                await channel.send(embed=embedLog)
            elif(entry.action == discord.AuditLogAction.member_update and await self.config.guild(entry.guild).enableUpdateLog()):
                if(await self.config.guild(entry.guild).useGeneralLogChannel()):
                    channel = entry.guild.get_channel(await self.config.guild(entry.guild).generalLogChannel())
                else:
                    channel = entry.guild.get_channel(await self.config.guild(entry.guild).updateLogChannel())
                if(entry.after.timed_out_until is not None):
                    timeout_time = str(timedelta(seconds=round((entry.after.timed_out_until - datetime.now(entry.after.timed_out_until.tzinfo)).total_seconds())))
                    if(entry.reason is not None):
                        embedLog.description=entry.target.mention + " hat von " + entry.user.mention + " einen Timeout für **" + timeout_time + "** mit der Begründung **" + entry.reason + "** bekommen"
                    else:
                        embedLog.description=entry.target.mention + " hat von " + entry.user.mention + " ohne Angabe von Gründen einen Timeout für **" + timeout_time + "** bekommen"
                    await channel.send(embed=embedLog)
                elif(entry.after.timed_out_until is None):
                    timeout_time = str(timedelta(seconds=round((entry.before.timed_out_until - datetime.now(entry.before.timed_out_until.tzinfo)).total_seconds())))
                    embedLog.description=entry.user.mention + " hat den Timeout von " + entry.target.mention + "aufgehoben"
                    embedLog.add_field(name="Verbleibende Zeit", value=timeout_time, inline=True)
                    await channel.send(embed=embedLog)
                    embedLog.clear_fields()
        except Exception as error:
            print("Fehler im Auditlog: " + str(error))
    
    async def get_invite_with_code(invite_list, code):
        for inv in invite_list:
            if inv.code == code:
                return inv
            
    async def init_user(self, member):
        await self.config.guild(member.guild).users.set_raw(member.id, value={'displayName': member.display_name,
                                                                                  'username': member.name,
                                                                                  'currentReason': "",
                                                                                  'currentPoints': 0,
                                                                                  'totalPoints': 0,
                                                                                  'firstWarn': "",
                                                                                  'lastWarn': "",
                                                                                  'warnCount': 0,
                                                                                  'kickCount': 0,
                                                                                  'softBanned': False,
                                                                                  'banned': False})
        
    async def clear_user(self, member):
        data = await self.config.guild(member.guild).users.get_raw(member.id)
        timeDiff = datetime.now() - member.joined_at.replace(tzinfo=None)
        oneDay = timedelta(days=1)
        if(data.get('warnCount') == 0 and data.get('kickCount') == 0 and data.get('softBanned') == False and data.get('banned') == False and timeDiff <= oneDay ):
            await self.config.guild(member.guild).users.clear_raw(member.id)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            await Modsystem.init_user(self, member)
            if(await self.config.guild(member.guild).enableJoinLog()):
                if(await self.config.guild(member.guild).useGeneralLogChannel() == True):
                    channel = member.guild.get_channel(await self.config.guild(member.guild).generalLogChannel())
                else:
                    channel = member.guild.get_channel(await self.config.guild(member.guild).joinLogChannel())
                invites_after = await member.guild.invites()
                usedInvite: discord.invite
                for invite in await self.config.guild(member.guild).invites():
                    result = await Modsystem.get_invite_with_code(invites_after, invite)
                    if(result is None):
                        await self.config.guild(member.guild).invites.clear_raw(invite)
                    else:
                        if(await self.config.guild(member.guild).invites.get_raw(invite, 'uses') < result.uses):
                            usedInvite = result
                            usedInviteInfo = await self.bot.fetch_invite(result.code)
                            break
                await self.config.guild(member.guild).invites.set_raw(usedInvite.code, value={'count': await self.config.guild(member.guild).invites.get_raw(usedInvite.code, 'count') + 1, 'uses': await self.config.guild(member.guild).invites.get_raw(usedInvite.code, 'uses') + 1})
                await self.config.guild(member.guild).invites.set_raw(member.id, value={'invitecode': usedInvite.code})
                embedLog.set_thumbnail(url=member.display_avatar.url)
                embedString=(f"Der Account {member.mention} wurde am **{(member.created_at).strftime('%d-%m-%Y')}** um **{(member.created_at).strftime('%H:%M')} Uhr** erstellt und ist mit dem Invite-Code **{usedInvite.code}** von {usedInvite.inviter.mention} beigetreten\n\n"
                             f"Informationen zu dem Invite:\n"
                             f"* Benutzungen: **{usedInvite.uses}**\n"
                             f"* Channel: {usedInvite.channel.mention}\n"
                             f"* Geblieben: **{await self.config.guild(member.guild).invites.get_raw(usedInvite.code, 'count')}**\n"
                             f"* Mitglieder: **{usedInviteInfo.approximate_member_count}**\n"
                             f"* Zurzeit aktiv: **{usedInviteInfo.approximate_presence_count}**\n"
                             f"* Läuft ab am: ")
                if(usedInvite.expires_at is None):
                    embedString += "**Niemals**\n"
                else:
                    embedString += f"**{(usedInvite.expires_at).strftime('%d-%m-%Y')}** um **{(usedInvite.expires_at).strftime('%H:%M')} Uhr**\n"
                embedString += f"* Link: **[Join]({usedInvite.url})**"
                embedLog.description=embedString
                await channel.send(embed=embedLog)
                embedLog.set_thumbnail(url=None)
        except Exception as error:
            print("Fehler bei Member-Join: " + str(error))

    @commands.Cog.listener()
    async def on_raw_member_remove(self, data):
        try:
            inviteCode = await self.config.guild(data.user.guild).invites.get_raw(data.user.id, 'invitecode')
            await self.config.guild(data.user.guild).invites.clear_raw(data.user.id)
            await self.config.guild(data.user.guild).invites.set_raw(inviteCode, value={'count': await self.config.guild(data.user.guild).invites.get_raw(inviteCode, 'count') - 1, 'uses': await self.config.guild(data.user.guild).invites.get_raw(inviteCode, 'uses')})
            await Modsystem.clear_user(self, data.user)
        except Exception as error:
            print("Fehler bei Member-Remove: " + str(error))

    @commands.Cog.listener()
    async def on_raw_message_delete(self, data):
        try:
            if(await self.config.guild(self.bot.get_guild(data.guild_id)).enableDeleteMessageLog()):
                if(await self.config.guild(self.bot.get_guild(data.guild_id)).useGeneralLogChannel() == True):
                    channel = self.bot.get_guild(data.guild_id).get_channel(await self.config.guild(self.bot.get_guild(data.guild_id)).generalLogChannel())
                else:
                    channel = self.bot.get_guild(data.guild_id).get_channel(await self.config.guild(self.bot.get_guild(data.guild_id)).updateLogChannel())
                async for entry in self.bot.get_guild(data.guild_id).audit_logs(action=discord.AuditLogAction.message_delete, limit=1):
                    global message_entry
                    message_entry = entry
                if(message_entry):
                    if(message_entry.created_at < data.cached_message.created_at):
                        message_entry.created_at = datetime.now()
                        message_entry.user = data.cached_message.author
                else:
                    message_entry.created_at = datetime.now()
                    message_entry.user = data.cached_message.author
                if(data.cached_message.attachments == [] and data.cached_message.embeds == []):
                    ownSticker = False
                    if(data.cached_message.stickers):
                        embedString=f"**Folgender Sticker wurde aus <#{data.channel_id}> gelöscht**\n\n"
                        for sticker in data.cached_message.stickers:
                            for gsticker in self.bot.get_guild(data.guild_id).stickers:
                                if sticker.id == gsticker.id:
                                    ownSticker = True
                                    break
                        if(ownSticker == False):
                            embedString += f"{data.cached_message.stickers}\n\n"
                    else:
                        embedString=(f"**Folgende Nachricht wurde aus <#{data.channel_id}> gelöscht**\n\n"
                                     f"{data.cached_message.content}\n\n")
                    if(data.cached_message.reference):
                        message_text = data.cached_message.reference.cached_message.content
                        message_text = message_text.replace('\n', '\n> ')
                        embedString += (f"**Bezieht sich auf:** {data.cached_message.reference.jump_url}\n\n"
                                        f"> {message_text}\n\n"
                                        f"*Geschrieben von* {data.cached_message.reference.cached_message.author.mention}\n\n")
                    embedString +=(f"Geschrieben von {data.cached_message.author.mention} am **{(data.cached_message.created_at).strftime('%d-%m-%Y')}** um **{(data.cached_message.created_at).replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%H:%M')} Uhr**\n"
                                    f"Gelöscht von {message_entry.user.mention} am **{(message_entry.created_at).strftime('%d-%m-%Y')}** um **{(message_entry.created_at).astimezone(tz=None).strftime('%H:%M')} Uhr**\n")
                    if(data.cached_message.pinned is not None):
                        if(data.cached_message.pinned):
                            embedString += "War die Nachricht gepinnt: **Ja**"
                        else:
                            embedString += "War die Nachricht gepinnt: **Nein**"
                    embedLog.description=embedString
                    if(ownSticker):
                        await channel.send(embed=embedLog, stickers=data.cached_message.stickers)
                    else:
                        await channel.send(embed=embedLog)
                elif(data.cached_message.embeds == []):
                    if(len(data.cached_message.attachments) > 1):
                        word = "Folgende Bilder wurden"
                    else:
                        word = "Folgendes Bild wurde"
                    embedString=f"**{word} aus <#{data.channel_id}> gelöscht**\n\n"
                    if(data.cached_message.reference):
                        embedString += (f"**Bezieht sich auf:** {data.cached_message.reference.jump_url}\n\n"
                                        f"> {data.cached_message.reference.cached_message.content}\n"
                                        f"> \n"
                                        f"> *Geschrieben von* {data.cached_message.reference.cached_message.author.mention}\n\n")
                    embedString +=(f"Geschrieben von {data.cached_message.author.mention} am **{(data.cached_message.created_at).strftime('%d-%m-%Y')}** um **{(data.cached_message.created_at).replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%H:%M')} Uhr**\n"
                                   f"Gelöscht von {message_entry.user.mention} am **{(message_entry.created_at).strftime('%d-%m-%Y')}** um **{(message_entry.created_at).astimezone(tz=None).strftime('%H:%M')} Uhr**\n")
                    embedLog.description=embedString
                    await channel.send(embed=embedLog)
                    for pic in data.cached_message.attachments:
                        ftype = pic.url.split('/')[-1].split('?')[0]
                        format = ftype.split('.')[-1]
                        lfile = io.BytesIO(requests.get(pic.url).content)
                        if(await self.config.guild(self.bot.get_guild(data.guild_id)).saveDeletedPics()):
                            path = os.path.dirname(__file__)
                            Image.open(lfile).save(f"{path}\\deleted_pics\\{ftype.split('.')[0]}-{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.{format}")
                            lfile.seek(0)
                        await channel.send(file=discord.File(fp=lfile, filename=f"{ftype}"))
                else:
                    if(len(data.cached_message.embeds) > 1):
                        word = "Folgende Embeds wurden"
                    else:
                        word = "Folgendes Embed wurde"
                    embedString=(f"**{word} aus <#{data.channel_id}> gelöscht**\n\n"
                                f"Geschrieben von {data.cached_message.author.mention} am **{(data.cached_message.created_at).strftime('%d-%m-%Y')}** um **{(data.cached_message.created_at).replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%H:%M')} Uhr**\n"
                                f"Gelöscht von {message_entry.user.mention} am **{(message_entry.created_at).strftime('%d-%m-%Y')}** um **{(message_entry.created_at).astimezone(tz=None).strftime('%H:%M')} Uhr**\n")
                    embedLog.description=embedString
                    data.cached_message.embeds.insert(0, embedLog)
                    await channel.send(embeds=data.cached_message.embeds)
        except Exception as error:
            print("Fehler bei Message-Log: " + str(error))

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        try:
            await self.config.guild(invite.guild).invites.set_raw(invite.code, value={'count': 0, 'uses': 0})
        except Exception as error:
            print("Fehler bei Invite-Create: " + str(error))

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        try:
            await self.config.guild(invite.guild).invites.clear_raw(invite.code)
        except Exception as error:
            print("Fehler bei Invite-Delete: " + str(error))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            if(await self.config.guild(member.guild).enableVoiceLog()):
                if(before.channel is not None and after.channel is None):
                    await before.channel.send(f"**{member.display_name}** hat den Channel verlassen")
        except Exception as error:
            print("Fehler bei Voice-Log: " + str(error))

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        try:
            if(dict(await self.config.guild(guild).users()).get(str(user.id)) is not None):
                await self.config.guild(guild).users.set_raw(user.id, 'banned', value=False)
        except Exception as error:
            print("Fehler bei Member-Unban: " + str(error))

    @tasks.loop(minutes=5)
    async def remove_warn_points(self):
        try:
            for guild in self.bot.guilds:
                if(await self.config.guild(guild).warnDynamicReset()):
                    for userWarn in await self.config.guild(guild).users():
                        if(await self.config.guild(guild).users.get_raw(userWarn, 'currentPoints') > 0 and guild.get_member(int(userWarn)) is not None):
                            await self.config.guild(guild).users.set_raw(userWarn, 'currentPoints', value=await self.config.guild(guild).users.get_raw(userWarn, 'currentPoints') - await self.config.guild(guild).warnDynamicResetCount())
                            print(f"Dynamische Punkte von {guild.get_member(int(userWarn)).display_name} wurden abgezogen")
                else:
                    for userWarn in await self.config.guild(guild).users():
                        if(guild.get_member(userWarn) is not None):
                            await self.config.guild(guild).users.set_raw(userWarn, 'currentPoints', value=0)
                            print("Warnpunkte wurden zurückgesetzt")
        except Exception as error:
            print("Fehler bei Scheduled-Task: " + str(error))

    async def cog_load(self):
        try:
            for guild in self.bot.guilds:
                if(await self.config.guild(guild).enableWarn()):
                    Modsystem.remove_warn_points.start(self)
                    print("Warnsystem aktiviert")
                    if(await self.config.guild(guild).warnDynamicReset()):
                        Modsystem.remove_warn_points.change_interval(minutes=await self.config.guild(guild).warnDynamicResetTime())
                        print(f"Dynamischer Punkteabbau auf {await self.config.guild(guild).warnDynamicResetTime()} Minuten gesetzt")
                    else:
                        Modsystem.remove_warn_points.change_interval(minutes=await self.config.guild(guild).warnResetTime())
                        print(f"Statischer Punktereset auf {await self.config.guild(guild).warnResetTime()} Minuten gesetzt")
        except Exception as error:
            print("Fehler in cog_load: " + str(error))

    async def cog_unload(self):
        try:
            Modsystem.remove_warn_points.cancel()
            print("Warnsystem deaktiviert")
        except Exception as error:
            print("Fehler in cog_unload: " + str(error))

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            for guild in self.bot.guilds:
                if(await self.config.guild(guild).enableWarn()):
                    Modsystem.remove_warn_points.start(self)
                    print("Warnsystem aktiviert")
                    if(await self.config.guild(guild).warnDynamicReset()):
                        Modsystem.remove_warn_points.change_interval(minutes=await self.config.guild(guild).warnDynamicResetTime())
                        print(f"Dynamischer Punkteabbau auf {await self.config.guild(guild).warnDynamicResetTime()} Minuten gesetzt")
                    else:
                        Modsystem.remove_warn_points.change_interval(minutes=await self.config.guild(guild).warnResetTime())
                        print(f"Statischer Punktereset auf {await self.config.guild(guild).warnResetTime()} Minuten gesetzt")
        except Exception as error:
            print("Fehler in cog_ready: " + str(error))

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if(message.author.bot is None):
                if(await self.config.guild(message.guild).deleteLinks()):
                    if(re.findall(await self.config.guild(message.guild).linkPattern(), message.content) != []):
                        embedLog.description=f"Diese inks sind auf **{message.guild.name}** verboten"
                        await message.author.send(embed=embedLog)
                        await message.delete()
        except Exception as error:
            print("Fehler in on_message: " + str(error))