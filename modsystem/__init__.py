from .modsystem import Modsystem

async def setup(bot):
    await bot.add_cog(Modsystem(bot))