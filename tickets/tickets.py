from typing import Optional
import discord

from .common.buttons import TicketButton
from .common.functions import Functions
from .common.modals import TicketCreateModal

from redbot.core import commands, app_commands, Config

embedSuccessDescription = "# Erfolgreich\n**Es wurden folgende Werte gesetzt:**"
embedSuccess = discord.Embed(description=embedSuccessDescription, color=0x0ffc03)
embedFailure = discord.Embed(color=0xff0000)
embedLog = discord.Embed(color=0xfc7f03)
modal = TicketCreateModal()

class Tickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=518963742)
        self.config.register_guild(
            host="None",
            user="None",
            password="None",
            embedTitle="Ticket",
            embedDescription="Drücke auf den Button um ein neues Ticket zu erstellen",
            embedFooter="None",
            embedFooterURL="None",
            buttonLabel="Neues Ticket erstellen",
            modalTitle="Ticket",
            modalNameLabel="Name",
            modalNamePlaceholder="Max Mustermann",
            modalMailLabel="E-Mail",
            modalMailPlaceholder="max@mustermann.de",
            modalSubjectLabel="Subject",
            modalSubjectPlaceholder="Trollen im Chat",
            modalMessageLabel="Message",
            modalMessagePlaceholder="Der User XXX trollt sämtliche User im Chat",
            ticketCategory=0,
            tickets={}
    )

    tickets = app_commands.Group(name="ticket", description="Ticket commands")

    @tickets.command(name="setup", description="Konfiguriere das System")
    @app_commands.describe(option="Welche Option soll geändert werden?", wert="Der Wert welcher gesetzt werden soll")
    @app_commands.choices(option=[
        app_commands.Choice(name="Hostname", value="host"),
        app_commands.Choice(name="Username", value="user"),
        app_commands.Choice(name="Password", value="password"),
        app_commands.Choice(name="Embed Title", value="embedTitle"),
        app_commands.Choice(name="Embed Description", value="embedDescription"),
        app_commands.Choice(name="Embed Footer", value="embedFooter"),
        app_commands.Choice(name="Embed Footer URL", value="embedFooterURL"),
        app_commands.Choice(name="Modal Title", value="modalTitle"),
        app_commands.Choice(name="Modal Name Label", value="modalNameLabel"),
        app_commands.Choice(name="Modal Name Placeholder", value="modalNamePlaceholder"),
        app_commands.Choice(name="Modal Mail Label", value="modalMailLabel"),
        app_commands.Choice(name="Modal Mail Placeholder", value="modalMailPlaceholder"),
        app_commands.Choice(name="Modal Subject Label", value="modalSubjectLabel"),
        app_commands.Choice(name="Modal Subject Placeholder", value="modalSubjectPlaceholder"),
        app_commands.Choice(name="Modal Message Label", value="modalMessageLabel"),
        app_commands.Choice(name="Modal Message Placeholder", value="modalMessagePlaceholder"),
        app_commands.Choice(name="Button Label", value="buttonLabel"),
        app_commands.Choice(name="Ticket Kategorie", value="ticketCategory")
    ])
    async def setup(self, interaction: discord.Interaction, option: app_commands.Choice[str], wert: str):
        try:

            match option.value:

                case "host":

                    await self.config.guild(interaction.guild).host.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Host__**\n* {wert}"

                case "user":

                    await self.config.guild(interaction.guild).user.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Username__**\n* {wert}"

                case "password":

                    await self.config.guild(interaction.guild).password.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Password__**\n* {wert}"

                case "embedTitle":

                    await self.config.guild(interaction.guild).embedTitle.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Embed Title__**\n* {wert}"

                case "embedDescription":

                    await self.config.guild(interaction.guild).embedDescription.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Embed Description__**\n* {wert}"

                case "embedFooter":

                    await self.config.guild(interaction.guild).embedFooter.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Embed Footer__**\n* {wert}"

                case "embedFooterURL":

                    await self.config.guild(interaction.guild).embedFooterURL.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Embed Footer URL__**\n* {wert}"

                case "modalTitle":

                    await self.config.guild(interaction.guild).modalTitle.set(wert)
                    await Functions.update_modal(modal, modal_title=wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Modal Title__**\n* {wert}"

                case "modalNameLabel":

                    await self.config.guild(interaction.guild).modalNameLabel.set(wert)
                    await Functions.update_modal(modal, name_label=wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**Modal Name Label**\n* {wert}"

                case "modalNamePlaceholder":

                    await self.config.guild(interaction.guild).modalNamePlaceholder.set(wert)
                    await Functions.update_modal(modal, name_placeholder=wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Modal Name Placeholder__**\n* {wert}"

                case "modalMailLabel":

                    await self.config.guild(interaction.guild).modalMailLabel.set(wert)
                    await Functions.update_modal(modal, mail_label=wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Modal Mail Label__**\n* {wert}"

                case "modalMailPlaceholder":

                    await self.config.guild(interaction.guild).modalMailPlaceholder.set(wert)
                    await Functions.update_modal(modal, mail_placeholder=wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Modal Mail Placeholder__**\n* {wert}"

                case "modalSubjectLabel":

                    await self.config.guild(interaction.guild).modalSubjectLabel.set(wert)
                    await Functions.update_modal(modal, subject_label=wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Modal Subject Label__**\n* {wert}"

                case "modalSubjectPlaceholder":

                    await self.config.guild(interaction.guild).modalSubjectPlaceholder.set(wert)
                    await Functions.update_modal(modal, subject_placeholder=wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Modal Subject Placeholder__**\n* {wert}"

                case "modalMessageLabel":

                    await self.config.guild(interaction.guild).modalMessageLabel.set(wert)
                    await Functions.update_modal(modal, message_label=wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Modal Message Label__**\n* {wert}"

                case "modalMessagePlaceholder":

                    await self.config.guild(interaction.guild).modalMessagePlaceholder.set(wert)
                    await Functions.update_modal(modal, message_placeholder=wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Modal Message Placeholder__**\n* {wert}"

                case "buttonLabel":

                    await self.config.guild(interaction.guild).buttonLabel.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Button Label__**\n* {wert}"

                case "ticketCategory":
                    
                    if(wert.isnumeric() == False):
                        raise Exception("Die ID darf nur aus Zahlen bestehen")
                    if(discord.utils.get(interaction.guild.categories, id=int(wert))) is None:
                        raise Exception("Keine Kategorie gefunden")
                    await self.config.guild(interaction.guild).ticketCategory.set(wert)
                    embedSuccess.description = embedSuccess.description + f"\n\n**__Ticket Kategorie__**\n* {wert}"
                    
            await interaction.response.send_message(embed=embedSuccess, ephemeral=True)
            embedSuccess.description = embedSuccessDescription

        except Exception as error:
            embedFailure.description = f"# Fehler\n### Es ist folgender Fehler aufgetreten:\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    @tickets.command(name="getconfig", description="Zeigt die gesammte Konfiguration")
    @app_commands.checks.has_permissions(administrator=True)
    async def getconfig(self, interaction: discord.Interaction):
        try:
            embedLog.description = (f"# Ticketsystem Konfiguration\n"
                                    f"### System\n"
                                    f"* Host: **{await self.config.guild(interaction.guild).host()}**\n"
                                    f"* User: **{await self.config.guild(interaction.guild).user()}**\n"
                                    f"* Password: **{await self.config.guild(interaction.guild).password()}**\n"
                                    f"### Embed\n"
                                    f"* Title: **{await self.config.guild(interaction.guild).embedTitle()}**\n"
                                    f"* Description: **{await self.config.guild(interaction.guild).embedDescription()}**\n"
                                    f"* Footer: **{await self.config.guild(interaction.guild).embedFooter()}**\n"
                                    f"* Footer URL: **{await self.config.guild(interaction.guild).embedFooterURL()}**\n"
                                    f"### Button\n"
                                    f"* Label: **{await self.config.guild(interaction.guild).buttonLabel()}**\n"
                                    f"### Modal\n"
                                    f"* Title: **{await self.config.guild(interaction.guild).modalTitle()}**\n"
                                    f"* Name Label: **{await self.config.guild(interaction.guild).modalNameLabel()}**\n"
                                    f"* Name Placeholder: **{await self.config.guild(interaction.guild).modalNamePlaceholder()}**\n"
                                    f"* E-Mail Label: **{await self.config.guild(interaction.guild).modalMailLabel()}**\n"
                                    f"* E-Mail Placeholder: **{await self.config.guild(interaction.guild).modalMailPlaceholder()}**\n"
                                    f"* Subject Label: **{await self.config.guild(interaction.guild).modalSubjectLabel()}**\n"
                                    f"* Subject Placeholder: **{await self.config.guild(interaction.guild).modalSubjectPlaceholder()}**\n"
                                    f"* Description Label: **{await self.config.guild(interaction.guild).modalMessageLabel()}**\n"
                                    f"* Description Placeholder: **{await self.config.guild(interaction.guild).modalDescriptionPlaceholder()}**\n"
                                    f"### Tickets\n"
                                    f"* Ticket Category: **{discord.utils.get(interaction.guild.categories, id=int(await self.config.guild(interaction.guild).ticketCategory()))}**")
            await interaction.response.send_message(embed=embedLog)
        except Exception as error:
            embedFailure.description = f"# Fehler\n### Es ist folgender Fehler aufgetreten:\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    @tickets.command(name="create", description="Erstelle ein neues Ticket")
    async def create(self, interaction: discord.Interaction):
        try:

            #await Functions.create_text_channel(self, interaction, 5)

            embed = discord.Embed(description=(f"# {await self.config.guild(interaction.guild).embedTitle()}\n"
                                               f"{await self.config.guild(interaction.guild).embedDescription()}"))
            
            # button = TicketButton(await self.config.guild(interaction.guild).buttonLabel(),
            #                       discord.ButtonStyle.green,
            #                       await self.config.guild(interaction.guild).modalTitle(),
            #                       await self.config.guild(interaction.guild).modalNameLabel(),
            #                       await self.config.guild(interaction.guild).modalNamePlaceholder(),
            #                       await self.config.guild(interaction.guild).modalMailLabel(),
            #                       await self.config.guild(interaction.guild).modalMailPlaceholder(),
            #                       await self.config.guild(interaction.guild).modalSubjectLabel(),
            #                       await self.config.guild(interaction.guild).modalSubjectPlaceholder(),
            #                       await self.config.guild(interaction.guild).modalMessageLabel(),
            #                       await self.config.guild(interaction.guild).modalMessagePlaceholder(),
            #                       discord.TextStyle.long,
            #                       interaction,
            #                       TicketCreateModal)

            modal.title = await self.config.guild(interaction.guild).modalTitle()
            modal.name.label = await self.config.guild(interaction.guild).modalNameLabel()
            modal.name.placeholder = await self.config.guild(interaction.guild).modalNamePlaceholder()
            modal.mail.label = await self.config.guild(interaction.guild).modalMailLabel()
            modal.mail.placeholder = await self.config.guild(interaction.guild).modalMailPlaceholder()
            modal.subject.label = await self.config.guild(interaction.guild).modalSubjectLabel()
            modal.subject.placeholder = await self.config.guild(interaction.guild).modalSubjectPlaceholder()
            modal.message.label = await self.config.guild(interaction.guild).modalMessageLabel()
            modal.message.placeholder = await self.config.guild(interaction.guild).modalMessagePlaceholder()
            modal.message.style = discord.TextStyle.long
            modal.mainClass = self.config
            
            await interaction.response.send_message(embed=embed, view=TicketButton(await self.config.guild(interaction.guild).buttonLabel(),
                                                                      discord.ButtonStyle.green,
                                                                      modal))
            #await interaction.response.send_message(embed=embed, view=button)

        except Exception as error:
            print(error)

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if(message.author.bot == False):
                for userID in await self.config.guild(message.guild).tickets():
                    if(await self.config.guild(message.guild).tickets.get_raw(userID, 'channel') == message.channel.id):
                        if(message.content == "close" and userID == str(message.author.id)):
                            await message.channel.delete()
                            await self.config.guild(message.guild).tickets.clear_raw(userID)
                        else:
                            await message.channel.send("Nur der User darf das Ticket schließen")
        except Exception as error:
            print(f"Fehler bei on_message: {error}")