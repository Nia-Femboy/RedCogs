import discord

from datetime import datetime, timedelta, timezone

class Functions():

    async def init_user(self, member: discord.Member, guild: discord.Guild):
            if(dict(await self.config.guild(guild).users()).get(str(member.id)) is None):
                await self.config.guild(member.guild).users.set_raw(member.id, value={'displayName': member.display_name,
                                                                                      'username': member.name,
                                                                                      'currentReason': "-",
                                                                                      'currentPoints': 0,
                                                                                      'totalPoints': 0,
                                                                                      'firstWarn': "-",
                                                                                      'lastWarn': "-",
                                                                                      'warnCount': 0,
                                                                                      'kickCount': 0,
                                                                                      'softBanned': False,
                                                                                      'banned': False})
            
    async def get_invite_with_code(invite_list, code):
            for inv in invite_list:
                if inv.code == code:
                    return inv
                
    async def clear_user(self, member):
            data = await self.config.guild(member.guild).users.get_raw(member.id)
            timeDiff = datetime.now() - member.joined_at.replace(tzinfo=None)
            oneDay = timedelta(days=1)
            if(data.get('warnCount') == 0 and data.get('kickCount') == 0 and data.get('softBanned') == False and data.get('banned') == False and timeDiff <= oneDay ):
                await self.config.guild(member.guild).users.clear_raw(member.id)

    async def do_softban(user: discord.user, channels: discord.Guild.channels, jailchannel: int):
        overwriteHide = discord.PermissionOverwrite()
        overwriteShow = discord.PermissionOverwrite()
        overwriteHide.view_channel=False
        overwriteShow.view_channel=True
        for channel in channels:
                if(channel.id == jailchannel):
                    await channel.set_permissions(user, overwrite=overwriteShow)
                else:
                    await channel.set_permissions(user, overwrite=overwriteHide)

    async def undo_softban(user: discord.user, channels: discord.Guild.channels):
        for channel in channels:
                await channel.set_permissions(user, overwrite=None)