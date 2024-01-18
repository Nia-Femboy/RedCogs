import discord

from redbot.core import commands, app_commands, Config
from mcrcon import MCRcon

class McWhitelist(commands.Cog):
    """Minecraft Whiteliste Cog"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=518963742)
        self.config.register_guild(
            host="",
            port=0,
            password="",
            mcuser={}
        )

    whitelist = app_commands.Group(name="whitelist", description="Whitelist management commands")

    @whitelist.command(name="setup", description="Einrichten der RCON Details")
    @app_commands.describe(host="Die IP oder Domain deines Servers", port="Der RCON Port deines Servers", password="Das von dir festgelegte RCON Passwort")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction, host: str, port: int, password: str):
        try:
            await self.config.guild(interaction.guild).host.set(host)
            await self.config.guild(interaction.guild).port.set(port)
            await self.config.guild(interaction.guild).password.set(password)
            embed = discord.Embed(title="Erfolgreich", description="Es wurden folgende Werte ersetzt:", color=0x24fc03)
            embed.add_field(name="Host", value=f"{host}", inline=True)
            embed.add_field(name="Port", value=f"{port}", inline=True)
            embed.add_field(name="Passwort", value=f"{password}", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            #await interaction.response.send_message(f"Es wurden folgende Werte gesetzt:\nHost: {host}\nPort: {port}\nPasswort: {password}", ephemeral=True)
        except Exception as error:
            embed = discord.Embed(description=f"Fehler: {error}", color=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @whitelist.command(name="add", description="Setze dich auf die Whitelist unseres Minecraft Servers")
    @app_commands.describe(username="Dein Minecraft Username")
    async def add(self, interaction: discord.Interaction, username: str):
        try:
            host = await self.config.guild(interaction.guild).host()
            port = await self.config.guild(interaction.guild).port()
            password = await self.config.guild(interaction.guild).password()
            existing = await self.config.guild(interaction.guild).mcuser.get_raw(interaction.user.id, 'mcusername')
            with MCRcon(host, password, port) as mcr:
                resp = mcr.command(f"/whitelist remove {existing}")
            removedExisting = 1
        except Exception as error:
            removedExisting = 0
        finally:
            try:
                with MCRcon(host, password, port) as mcr:
                    resp = mcr.command(f"/whitelist add {username.lower()}")
                await self.config.guild(interaction.guild).mcuser.set_raw(interaction.user.id, value={'discordusername': interaction.user.name, 'displayname': interaction.user.display_name, 'mcusername': username.lower()})
                if removedExisting == 0:
                    embed = discord.Embed(description=f"Du hast {username} zur Whitelist hinzugefügt", color=0x24fc03)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                elif removedExisting == 1:
                    embed = discord.Embed(description=f"Dein Username wurde von {existing} zu {username} auf der Whitelist geändert", color=0x24fc03)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
            except Exception as error:
                embed = discord.Embed(description=f"Fehler beim hinzufügen zur Whitelist\n{error}", color=0xff0000)
                await interaction.response.send_message(embed=embed, ephemeral=True)

    @whitelist.command(name="remove", description="Entferne dich von der Whitelist unseres Minecraft Servers")
    async def remove(self, interaction: discord.Interaction):
        try:
            host = await self.config.guild(interaction.guild).host()
            port = await self.config.guild(interaction.guild).port()
            password = await self.config.guild(interaction.guild).password()
            username = await self.config.guild(interaction.guild).mcuser.get_raw(interaction.user.id, 'mcusername')
            with MCRcon(host, password, port) as mcr:
                resp = mcr.command(f"/whitelist remove {username}")
            #test = await self.config.guild(interaction.guild).mcuser()
            await self.config.guild(interaction.guild).mcuser.clear_raw(interaction.user.id)
            embed = discord.Embed(description=f"{username} wurde von der Whitelist entfernt", color=0x24fc03)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as error:
            embed = discord.Embed(description=f"Du warst nicht auf der Whitelist hinterlegt", color=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @whitelist.command(name="showuser", description="Zeige sämtliche hinterlegten User")
    @app_commands.checks.has_permissions(administrator=True)
    async def showuser(self, interaction: discord.Interaction):
        try:
            user = await self.config.guild(interaction.guild).mcuser()
            embed = discord.Embed(title="Registrierte User", color=0x24fc03)
            for userID in user:
                dname = await self.config.guild(interaction.guild).mcuser.get_raw(userID, 'displayname')
                mcname = await self.config.guild(interaction.guild).mcuser.get_raw(userID, 'mcusername')
                embed.add_field(name=f"{dname}", value=f"{mcname}", inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as error:
            embed = discord.Embed(description=f"Fehler: {error}", color=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            host = await self.config.guild(member.guild).host()
            port = await self.config.guild(member.guild).port()
            password = await self.config.guild(member.guild).password()
            username = await self.config.guild(member.guild).mcuser.get_raw(member.id, 'mcusername')
            with MCRcon(host, password, port) as mcr:
                resp = mcr.command(f"/whitelist remove {username}")
            await self.config.guild(member.guild).mcuser.clear_raw(member.id)
            removedUser = 1
        except Exception as error:
            test = 0
