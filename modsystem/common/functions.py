from datetime import datetime, timedelta, timezone

class Functions():

    async def init_user(self, member):
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