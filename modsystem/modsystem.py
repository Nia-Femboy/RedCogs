import discord

from discord.utils import MISSING
from discord.ext import tasks

from redbot.core import commands, app_commands, Config
from datetime import datetime, timedelta, timezone

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
            warnUseChannel=False,
            warnUseDM=True,
            warnModRole=0,
            warnFirstMultiplicator=1,
            warnSecondMultiplicator=1,
            warnThirdMultiplicator=1,
            userWarns={},
            userInvites={}
        )

    modsystem = app_commands.Group(name="modlog", description="Modlog setup commands")

    @modsystem.command(name="setupchannel", description="Allgemeines Setup des Systems")
    @app_commands.describe(choice="Bitte den gewünschten Parameter auswählen", channelid="Die ChannelID des jeweiligen Channel")
    @app_commands.choices(choice=[
        app_commands.Choice(name="General Logchannel", value="gChannel"),
        app_commands.Choice(name="Warn Logchannel", value="wChannel"),
        app_commands.Choice(name="Kick Logchannel", value="kChannel"),
        app_commands.Choice(name="Ban Logchannel", value="bChannel"),
        app_commands.Choice(name="Update Logchannel", value="uChannel"),
        app_commands.Choice(name="Join Logchannel", value="jChannel"),
        app_commands.Choice(name="Message Logchannel", value="mChannel")
    ])
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction, choice: app_commands.Choice[str], channelid: str):
        try:

            if(interaction.guild.get_channel(int(channelid)) is None):
                        raise Exception("Channel existiert nicht")

            match choice.value:

                case "gChannel":

                    await self.config.guild(interaction.guild).generalLogChannel.set(int(channelid))
                    embedSuccess.add_field(name="General Log Channel", value=channelid)

                case "wChannel":

                    await self.config.guild(interaction.guild).warnLogChannel.set(int(channelid))
                    embedSuccess.add_field(name="Warning Log Channel", value=channelid)

                case "kChannel":

                    await self.config.guild(interaction.guild).kickLogChannel.set(int(channelid))
                    embedSuccess.add_field(name="Kick Log Channeöl", value=channelid)

                case "bChannel":

                    await self.config.guild(interaction.guild).banLogChannel.set(int(channelid))
                    embedSuccess.add_field(name="Ban Log Channel", value=channelid)

                case "uChannel":

                    await self.config.guild(interaction.guild).updateLogChannel.set(int(channelid))
                    embedSuccess.add_field(name="Client-Update Log Channel", value=channelid)

                case "jChannel":

                    await self.config.guild(interaction.guild).joinLogChannel.set(int(channelid))
                    embedSuccess.add_field(name="Join Log Channel", value=channelid)

                case "mChannel":

                    await self.config.guild(interaction.guild).deleteMessageLogChannel.set(int(channelid))
                    embedSuccess.add_field(name="Delete Message Log Channel", value=channelid)

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
        app_commands.Choice(name="Voicelog", value="vLog")
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
                        if((await self.config.guild(interaction.guild).warnUseChannel() == False) or (await self.config.guild(interaction.guild).useGeneralLogChannel() and interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is not None)):
                            if(await self.config.guild(interaction.guild).warnResetTime() > 0 and await self.config.guild(interaction.guild).warnDDynamicReset() == False):
                                await self.config.guild(interaction.guild).enableWarn.set(status)
                                Modsystem.remove_warn_points.change_interval(minutes=await self.config.guild(interaction.guild).warnResetTime())
                                Modsystem.remove_warn_points.start(self)
                            elif(await self.config.guild(interaction.guild).warnDynamicReset() and await self.config.guild(interaction.guild).warnDynamicResetTime() > 0):
                                await self.config.guild(interaction.guild).enableWarn.set(status)
                                Modsystem.remove_warn_points.change_interval(minutes=await self.config.guild(interaction.guild).warnDynamicResetTime())
                                Modsystem.remove_warn_points.start(self)
                            else:
                                await self.config.guild(interaction.guild).enableWarn.set(status)
                        elif(await self.config.guild(interaction.guild).warnUseChannel() and interaction.guild.get_channel(int(await self.config.guild(interaction.guild).warnLogChannel())) is None):
                            raise Exception("Kein gültiger Channel definiert")
                        elif(await self.config.guild(interaction.guild).useGeneralLogChannel() and interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is None):
                            raise Exception("Kein gültiger genereller Channel definiert")
                    else:
                        await self.config.guild(interaction.guild).enableWarn.set(status)
                        Modsystem.remove_warn_points.stop()
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
                                if(invite.code in await self.config.guild(interaction.guild).userInvites()):
                                    await self.config.guild(interaction.guild).userInvites.set_raw(invite.code, value={'count': await self.config.guild(interaction.guild).userInvites.get_raw(invite.code, 'count'), 'uses': invite.uses})
                                else:
                                    await self.config.guild(interaction.guild).userInvites.set_raw(invite.code, value={'count': 0, 'uses': invite.uses})
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
                            embedSuccess.add_field(name="Client-Update Log", value=status)
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
        app_commands.Choice(name="Nutze einen Logchannel", value="warnUseChannel"),
        app_commands.Choice(name="Die niedrigste Modrolle welche warnen können soll", value="warnModRole"),
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
                    embedSuccess.add_field(name="Es wurde folgender Wert gesetzt:", value=int(wert))

                case "warnKickWeight":

                    if(wert == None):
                        raise Exception("Bitte den wert festlegen")
                    await self.config.guild(interaction.guild).warnKickWeight.set(int(wert))
                    embedSuccess.add_field(name="Es wurde folgender Wert gesetzt:", value=int(wert))

                case "warnBanWeight":

                    if(wert == None):
                        raise Exception("Bitte den wert festlegen")
                    await self.config.guild(interaction.guild).warnBanWeight.set(int(wert))
                    embedSuccess.add_field(name="Es wurde folgender Wert gesetzt:", value=int(wert))

                case "warnDynamicReset":

                    if(activate == None):
                        raise Exception("Bitte activate festlegen")
                    if(activate):
                        Modsystem.remove_warn_points.change_interval(minutes=await self.config.guild(interaction.guild).warnDynamicResetTime())
                    else:
                        Modsystem.remove_warn_points.change_interval(minutes=await self.config.guild(interaction.guild).warnResetTime())
                    await self.config.guild(interaction.guild).warnDynamicReset.set(activate)
                    embedSuccess.add_field(name="Es wurde folgender Wert gesetzt:", value=activate)

                case "warnDynamicResetTime":

                    if(wert == None):
                        raise Exception("Bitte den wert festlegen")
                    if(await self.config.guild(interaction.guild).warnDynamicReset() and await self.config.guild(interaction.guild).enableWarn()):
                        Modsystem.remove_warn_points.change_interval(minutes=int(wert))
                    await self.config.guild(interaction.guild).warnDynamicResetTime.set(int(wert))
                    embedSuccess.add_field(name="Es wurde folgender Wert gesetzt:", value=int(wert))

                case "warnDynamicResetCount":

                    if(wert == None):
                        raise Exception("Bitte den wert festlegen")
                    await self.config.guild(interaction.guild).warnDynamicResetCount.set(int(wert))
                    embedSuccess.add_field(name="Es wurde folgender Wert gesetzt:", value=int(wert))

                case "warnResetTime":

                    if(wert == None):
                        raise Exception("Bitte den wert festlegen")
                    if(await self.config.guild(interaction.guild).warnDynamicReset() == False and await self.config.guild(interaction.guild).enableWarn()):
                        Modsystem.remove_warn_points.change_interval(minutes=int(wert))
                    await self.config.guild(interaction.guild).warnResetTime.set(int(wert))
                    embedSuccess.add_field(name="Es wurde folgender Wert gesetzt:", value=int(wert))

                case "warnUseDM":

                    if(activate == None):
                        raise Exception("Bitte activate festlegen")
                    await self.config.guild(interaction.guild).warnUseDM.set(activate)
                    embedSuccess.add_field(name="Es wurde folgender Wert gesetzt:", value=activate)

                case "warnUseChannel":

                    if(activate == None):
                        raise Exception("Bitte activate festlegen")
                    if(activate):
                        if((interaction.guild.get_channel(int(await self.config.guild(interaction.guild).warnLogChannel())) and await self.config.guild(interaction.guild).useGeneralLogChannel() == False) or (interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) and await self.config.guild(interaction.guild).useGeneralLogChannel())):
                            await self.config.guild(interaction.guild).warnUseChannel.set(activate)
                            embedSuccess.add_field(name="Es wurde folgender Wert gesetzt:", value=activate)
                        else:
                            raise Exception("Kein gültiger Channel festgelegt")
                    else:
                        await self.config.guild(interaction.guild).warnUseChannel.set(activate)
                        embedSuccess.add_field(name="Es wurde folgender Wert gesetzt:", value=activate)

                case "warnModRole":

                    if(wert == None):
                        raise Exception("Bitte den wert festlegen")
                    if(interaction.guild.get_role(int(wert))):
                        await self.config.guild(interaction.guild).warnModRole.set(int(wert))
                        embedSuccess.add_field(name="Es wurde folgender Wert gesetzt:", value=int(wert))
                    else:
                        raise Exception("Keine gültige Rolle angegeben")
                    
                case "warnFirstMultiplicator":

                    if(wert == None):
                        raise Exception("Bitte einen Wert setzten")
                    await self.config.guild(interaction.guild).warnFirstMultiplicator.set(float(wert.replace(",", ".")))
                    embedSuccess.add_field(name="Es wurde folgender Wert gesetzt:", value=float(wert.replace(",", ".")))

                case "warnSecondMultiplicator":

                    if(wert == None):
                        raise Exception("Bitte einen Wert setzten")
                    await self.config.guild(interaction.guild).warnSecondMultiplicator.set(float(wert.replace(",", ".")))
                    embedSuccess.add_field(name="Es wurde folgender Wert gesetzt:", value=float(wert.replace(",", ".")))

                case "warnThirdMultiplicator":

                    if(wert == None):
                        raise Exception("Bitte einen Wert setzten")
                    await self.config.guild(interaction.guild).warnThirdMultiplicator.set(float(wert.replace(",", ".")))
                    embedSuccess.add_field(name="Es wurde folgender Wert gesetzt:", value=float(wert.replace(",", ".")))

            await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()

        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    @modsystem.command(name="getconfig", description="Schau dir die aktuelle Config an")
    @app_commands.checks.has_permissions(administrator=True)
    async def showconfig(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title="Config", color=0x0ffc03)
            embed.description=(f"**Channel:**\n"
                               f"Gneral Log-Channel: <#{await self.config.guild(interaction.guild).generalLogChannel()}>\n"
                               f"Warn Log-Channel: <#{await self.config.guild(interaction.guild).warnLogChannel()}>\n"
                               f"Kick Log-Channel: <#{await self.config.guild(interaction.guild).kickLogChannel()}>\n"
                               f"Ban Log-Channel: <#{await self.config.guild(interaction.guild).banLogChannel()}>\n"
                               f"Update Log-Channel: <#{await self.config.guild(interaction.guild).updateLogChannel()}>\n"
                               f"Join Log-Channel: <#{await self.config.guild(interaction.guild).joinLogChannel()}>\n"
                               f"Delete Message Log-Channel: <#{await self.config.guild(interaction.guild).deleteMessageLogChannel()}>\n\n"
                               f"**Status:**\n"
                               f"Warn funktion  aktiviert: **{await self.config.guild(interaction.guild).enableWarn()}**\n"
                               f"Kick-Log: **{await self.config.guild(interaction.guild).enableKickLog()}**\n"
                               f"Ban-Log: **{await self.config.guild(interaction.guild).enableBanLog()}**\n"
                               f"Update-Log: **{await self.config.guild(interaction.guild).enableUpdateLog()}**\n"
                               f"Join-Log: **{await self.config.guild(interaction.guild).enableJoinLog()}**\n"
                               f"Delete  Message-Log: **{await self.config.guild(interaction.guild).enableDeleteMessageLog()}**\n"
                               f"Voice-Log: **{await self.config.guild(interaction.guild).enableVoiceLog()}**\n\n"
                               f"**Warn**\n"
                               f"Warnpunke pro Warn: **{await self.config.guild(interaction.guild).warnWeight()}**\n"
                               f"Nötige Punkte zum Kicken: **{await self.config.guild(interaction.guild).warnKickWeight()}**\n"
                               f"Nötige Punkte zum Bannen: **{await self.config.guild(interaction.guild).warnBanWeight()}**\n"
                               f"Dynamischer Punkteabbau: **{await self.config.guild(interaction.guild).warnDynamicReset()}**\n"
                               f"Dynamischer Punkteabbau Intervall: **{await self.config.guild(interaction.guild).warnDynamicResetTime()}**\n"
                               f"Dynamischer Punkteabbau Punkte: **{await self.config.guild(interaction.guild).warnDynamicResetCount()}**\n"
                               f"Statischer Punkteabbau Intervall: **{await self.config.guild(interaction.guild).warnResetTime()}**\n"
                               f"Nutze Channel für die Verwarnungen: **{await self.config.guild(interaction.guild).warnUseChannel()}**\n"
                               f"Nutze DM für die Verwarnungen: **{await self.config.guild(interaction.guild).warnUseDM()}**\n"
                               f"Mindestrolle die Verwarnen kann: {interaction.guild.get_role(await self.config.guild(interaction.guild).warnModRole()).mention}\n\n"
                               f"**General:**\n"
                               f"Nutze den generellen Log-Channel: **{await self.config.guild(interaction.guild).useGeneralLogChannel()}**\n")
            await interaction.response.send_message(embed=embed)
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    @modsystem.command(name="updateinvitecodes", description="Update die gespeicherten Invite-Codes")
    @app_commands.checks.has_permissions(administrator=True)
    async def updateinvitecodes(self, interaction: discord.Interaction):
        try:
            for invite in await interaction.guild.invites():
                if(await self.config.guild(interaction.guild).userInvites.get_raw(invite.code) is None):
                    await self.config.guild(interaction.guild).userInvites.set_raw(invite.code, value={'count': 0, 'uses': invite.uses})
                else:
                    await self.config.guild(interaction.guild).userInvites.set_raw(invite.code, value={'count': await self.config.guild(interaction.guild).userInvites.get_raw(invite.code, 'count'), 'uses': invite.uses})
            embedSuccess.add_field(name="Update der Invite-Codes", value="Erfolgreich")
            await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    @app_commands.command()
    @app_commands.describe(user="Der User der verwarnt werden soll", reason="Grund der Verwarnung", stufe="Die Schwere der Verwarnung 1 - 3 (Optional)")
    @app_commands.checks.cooldown(1, 90)
    async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str, stufe: int = None):
        try:
            if(await self.config.guild(interaction.guild).enableWarn() == False):
                raise Exception("Die Funktion ist momentan nicht aktiviert")
            if(interaction.user.top_role.position < interaction.guild.get_role(await self.config.guild(interaction.guild).warnModROle()).position):
                raise Exception("Keine Berechtigung diesen Befehl zu nutzen")
            if(interaction.user.top_role.position < user.top_role.position):
                raise Exception("Du kannst keine Leute verwarnen die einen höheren Rang haben als du")
            if(user.bot):
                raise Exception("Du kannst keinen Bot verwarnen")
            embed = discord.Embed(title="Aktion Erfolgreich", color=0x0ffc03)
            embedDM = discord.Embed(title="!!!Important/Wichtig!!!", color=0xff0000)
            if(await self.config.guild(interaction.guild).warnUseChannel() and await self.config.guild(interaction.guild).warnUseDM()):
                recipientChannel = interaction.guild.get_channel(int(await self.config.guild(interaction.guild).warnLogChannel()))
                recipientUser = user
            elif(await self.config.guild(interaction.guild).warnUseChannel() == False and await self.config.guild(interaction.guild).warnUseDM() == False):
                embedNotice = discord.Embed(title="Information", description=f"User wird per DM benachrichtigt da weder der Warnchannel noch die DM's aktiviert sind", color=0xfc7f03)
                interaction.channel.send(embed=embedNotice)
                recipientChannel = None
                recipientUser = user
            elif(await self.config.guild(interaction.guild).warnUseChannel()):
                recipientChannel = interaction.guild.get_channel(int(await self.config.guild(interaction.guild).warnLogChannel()))
                recipientUser = None
            elif(await self.config.guild(interaction.guild).warnUseDM()):
                recipientChannel = None
                recipientUser = user
            if(stufe is not None):
                if(0 > stufe > 3):
                    raise Exception("Die auszuwählende Stufe geht von 1 bis 3")
                else:
                    match stufe:
                        case 1:
                            multiplikator = await self.config.guild(interaction.guild).warnFirstMultiplicator()
                        case 2:
                            multiplikator = await self.config.guild(interaction.guild).warnSecondMultiplicator()
                        case 3:
                            multiplikator = await self.config.guild(interaction.guild).warnThirdMultiplicator()
                    currentTime = datetime.now().astimezone(tz=None).strftime('%d-%m-%Y um %H:%M')
                    if(dict(await self.config.guild(interaction.guild).userWarns()).get(str(user.id)) is None):
                        await self.config.guild(interaction.guild).userWarns.set_raw(user.id, value={'displayName': user.display_name,
                                                                                                     'username': user.name,
                                                                                                     'currentReason': reason,
                                                                                                     'currentPoints': await self.config.guild(interaction.guild).warnWeight() * multiplikator,
                                                                                                     'totalPoints': await self.config.guild(interaction.guild).warnWeight() * multiplikator,
                                                                                                     'firstWarn': currentTime,
                                                                                                     'lastWarn': currentTime,
                                                                                                     'kickCount': 0,
                                                                                                     'banned': False})
                        embed.description=(f"{user.mention} **wurde erfolgreich verwarnt**\n\n"
                                           f"Aktuelle Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                           f"Fehlende Punkte bis zum Kick: **{await self.config.guild(interaction.guild).warnKickWeight() - await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                           f"Fehlende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n")
                        embedDM.description=(f"Du wurdest gerade von {interaction.user.display_name} mit der Begründung **{reason}** Verwarnt\n\n"
                                             f"Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                             f"Verbleibende Punkte bis zum Kick: **{await self.config.guild(interaction.guild).warnKickWeight() - await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                             f"Verbleibende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**")
                    else:
                        if(await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'banned')):
                            raise Exception("Warn nicht möglich da der User bereits gebant ist")
                        currentPoints = await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints') + await self.config.guild(interaction.guild).warnWeight() * multiplikator
                        totalPoints = await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'totalPoints') + await self.config.guild(interaction.guild).warnWeight() * multiplikator
                        if(currentPoints < await self.config.guild(interaction.guild).warnKickWeight() or (await self.config.guild(interaction.guild).warnKickWeight() < currentPoints < await self.config.guild(interaction.guild).warnBanWeight())):
                            await self.config.guild(interaction.guild).userWarns.set_raw(user.id, value={'displayName': user.display_name,
                                                                                                         'username': user.name,
                                                                                                         'currentReason': reason,
                                                                                                         'currentPoints': currentPoints,
                                                                                                         'totalPoints': totalPoints,
                                                                                                         'firstWarn': await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'firstWarn'),
                                                                                                         'lastWarn': currentTime,
                                                                                                         'kickCount': await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'kickCount'),
                                                                                                         'banned': False})
                            if(await self.config.guild(interaction.guild).warnKickWeight() - currentPoints < 0):
                                embed.description=(f"{user.mention} **wurde erfolgreich verwarnt**\n\n"
                                                   f"Aktuelle Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                                   f"Anzahl der Kicks: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'kickCount')}**\n"
                                                   f"Fehlende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - currentPoints}**\n")
                                embedDM.description=(f"Du wurdest gerade von {interaction.user.display_name} mit der Begründung **{reason}** Verwarnt\n\n"
                                                     f"Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                                     f"Anzahl deiner Kicks: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'kickCount')}**\n"
                                                     f"Verbleibende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**")
                            else:
                                embed.description=(f"{user.mention} **wurde erfolgreich verwarnt**\n\n"
                                                   f"Aktuelle Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                                   f"Fehlende Punkte bis zum Kick: **{await self.config.guild(interaction.guild).warnKickWeight() - currentPoints}**\n"
                                                   f"Fehlende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - currentPoints}**\n")
                            embedDM.description=(f"Du wurdest gerade von {interaction.user.display_name} mit der Begründung **{reason}** Verwarnt\n\n"
                                                 f"Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                                 f"Verbleibende Punkte bis zum Kick: **{await self.config.guild(interaction.guild).warnKickWeight() - await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                                 f"Verbleibende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**")
                        elif(await self.config.guild(interaction.guild).warnKickWeight() <= currentPoints < await self.config.guild(interaction.guild).warnBanWeight()):
                            await self.config.guild(interaction.guild).userWarns.set_raw(user.id, value={'displayName': user.display_name,
                                                                                                         'username': user.name,
                                                                                                         'currentReason': reason,
                                                                                                         'currentPoints': currentPoints,
                                                                                                         'totalPoints': totalPoints,
                                                                                                         'firstWarn': await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'firstWarn'),
                                                                                                         'lastWarn': currentTime,
                                                                                                         'kickCount': await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'kickCount') + 1,
                                                                                                         'banned': False})
                            await user.kick(reason=reason)
                            embed.description=(f"{user.mention} wurde mit der Begründung **{reason}** gekickt\n\n"
                                               f"Aktuelle Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                               f"Kickgrenze: **{await self.config.guild(interaction.guild).warnKickWeight()}**\n"
                                               f"Fehlende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - currentPoints}**\n")
                            embedDM.description=(f"Du wurdest gerade von {interaction.user.display_name} mit der Begründung **{reason}** vom Server gekickt\n\n"
                                                 f"Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                                 f"Dies ist dein **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'kickCount')}.** Kick\n"
                                                 f"Verbleibende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n")
                        elif(currentPoints >= await self.config.guild(interaction.guild).warnBanWeight()):
                            await self.config.guild(interaction.guild).userWarns.set_raw(user.id, value={'displayName': user.display_name,
                                                                                                         'username': user.name,
                                                                                                         'currentReason': reason,
                                                                                                         'currentPoints': currentPoints,
                                                                                                         'totalPoints': totalPoints,
                                                                                                         'firstWarn': await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'firstWarn'),
                                                                                                         'lastWarn': currentTime,
                                                                                                         'kickCount': await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'kickCount'),
                                                                                                         'banned': True})
                            await user.ban(reason=reason, delete_message_days=1)
                            embed.description=(f"{user.mention} wurde mit der Begründung **{reason}** gebannt\n\n"
                                               f"Aktuelle Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                               f"Anzahl der Kicks: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'kickCount')}**\n"
                                               f"Bangrenze: **{await self.config.guild(interaction.guild).warnBanWeight()}**")
                            embedDM.description=(f"Du wurdest gerade von {interaction.user.display_name} mit der Begründung **{reason}** gebant\n\n")
            else:
                currentTime = datetime.now().astimezone(tz=None).strftime('%d-%m-%Y : %H:%M')
                if(dict(await self.config.guild(interaction.guild).userWarns()).get(str(user.id)) is None):
                    await self.config.guild(interaction.guild).userWarns.set_raw(user.id, value={'displayName': user.display_name,
                                                                                                 'username': user.name,
                                                                                                 'currentReason': reason,
                                                                                                 'currentPoints': await self.config.guild(interaction.guild).warnWeight(),
                                                                                                 'totalPoints': await self.config.guild(interaction.guild).warnWeight(),
                                                                                                 'firstWarn': currentTime,
                                                                                                 'lastWarn': currentTime,
                                                                                                 'kickCount': 0,
                                                                                                 'banned': False})
                    embed.description=(f"{user.mention} **wurde erfolgreich verwarnt**\n\n"
                                       f"Aktuelle Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                       f"Fehlende Punkte bis zum Kick: **{await self.config.guild(interaction.guild).warnKickWeight() - await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                       f"Fehlende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n")
                    embedDM.description=(f"Du wurdest gerade von {interaction.user.display_name} mit der Begründung **{reason}** Verwarnt\n\n"
                                         f"Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                         f"Verbleibende Punkte bis zum Kick: **{await self.config.guild(interaction.guild).warnKickWeight() - await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                         f"Verbleibende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**")
                else:
                    if(await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'banned')):
                        raise Exception("Warn nicht möglich da der User bereits gebant ist")
                    currentPoints = await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints') + await self.config.guild(interaction.guild).warnWeight()
                    totalPoints = await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'totalPoints') + await self.config.guild(interaction.guild).warnWeight()
                    if(currentPoints < await self.config.guild(interaction.guild).warnKickWeight() or (await self.config.guild(interaction.guild).warnKickWeight() < currentPoints < await self.config.guild(interaction.guild).warnBanWeight())):
                        await self.config.guild(interaction.guild).userWarns.set_raw(user.id, value={'displayName': user.display_name,
                                                                                                     'username': user.name,
                                                                                                     'currentReason': reason,
                                                                                                     'currentPoints': currentPoints,
                                                                                                     'totalPoints': totalPoints,
                                                                                                     'firstWarn': await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'firstWarn'),
                                                                                                     'lastWarn': currentTime,
                                                                                                     'kickCount': await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'kickCount'),
                                                                                                     'banned': False})
                        if(await self.config.guild(interaction.guild).warnKickWeight() - currentPoints < 0):
                            embed.description=(f"{user.mention} **wurde erfolgreich verwarnt**\n\n"
                                               f"Aktuelle Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                               f"Anzahl der Kicks: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'kickCount')}**\n"
                                               f"Fehlende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - currentPoints}**\n")
                            embedDM.description=(f"Du wurdest gerade von {interaction.user.display_name} mit der Begründung **{reason}** Verwarnt\n\n"
                                                 f"Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                                 f"Anzahl deiner Kicks: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'kickCount')}**\n"
                                                 f"Verbleibende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**")
                        else:
                            embed.description=(f"{user.mention} **wurde erfolgreich verwarnt**\n\n"
                                               f"Aktuelle Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                               f"Fehlende Punkte bis zum Kick: **{await self.config.guild(interaction.guild).warnKickWeight() - currentPoints}**\n"
                                               f"Fehlende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - currentPoints}**\n")
                            embedDM.description=(f"Du wurdest gerade von {interaction.user.display_name} mit der Begründung **{reason}** Verwarnt\n\n"
                                                 f"Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                                 f"Verbleibende Punkte bis zum Kick: **{await self.config.guild(interaction.guild).warnKickWeight() - await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                                 f"Verbleibende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**")
                    elif(await self.config.guild(interaction.guild).warnKickWeight() <= currentPoints < await self.config.guild(interaction.guild).warnBanWeight()):
                        await self.config.guild(interaction.guild).userWarns.set_raw(user.id, value={'displayName': user.display_name,
                                                                                                     'username': user.name,
                                                                                                     'currentReason': reason,
                                                                                                     'currentPoints': currentPoints,
                                                                                                     'totalPoints': totalPoints,
                                                                                                     'firstWarn': await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'firstWarn'),
                                                                                                     'lastWarn': currentTime,
                                                                                                     'kickCount': await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'kickCount') + 1,
                                                                                                     'banned': False})
                        await user.kick(reason=reason)
                        embed.description=(f"{user.mention} wurde mit der Begründung **{reason}** gekickt\n\n"
                                           f"Aktuelle Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                           f"Kickgrenze: **{await self.config.guild(interaction.guild).warnKickWeight()}**\n"
                                           f"Fehlende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - currentPoints}**\n")
                        embedDM.description=(f"Du wurdest gerade von {interaction.user.display_name} mit der Begründung **{reason}** vom Server gekickt\n\n"
                                             f"Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                             f"Dies ist dein **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'kickCount')}.** Kick\n"
                                             f"Verbleibende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n")
                    elif(currentPoints >= await self.config.guild(interaction.guild).warnBanWeight()):
                        await self.config.guild(interaction.guild).userWarns.set_raw(user.id, value={'displayName': user.display_name,
                                                                                                     'username': user.name,
                                                                                                     'currentReason': reason,
                                                                                                     'currentPoints': currentPoints,
                                                                                                     'totalPoints': totalPoints,
                                                                                                     'firstWarn': await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'firstWarn'),
                                                                                                     'lastWarn': currentTime,
                                                                                                     'kickCount': await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'kickCount'),
                                                                                                     'banned': True})
                        await user.ban(reason=reason, delete_message_days=1)
                        embed.description=(f"{user.mention} wurde mit der Begründung **{reason}** gebannt\n\n"
                                           f"Aktuelle Punkte: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'currentPoints')}**\n"
                                           f"Anzahl der Kicks: **{await self.config.guild(interaction.guild).userWarns.get_raw(user.id, 'kickCount')}**\n"
                                           f"Bangrenze: **{await self.config.guild(interaction.guild).warnBanWeight()}**")
                        embedDM.description=(f"Du wurdest gerade von {interaction.user.display_name} mit der Begründung **{reason}** gebant\n\n")
                        
            if(recipientChannel is not None):
                await recipientChannel.send(embed=embed)

            if(recipientUser is not None):
                await recipientUser.send(embed=embedDM)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as error:

            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    @modsystem.command(name="setwarnpoints", description="Setze die Warnpoints für einen User")
    @app_commands.describe(user="User", points="Warnpoints")
    @app_commands.checks.has_permissions(administrator=True)
    async def setwarnpoints(self, interaction: discord.Interaction, user: discord.User, points: int):
        try:
            if(dict(await self.config.guild(interaction.guild).userWarns()).get(str(user.id)) is not None):
                await self.config.guild(interaction.guild).userWarns.set_raw(user.id, 'currentPoints', value=points)
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

    @modsystem.command(name="showwuserwarnstats", description="Zeigt die aktuellen Daten für einen User an")
    @app_commands.describe(user="User")
    async def showuserwarnstats(self, interaction: discord.Interaction, user: discord.User):
        try:
            if(interaction.user.top_role.positions < interaction.guild.get_role(await self.config.guild(interaction.guild).warnModRole()).position):
                if(interaction.user != user):
                    raise Exception("Du darfst dir nur deine Eigenen Daten anschauen")
            embed = discord.Embed(title=f"Hier sind die aktuellen Daten", color=0xfc7f03)
            if(dict(await self.config.guild(interaction.guild).userWarns()).get(str(user.id)) is not None):
                currentUserRecord = await self.config.guild(interaction.guild).userWarns.get_raw(user.id)
                embed.description=(f"**Es ist aktuell folgendes von {user.mention} gespeichert:**\n\n"
                                   f"Begründung des letzten Warns: **{currentUserRecord.get('currentReason')}**\n"
                                   f"Aktuelle Punkte: **{currentUserRecord.get('currentPoints')}**\n"
                                   f"Alle jemals erhaltene Punkte: **{currentUserRecord.get('totalPoints')}**\n"
                                   f"Erster Warn am **{currentUserRecord.get('firstWarn')}** erhalten\n"
                                   f"Letzter Warn am **{currentUserRecord.get('lastWarn')}** erhalten\n"
                                   f"Anzahl an Kicks durch Warns: **{currentUserRecord.get('kickCount')}**\n"
                                   f"User gebannt: **{currentUserRecord.get('banned')}**")
                embed.set_thumbnail(url=user.display_avatar.url)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed.description=f"**Es liegen aktuell keine Daten zu {user.mention} vor**"
                embed.set_thumbnail(url=user.display_avatar.url)
                await interaction.response.send_message(embed=embed)
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)
            

    @modsystem.command(name="showwarnlist", description="Zeige eine List an mit allen Verwarnungen")
    async def showwarnlist(self, interaction: discord.Interaction):
        try:
            if(interaction.user.top_role.position < interaction.guild.get_role(await self.config.guild(interaction.guild).warnModRole()).position):
                raise Exception("Du hast keine Berechtigungen diesen Befehl auszuführen")
            embed = discord.Embed(title="Alle aktuellen Verwarnungen", color=0xfc7f03)
            listString = ""
            for index, userID in enumerate(dict(await self.config.guild(interaction.guild).userWarns()), start=1):
                if index % 4 == 0:
                    embed.description=listString
                    await interaction.channel.send(embed=embed)
                    listString = ""
                listString += (f"{interaction.guild.get_member(int(userID)).mention}\n\n"
                               f"Username: **{interaction.guild.get_member(int(userID)).name}**\n"
                               f"Aktuelle Points: **{await self.config.guild(interaction.guild).userWarns.get_raw(userID, 'currentPoints')}**\n"
                               f"Gesamte Points: **{await self.config.guild(interaction.guild).userWarns.get_raw(userID, 'totalPoints')}**\n"
                               f"Anzahl der Kicks: **{await self.config.guild(interaction.guild).userWarns.get_raw(userID, 'kickCount')}**\n"
                               f"Verbleibende Punkte bis zum Ban: **{await self.config.guild(interaction.guild).warnBanWeight() - await self.config.guild(interaction.guild).userWarns.get_raw(userID, 'currentPoints')}**\n\n\n")
            embed.description = listString
            await interaction.response.send_message(embed=embed)
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:**\n\n{error}"

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry):
        try:
            if(entry.action == discord.AuditLogAction.kick and await self.config.guild(entry.guild).enableKickLog() == 1):
                if(await self.config.guild(entry.guild).useGeneralLogChannel() == True):
                    channel = entry.guild.get_channel(await self.config.guild(entry.guild).generalLogChannel())
                else:
                    channel = entry.guild.get_channel(await self.config.guild(entry.guild).kickLogChannel())
                if(entry.reason is not None):
                    embedLog.description=entry.target.mention + " wurde von " + entry.user.mention + " mit der Begründung **" + entry.reason + "** gekickt"
                else:
                    embedLog.description=entry.target.mention + " wurde von " + entry.user.mention + " ohne Angabe von Gründen gekickt"
                await channel.send(embed=embedLog)
            elif(entry.action == discord.AuditLogAction.ban and await self.config.guild(entry.guild).enableBanLog() == 1):
                if(await self.config.guild(entry.guild).useGeneralLogChannel() == True):
                    channel = entry.guild.get_channel(await self.config.guild(entry.guild).generalLogChannel())
                else:
                    channel = entry.guild.get_channel(await self.config.guild(entry.guild).banLogChannel())
                if(entry.reason is not None):
                    embedLog.description=entry.target.mention + " wurde von " + entry.user.mention + " mit der Begründung **" + entry.reason + "** gebant"
                else:
                    embedLog.description=entry.target.mention + " wurde von " + entry.user.mention + " ohne Angabe von Gründen gebant"
                await channel.send(embed=embedLog)
            elif(entry.action == discord.AuditLogAction.member_update and await self.config.guild(entry.guild).enableUpdateLog() == 1):
                if(await self.config.guild(entry.guild).useGeneralLogChannel() == True):
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

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            if(await self.config.guild(member.guild).enableJoinLog()):
                if(await self.config.guild(member.guild).useGeneralLogChannel() == True):
                    channel = member.guild.get_channel(await self.config.guild(member.guild).generalLogChannel())
                else:
                    channel = member.guild.get_channel(await self.config.guild(member.guild).joinLogChannel())
                invites_after = await member.guild.invites()
                usedInvite: discord.invite
                for invite in await self.config.guild(member.guild).userInvites():
                    result = await Modsystem.get_invite_with_code(invites_after, invite)
                    if(result is None):
                        await self.config.guild(member.guild).userInvites.clear_raw(invite)
                    else:
                        if(await self.config.guild(member.guild).userInvites.get_raw(invite, 'uses') < result.uses):
                            usedInvite = result
                            usedInviteInfo = await self.bot.fetch_invite(result.code)
                            break
                await self.config.guild(member.guild).userInvites.set_raw(usedInvite.code, value={'count': await self.config.guild(member.guild).userInvites.get_raw(usedInvite.code, 'count') + 1, 'uses': await self.config.guild(member.guild).userInvites.get_raw(usedInvite.code, 'uses') + 1})
                await self.config.guild(member.guild).userInvites.set_raw(member.id, value={'invitecode': usedInvite.code})
                embedLog.set_thumbnail(url=member.display_avatar.url)
                embedString=(f"Der Account {member.mention} wurde am **{(member.created_at).strftime('%d-%m-%Y')}** um **{(member.created_at).strftime('%H:%M')} Uhr** erstellt und ist mit dem Invite-Code **{usedInvite.code}** von {usedInvite.inviter.mention} beigetreten\n\n"
                             f"Informationen zu dem Invite:\n"
                             f"* Benutzungen: **{usedInvite.uses}**\n"
                             f"* Channel: {usedInvite.channel.mention}\n"
                             f"* Geblieben: **{await self.config.guild(member.guild).userInvites.get_raw(usedInvite.code, 'count')}**\n"
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
            inviteCode = await self.config.guild(data.user.guild).userInvites.get_raw(data.user.id, 'invitecode')
            await self.config.guild(data.user.guild).userInvites.clear_raw(data.user.id)
            await self.config.guild(data.user.guild).userInvites.set_raw(inviteCode, value={'count': await self.config.guild(data.user.guild).userInvites.get_raw(inviteCode, 'count') - 1, 'uses': await self.config.guild(data.user.guild).userInvites.get_raw(inviteCode, 'uses')})
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
                if(message_entry.created_at < data.cached_message.created_at):
                    message_entry.created_at = datetime.now()
                    message_entry.user = data.cached_message.author
                if(data.cached_message.attachments == [] and data.cached_message.embeds == []):
                    embedString=(f"**Folgende Nachricht wurde aus <#{data.channel_id}> gelöscht**\n\n\n"
                                f"{data.cached_message.content}\n\n\n"
                                f"Geschrieben von {data.cached_message.author.mention} am **{(data.cached_message.created_at).strftime('%d-%m-%Y')}** um **{(data.cached_message.created_at).replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%H:%M')} Uhr**\n"
                                f"Gelöscht von {message_entry.user.mention} am **{(message_entry.created_at).strftime('%d-%m-%Y')}** um **{(message_entry.created_at).astimezone(tz=None).strftime('%H:%M')} Uhr**\n")
                    if(data.cached_message.pinned is not None):
                        if(data.cached_message.pinned):
                            embedString += "War die Nachricht gepinnt: **Ja**"
                        else:
                            embedString += "War die Nachricht gepinnt: **Nein**"
                    embedLog.description=embedString
                    await channel.send(embed=embedLog)
                elif(data.cached_message.embeds == []):
                    if(len(data.cached_message.attachments) > 1):
                        word = "Folgende Bilder wurden"
                    else:
                        word = "Folgendes Bild wurde"
                    embedString=(f"**{word} aus <#{data.channel_id}> gelöscht**\n\n"
                                f"Geschrieben von {data.cached_message.author.mention} am **{(data.cached_message.created_at).strftime('%d-%m-%Y')}** um **{(data.cached_message.created_at).replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%H:%M')} Uhr**\n"
                                f"Gelöscht von {message_entry.user.mention} am **{(message_entry.created_at).strftime('%d-%m-%Y')}** um **{(message_entry.created_at).astimezone(tz=None).strftime('%H:%M')} Uhr**\n")
                #pic = io.BytesIO(await data.cached_message.attachments[0].read(use_cached=True))
                #await channel.send(file=discord.File(pic, 'image.png'))
                    embedLog.description=embedString
                    await channel.send(embed=embedLog)
                    for pic in data.cached_message.attachments:
                        await channel.send(pic)
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
            await self.config.guild(invite.guild).userInvites.set_raw(invite.code, value={'count': 0, 'uses': 0})
        except Exception as error:
            print("Fehler bei Invite-Create: " + str(error))

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        try:
            await self.config.guild(invite.guild).userInvites.clear_raw(invite.code)
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
            if(dict(await self.config.guild(guild).userWarns()).get(str(user.id)) is not None):
                await self.config.guild(guild).userWarns.set_raw(user.id, 'banned', value=False)
        except Exception as error:
            print("Fehler bei Member-Unban: " + error)

    @tasks.loop(minutes=5)
    async def remove_warn_points(self):
        try:
            for guild in self.bot.guilds:
                if(await self.config.guild(guild).warnDynamicReset()):
                    for userWarn in await self.config.guild(guild).userWarns():
                        await self.config.guild(guild).userWarns.set_raw(userWarn, 'currentPoints', value=await self.config.guild(guild).userWarns.get_raw(userWarn, 'currentPoints') - await self.config.guild(guild).warnDynamicResetCount())
                else:
                    for userWarn in await self.config.guild(guild).userWarns():
                        await self.config.guild(guild).userWarns.set_raw(userWarn, 'currentPoints', value=0)
        except Exception as error:
            print("Fehler bei Scheduled-Task: " + error)

    async def cog_load(self):
        try:
            for guild in self.bot.guilds:
                if(await self.config.guild(guild).enableWarn()):
                    Modsystem.remove_warn_points.start(self)
                    if(await self.config.guild(guild).warnDynamicReset()):
                        Modsystem.remove_warn_points.change_interval(minutes=await self.config.guild(guild).warnDynamicResetTime())
                    else:
                        Modsystem.remove_warn_points.change_interval(minutes=await self.config.guild(guild).warnResetTime())
        except Exception as error:
            print("Fehler in cog_load: " + error)

    async def cog_unload(self):
        try:
            Modsystem.remove_warn_points.cancel()
        except Exception as error:
            print("Fehler in cog_unload: " + error)

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            for guild in self.bot.guilds:
                if(await self.config.guild(guild).enableWarn()):
                    Modsystem.remove_warn_points.start(self)
                    if(await self.config.guild(guild).warnDynamicReset()):
                        Modsystem.remove_warn_points.change_interval(minutes=await self.config.guild(guild).warnDynamicResetTime())
                    else:
                        Modsystem.remove_warn_points.change_interval(minutes=await self.config.guild(guild).warnResetTime())
        except Exception as error:
            print("Fehler in cog_load: " + error)