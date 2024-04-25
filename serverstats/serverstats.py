import discord

from redbot.core import commands, app_commands, Config

class ServerStats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=518963742)
        self.config.register_guild(
            memberCountChannel = 1199481948687585300,
            boosterCountChannel = 0,
            botCountChannel = 0,
            bannedCountChannel = 0,
            adminCountChannel = 0,
            modCountChannel = 0,
            helperCountChannel = 0,
            normalUserCountChannel = 0,
            memberChannelName = "dsaasd",
            boosterChannelName = "asdasd",
            botChannelName = "asddssss",
            bannedChannelName = "sdafasagaad",
            adminChannelName = "fdsfasf",
            modChannelName = "sgsdfsdf",
            helperChannelName = "sdgsdfsdf",
            normalUserChannelName = "sdsgsdsdfsf",
            memberActive = 0,
            boosterActive = 0,
            botActive = 0,
            bannedActive = 0,
            adminActive = 0,
            modActive = 0,
            helperActive = 0,
            normalUserActive = 0
        )

    serverstats = app_commands.Group(name="serverstats", description="Manage ServerStats Channel")

    @serverstats.command(name="setchannel", description="Setze Channel für Stats")
    @app_commands.describe(counter="Welcher Counter möchtest du Konfigurieren?", channel="ChannelID des Channels der genutzt werden soll")
    @app_commands.choices(counter=[
            app_commands.Choice(name="Member", value="memberCountChannel"),
            app_commands.Choice(name="Booster", value="boosterCountChannel"),
            app_commands.Choice(name="Bot", value="botCountChannel"),
            app_commands.Choice(name="Banned", value="bannedCountChannel"),
            app_commands.Choice(name="Admin", value="adminCountChannel"),
            app_commands.Choice(name="Moderator", value="modCountChannel"),
            app_commands.Choice(name="Helper", value="helperCountChannel"),
            app_commands.Choice(name="NormalUser", value="normalUserCountChannel")
        ])
    @app_commands.checks.has_permissions(administrator=True)
    async def setchannel(self, interaction: discord.Interaction, counter: app_commands.Choice[str], channel: int):
        try:
            if(counter.value == "memberCountChannel"):
                confval = self.config.guild(interaction.guild).memberCountChannel
            elif(counter.value == "boosterCountChannel"):
                confval = self.config.guild(interaction.guild).boosterCountChannel
            elif(counter.value == "botCountChannel"):
                confval = self.config.guild(interaction.guild).botCountChannel
            elif(counter.value == "bannedCountChannel"):
                confval = self.config.guild(interaction.guild).bannedCountChannel
            elif(counter.value == "adminCountChannel"):
                confval = self.config.guild(interaction.guild).modCountChannel
            elif(counter.value == "helperCountChannel"):
                confval = self.config.guild(interaction.guild).helperCountChannel
            elif(counter.value == "normalUserCountChannel"):
                confval = self.config.guild(interaction.guild).normalUserCountChannel
            await confval.set(channel)
            embed = discord.Embed(title="Erfolgreich", description="Es wurden folgende Werte gespeichert", color=0x0ffc03)
            embed.add_field(name="Art", value=f"{counter.name}", inline=True)
            embed.add_field(name="Channel", value=f"{channel}", inline=True)
            await interaction.response.send_message(embed=embed)
        except Exception as error:
            embed = discord.Embed(title="Fehler", description=f"Folgender Fehler ist eingetreten: {error}", color=0xff0000)
            await interaction.response.send_message(embed=embed)

    @serverstats.command(name="setchannelname", description="Setzte den Channelnamen")
    @app_commands.describe(counter="Counter", name="Channelname")
    @app_commands.choices(counter=[
        app_commands.Choice(name="Member", value="memberActive"),
        app_commands.Choice(name="Booster", value="boosterActive"),
        app_commands.Choice(name="Bot", value="botActive"),
        app_commands.Choice(name="Banned", value="bannedActive"),
        app_commands.Choice(name="Admin", value="adminActive"),
        app_commands.Choice(name="Moderator", value="modActive"),
        app_commands.Choice(name="Helper", value="helperActive"),
        app_commands.Choice(name="NormalUser", value="normalUserActive")
    ])
    @app_commands.checks.has_permissions(administrator=True)
    async def setchannelname(self, interaction: discord.Interaction, counter: app_commands.Choice[str], name: str):
        try:
            if(counter.value == "memberCountChannel"):
                confval = self.config.guild(interaction.guild).memberChannelName
            elif(counter.value == "boosterCountChannel"):
                confval = self.config.guild(interaction.guild).boosterChannelName
            elif(counter.value == "botCountChannel"):
                confval = self.config.guild(interaction.guild).botChannelName
            elif(counter.value == "bannedCountChannel"):
                confval = self.config.guild(interaction.guild).bannedChannelName
            elif(counter.value == "adminCountChannel"):
                confval = self.config.guild(interaction.guild).modChannelName
            elif(counter.value == "helperCountChannel"):
                confval = self.config.guild(interaction.guild).helperChannelName
            elif(counter.value == "normalUserCountChannel"):
                confval = self.config.guild(interaction.guild).normalUserChannelName
            await confval.set(name)
            embed = discord.Embed(title="Erfolgreich", description="Es wurden folgende Werte gespeichert", color=0x0ffc03)
            embed.add_field(name=f"{counter.name}", value=f"{name}", inline=False)
            interaction.response.send_message(embed=embed)
        except Exception as error:
            embed = discord.Embed(title="Fehler", description=f"Es ist folgender Fehler aufgetreten: {error}", color=0xff0000)
            interaction.response.send_message(embed=embed)

    @serverstats.command(name="setactive", description="Aktiviere einzelne Counter")
    @app_commands.describe(counter="Counter", active="Aktivieren?")
    @app_commands.choices(counter=[
        app_commands.Choice(name="Member", value="memberActive"),
        app_commands.Choice(name="Booster", value="boosterActive"),
        app_commands.Choice(name="Bot", value="botActive"),
        app_commands.Choice(name="Banned", value="bannedActive"),
        app_commands.Choice(name="Admin", value="adminActive"),
        app_commands.Choice(name="Moderator", value="modActive"),
        app_commands.Choice(name="Helper", value="helperActive"),
        app_commands.Choice(name="NormalUser", value="normalUserActive")
    ], active=[
        app_commands.Choice(name="Ja", value=1),
        app_commands.Choice(name="Nein", value=0)
    ])
    @app_commands.checks.has_permissions(administrator=True)
    async def setactive(self, interaction: discord.Interaction, counter: app_commands.Choice[str], active: app_commands.Choice[int]):
        try:
            if(counter.value == "memberActive"):
                confval = self.config.guild(interaction.guild).memberactive
            elif(counter.value == "boosterActive"):
                confval = self.config.guild(interaction.guild).boosterActive
            elif(counter.value == "botActive"):
                confval = self.config.guild(interaction.guild).botActive
            elif(counter.value == "bannedActive"):
                confval = self.config.guild(interaction.guild).bannedActive
            elif(counter.value == "adminActive"):
                confval = self.config.guild(interaction.guild).adminActive
            elif(counter.value == "modActive"):
                confval = self.config.guild(interaction.guild).modActive
            elif(counter.value == "helperActive"):
                confval = self.config.guild(interaction.guild).helperActive
            elif(counter.value == "normalUser"):
                confval = self.config.guild(interaction.guild).normalUser
            await confval.set(active.value)
            embed = discord.Embed(title="Erfolgreich", description="Es wurden folgende Werte gesetzt", color=0x0ffc03)
            embed.add_field(name=f"{counter.name}", value=f"{active.name}", inline=False)
            await interaction.response.send_message(embed=embed)
        except Exception as error:
            embed = discord.Embed(title="Fehler", description=f"Folgender Fehler ist eingetreten: {error}", color=0xff0000)
            await interaction.response.send_message(embed=embed)
            

    @serverstats.command(name="getconf", description="Zeige die Konfiguration")
    @app_commands.checks.has_permissions(administrator=True)
    async def getconf(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title="Aktuelle Konfiguration", description="Es wurden folgende Einstellungen konfiguriert", color=0x0ffc03)
            art = "Member\n"
            convertActive = lambda a : "True\n" if(a == 1) else "False\n"
            channel = str(await self.config.guild(interaction.guild).memberCountChannel()) + "\n"
            status = convertActive(await self.config.guild(interaction.guild).memberActive())
            name = await self.config.guild(interaction.guild).memberChannelName() + "\n"
            art += "Booster\n"
            channel += str(await self.config.guild(interaction.guild).boosterCountChannel()) + "\n"
            status += convertActive(await self.config.guild(interaction.guild).boosterActive())
            name += await self.config.guild(interaction.guild).boosterChannelName() + "\n"
            art += "Bot\n"
            channel += str(await self.config.guild(interaction.guild).botCountChannel()) + "\n"
            status += convertActive(await self.config.guild(interaction.guild).botActive())
            name += await self.config.guild(interaction.guild).botChannelName() + "\n"
            art  += "Banned\n"
            channel += str(await self.config.guild(interaction.guild).bannedCountChannel()) + "\n"
            status += convertActive(await self.config.guild(interaction.guild).bannedActive())
            name += await self.config.guild(interaction.guild).bannedChannelName() + "\n"
            art += "Admin\n"
            channel += str(await self.config.guild(interaction.guild).adminCountChannel()) + "\n"
            status += convertActive(await self.config.guild(interaction.guild).adminActive())
            name += await self.config.guild(interaction.guild).adminChannelName() + "\n"
            art += "Mod\n"
            channel += str(await self.config.guild(interaction.guild).modCountChannel()) + "\n"
            status += convertActive(await self.config.guild(interaction.guild).modActive())
            name += await self.config.guild(interaction.guild).modChannelName() + "\n"
            art += "Helper\n"
            channel += str(await self.config.guild(interaction.guild).helperCountChannel()) + "\n"
            status += convertActive(await self.config.guild(interaction.guild).helperActive())
            name += await self.config.guild(interaction.guild).helperChannelName() + "\n"
            art += "Normal User\n"
            channel += str(await self.config.guild(interaction.guild).normalUserCountChannel()) + "\n"
            status += convertActive(await self.config.guild(interaction.guild).normalUserActive())
            name += await self.config.guild(interaction.guild).normalUserChannelName() + "\n"
            embed.add_field(name="Art", value=f"{status}", inline=True)
            embed.add_field(name="Channel", value=f"{channel}", inline=True)
            embed.add_field(name="Status", value=f"{status}", inline=True)
            embed.add_field(name="Art", value=f"{art}", inline=True)
            embed.add_field(name="Channel Name", value=f"{name}", inline=True)
            await interaction.response.send_message(embed=embed)
        except Exception as error:
            embed = discord.Embed(title="Fehler", description=f"Es ist folgendes Problem aufgetreten: {error}", color=0xff0000)
            await interaction.response.send_message(embed=embed)

    @commands.command()
    async def setChannel(self, interaction: discord.Interaction, channelID: int, name: str):
        try:
            intents = discord.Intents()
            intents.presences
            intents.members = True
            print(channelID)
            valueset = await self.config.guild(interaction.guild).get_raw(channelID)
            print(valueset)
            #channel = discord.utils.get(self.guild.channels, id=1199481948687585300)
            #await channel.edit(name=f"Erfolgreich!")
        except Exception as error:
            print(f"Error: {error}")