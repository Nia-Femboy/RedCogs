from .mcwhitelist import McWhitelist

async def setup(bot):
    await bot.add_cog(McWhitelist(bot))