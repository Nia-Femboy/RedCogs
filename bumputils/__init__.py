from .bumputils import BumpUtils

async def setup(bot):
    await bot.add_cog(BumpUtils(bot))