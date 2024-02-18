import discord

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
            userWarns={},
            userInvites={}
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
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:\n\n**{error}**"
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
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:\n\n**{error}**"
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
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:\n\n**{error}**"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="setbanlogchannel", description="Setzte den Logchannel für bans")
    @app_commands.describe(channelid="Die ChannelID des Ban Logchannel")
    @app_commands.checks.has_permissions(administrator=True)
    async def setbanlogchannel(self, interaction: discord.Interaction, channelid: str):
        try:
            if(interaction.guild.get_channel(int(channelid)) is None):
                raise Exception("Channel existiert nicht")
            await self.config.guild(interaction.guild).banLogChannel.set(int(channelid))
            embedSuccess.add_field(name="Ban Log Channel", value=channelid)
            await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:\n\n**{error}**"
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
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:\n\n**{error}**"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="setjoinlogchannel", description="Setze den Logchannel für Joins")
    @app_commands.describe(channelid="Die ChannelID des Join Logchannel")
    @app_commands.checks.has_permissions(administrator=True)
    async def setjoinlogchannel(self, interaction: discord.Interaction, channelid: str):
        try:
            if(interaction.guild.get_channel(int(channelid)) is None):
                raise Exception("Channel existiert nicht")
            await self.config.guild(interaction.guild).joinLogChannel.set(int(channelid))
            embedSuccess.add_field(name="Join Log Channel", value=channelid)
            await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:\n\n**{error}**"
            interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="setmessagedeletelogchannel", description="Setze den Logchannel für Delete-Messages")
    @app_commands.describe(channelid="Die ChannelID des Delete Message Logchannel")
    @app_commands.checks.has_permissions(administrator=True)
    async def setmessagedeletelogchannel(self, interaction: discord.Interaction, channelid: str):
        try:
            if(interaction.guild.get_channel(int(channelid)) is None):
                raise Exception("Channel existiert nicht")
            await self.config.guild(interaction.guild).deleteMessageLogChannel.set(int(channelid))
            embedSuccess.add_field(name="Delete Message Log Channel", value=channelid)
            await interaction.response.send_message(embed=embedSuccess)
            embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:\n\n**{error}**"
            interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="usegenerallogchannel", description="Nutze einen generellen Logchannel")
    @app_commands.describe(multiplelogchannel="Soll ein genereller Channel genutzt werden?")
    @app_commands.checks.has_permissions(administrator=True)
    async def usegenerallogchannel(self, interaction: discord.Interaction, multiplelogchannel: bool):
        try:
            if(multiplelogchannel):
                if(await self.config.guild(interaction.guild).generalLogChannel() is None):
                    raise Exception("Kein gültiger Channel definiert")
            else:
                await self.config.guild(interaction.guild).useGeneralLogChannel.set(multiplelogchannel)
                embedSuccess.add_field(name="Nutze General Log Channel", value=multiplelogchannel, inline=True)
                await interaction.response.send_message(embed=embedSuccess)
                embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:\n\n**{error}**"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="enablebanlog", description="Aktiviere oder deaktiviere das Loggen der Bans")
    @app_commands.describe(activate="Aktivieren oder deaktivieren")
    @app_commands.checks.has_permissions(administrator=True)
    async def enablebanlog(self, interaction: discord.Interaction, activate: bool):
        try:
            if(activate):
                if(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is not None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                    await self.config.guild(interaction.guild).enableBanLog.set(activate)
                    embedSuccess.add_field(name="Ban Log", value=activate)
                    await interaction.response.send_message(embed=embedSuccess)
                    embedSuccess.clear_fields()
                elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                    raise Exception("Kein gültiger genereller Channel definiert")
                elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).banLogChannel())) is None):
                    raise Exception("Kein Gültiger Channel angegeben")
            else:
                await self.config.guild(interaction.guild).enableBanLog.set(activate)
                embedSuccess.add_field(name="Ban Log", value=activate)
                await interaction.response.send_message(embed=embedSuccess)
                embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:\n\n**{error}**"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="enablekicklog", description="Aktiviere oder deaktiviere das Loggen der Kicks")
    @app_commands.describe(activate="Aktivieren oder deaktivieren")
    @app_commands.checks.has_permissions(administrator=True)
    async def enablekicklog(self, interaction: discord.Interaction, activate: bool):
        try:
            if(activate):
                if(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is not None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                    await self.config.guild(interaction.guild).enableKickLog.set(activate)
                    embedSuccess.add_field(name="Kick Log", value=activate)
                    await interaction.response.send_message(embed=embedSuccess)
                    embedSuccess.clear_fields()
                elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                    raise Exception("Kein gültiger genereller Channel definiert")
                elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).kickLogChannel())) is None):
                    raise Exception("Kein Gültiger Channel angegeben")
            else:
                await self.config.guild(interaction.guild).enableKickLog.set(activate)
                embedSuccess.add_field(name="Kick Log", value=activate)
                await interaction.response.send_message(embed=embedSuccess)
                embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:\n\n**{error}**"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="enableupdatelog", description="Aktiviere oder deaktiviere das Loggen der Client-Updates")
    @app_commands.describe(activate="Aktivieren oder deaktivieren")
    @app_commands.checks.has_permissions(administrator=True)
    async def enableupdatelog(self, interaction: discord.Interaction, activate: bool):
        try:
            if(activate):
                if(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is not None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                    await self.config.guild(interaction.guild).enableUpdateLog.set(activate)
                    embedSuccess.add_field(name="Client-Update Log", value=activate)
                    await interaction.response.send_message(embed=embedSuccess)
                    embedSuccess.clear_fields()
                elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                    raise Exception("Kein gültiger genereller Channel definiert")
                elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).updateLogChannel())) is None):
                    raise Exception("Kein Gültiger Channel angegeben")
            else:
                await self.config.guild(interaction.guild).enableUpdateLog.set(activate)
                embedSuccess.add_field(name="Client-Update Log", value=activate)
                await interaction.response.send_message(embed=embedSuccess)
                embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist folgender Fehler aufgetreten:\n\n**{error}**"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="enablejoinlog", description="Aktiviere oder deaktiviere das Loggen neuer User beim Joinen")
    @app_commands.describe(activate="Aktivieren oder deaktivieren")
    @app_commands.checks.has_permissions(administrator=True)
    async def enablejoinlog(self, interaction: discord.Interaction, activate: bool):
        try:
            if(activate):
                if(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is not None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                    await self.config.guild(interaction.guild).enableJoinLog.set(activate)
                    for invite in await interaction.guild.invites():
                        await self.config.guild(interaction.guild).userInvites.set_raw(invite.code, value={'count': 0, 'uses': invite.uses})
                    embedSuccess.add_field(name="Join Log", value=activate)
                    await interaction.response.send_message(embed=embedSuccess)
                    embedSuccess.clear_fields()
                elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                    raise Exception("Kein gültiger genereller Channel definiert")
                elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).enableJoinLog())) is None):
                    raise Exception("Kein Gültiger Channel angegeben")
            else:
                await self.config.guild(interaction.guild).enableJoinLog.set(activate)
                embedSuccess.add_field(name="Join Log", value=activate)
                await interaction.response.send_message(embed=embedSuccess)
                embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist ein Fehler aufgetreten:\n\n**{error}**"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="enabledeletemessagelog", description="Aktiviere oder deaktiviere das Loggen gelöschter Nachrichten")
    @app_commands.describe(activate="Aktivieren oder deaktivieren")
    @app_commands.checks.has_permissions(administrator=True)
    async def enabledeletemessagelog(self, interaction: discord.Interaction, activate: bool):
        try:
            if(activate):
                if(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is not None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                    await self.config.guild(interaction.guild).enableDeleteMessageLog.set(activate)
                    embedSuccess.add_field(name="DeleteMessageLog", value=activate)
                    await interaction.response.send_message(embed=embedSuccess)
                    embedSuccess.clear_fields()
                elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is None and await self.config.guild(interaction.guild).useGeneralLogChannel()):
                    raise Exception("Kein Gültiger genereller Channel definiert")
                elif(interaction.guild.get_channel(int(await self.config.guild(interaction.guild).deleteMessageLogChannel())) is None):
                    raise Exception("Kein Gültiger Channel angegeben")
            else:
                await self.config.guild(interaction.guild).enableDeleteMessageLog.set(activate)
                embedSuccess.add_field(name="DeleteMessageLog", value=activate)
                await interaction.response.send_message(embed=embedSuccess)
                embedSuccess.clear_fields()
        except Exception as error:
            embedFailure.description=f"**Es ist ein Fehler aufgetreten:\n\n**{error}**"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="enablevoicelog", description="Aktiviere oder deaktiviere das Loggen von Clients die den Voicechannel verlassen haben")
    @app_commands.describe(activate="Aktivieren oder deaktivieren")
    @app_commands.checks.has_permissions(administrator=True)
    async def enablevoicelog(self, interaction: discord.Interaction, activate: bool):
        try:
            await self.config.guild(interaction.guild).enableVoiceLog.set(activate)
            embedSuccess.add_field(name="Voice Log", value=activate)
            await interaction.response.send_message(embed=embedSuccess)
        except Exception as error:
            embedFailure.description=f"**Es ist ein Fehler aufgetreten:\n\n**{error}**"
            await interaction.response.send_message(embed=embedFailure)

    @modsystem.command(name="enablewarn", description="Aktiviere die Warn funktion")
    @app_commands.describe(activate="Aktivieren oder deaktivieren")
    @app_commands.checks.has_permissions(administrator=True)
    async def enablewarn(self, interaction: discord.Interaction, activate: bool):
        try:
            if(activate == False):
                await self.config.guild(interaction.guild).enableWarn.set(activate)
            else:
                if(await self.config.guild(interaction.guild).warnUseChannel() == False):
                    await self.config.guild(interaction.guild).enableWarn.set(activate)
                elif(await self.config.guild(interaction.guild).warnUseChannel() and interaction.guild.get_channel(int(await self.config.guild(interaction.guild).warnLogChannel())) is None):
                    raise Exception("Kein gültiger Channel definiert")
                if(await self.config.guild(interaction.guild).useGeneralLogChannel() and interaction.guild.get_channel(int(await self.config.guild(interaction.guild).generalLogChannel())) is not None):
                    await self.config.guild(interaction.guild).enableWarn.set(activate)
                else:
                    raise Exception("Kein gültiger Channel hinterlegt")
            embedSuccess.add_field(name="Aktiviere Warn funktion", value=activate)
            await interaction.response.send_message(embed=embedSuccess)
        except Exception as error:
            embedFailure.description=f"**Es ist ein Fehler aufgetreten:\n\n**{error}**"
            await interaction.response.send_message(embed=embedFailure)

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
                               f"Delete  Message-Log: **{await self.config.guild(interaction.guild).enableDeleteMessageLog()}**\n\n"
                               f"**General:**\n"
                               f"Nutze generel Log-Channel: **{await self.config.guild(interaction.guild).useGeneralLogChannel()}**\n")
            await interaction.response.send_message(embed=embed)
        except Exception as error:
            embedFailure.description=f"Es ist folgender Fehler aufgetreten:\n\n**{error}**"
            await interaction.response.send_message(embed=embedFailure)

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
            print(error)
    
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
            print(error)

    @commands.Cog.listener()
    async def on_raw_member_remove(self, data):
        try:
            inviteCode = await self.config.guild(data.user.guild).userInvites.get_raw(data.user.id, 'invitecode')
            await self.config.guild(data.user.guild).userInvites.clear_raw(data.user.id)
            await self.config.guild(data.user.guild).userInvites.set_raw(inviteCode, value={'count': await self.config.guild(data.user.guild).userInvites.get_raw(inviteCode, 'count') - 1})
        except Exception as error:
            print(error)

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
                embedString=(f"**Folgende Nachricht wurde aus <#{data.channel_id}> gelöscht**\n\n"
                             f"{data.cached_message.content}\n\n"
                             f"Geschrieben von {data.cached_message.author.mention} am **{(data.cached_message.created_at).strftime('%d-%m-%Y')}** um **{(data.cached_message.created_at).replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%H:%M')} Uhr**\n"
                             f"Gelöscht von {message_entry.user.mention} am **{(message_entry.created_at).strftime('%d-%m-%Y')}** um **{(message_entry.created_at).astimezone(tz=None).strftime('%H:%M')} Uhr**\n")
                if(data.cached_message.pinned is not None):
                    if(data.cached_message.pinned):
                        embedString += "War die Nachricht gepinnt: **Ja**"
                    else:
                        embedString += "War die Nachricht gepinnt: **Nein**"
                embedLog.description=embedString
                await channel.send(embed=embedLog)
        except Exception as error:
            print(error)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        try:
            await self.config.guild(invite.guild).userInvites.set_raw(invite.code, value={'count': 0})
        except Exception as error:
            print(error)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        try:
            await self.config.guild(invite.guild).userInvites.clear_raw(invite.code)
        except Exception as error:
            print(error)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            if(await self.config.guild(member.guild).enableVoiceLog()):
                if(before.channel is not None and after.channel is None):
                    await before.channel.send(f"**{member.display_name}** hat den Channel verlassen")
        except Exception as error:
            print(error)