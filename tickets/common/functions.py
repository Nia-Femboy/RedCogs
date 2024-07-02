import discord

from zammad_py import ZammadAPI

embedSuccess = discord.Embed(description="# Erfolgreich\n**Es wurden folgende Werte gesetzt:**", color=0x0ffc03)
embedFailure = discord.Embed(color=0xff0000)
embedLog = discord.Embed(color=0xfc7f03)

class Functions():

    async def create_ticket(self, interaction: discord.Interaction, name: str, mail: str, subject: str, message: str):
        try:
            client = ZammadAPI(url=self.config.guild(interaction.guild).host(), username=self.config.guild(interaction.guild).user(), password=self.config.guild(interaction.guild).password())

            params = {
                "title": self.ticket__title.value,
                "group": "Discord",
                "customer": mail,
                "article": {
                    "from": name,
                    "subject": subject,
                    "body": message,
                    "type": "note",
                    "internal": False
                }
            }

            ticket = client.ticket.create(params=params)
            print(ticket)
        except Exception as error:
            embedFailure.description = f"# Fehler\n### Es ist folgender Fehler aufgetreten:\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    async def create_text_channel(self, interaction: discord.Interaction, ticketID: int):
        try:
            channelname=f"ticket-{interaction.user}"
            permissionOverwrite = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True)
            }
            channel = await interaction.guild.create_text_channel(name=channelname, category=discord.utils.get(interaction.guild.categories, id=int(await self.config.guild(interaction.guild).ticketCategory())), overwrites=permissionOverwrite)
            await interaction.channel.typing()
            await channel.send("Heyho")
            await self.config.guild(interaction.guild).tickets.set_raw(interaction.user.id, value={'channel': channel.id, 'zammadID': ticketID})
            # msg = await interaction.client.wait_for('message', timeout=None)
            # print(msg.content)
            # if(msg.content == "close"):
            #     await channel.delete()
        except Exception as error:
            embedFailure.description = f"# Fehler\n### Es ist folgenderA Fehler aufgetreten:\n\n{error}"
            await interaction.response.send_message(embed=embedFailure, ephemeral=True)

    async def create_ticket_modal(interaction: discord.Interaction, func):
            modal = func(title="self.title")
            modal.name.label = "self.nameLabel"
            modal.name.placeholder = "self.namePlaceholder"
            modal.mail.label = "self.mailLabel"
            modal.mail.placeholder = "self.mailPlaceholder"
            modal.subject.label = "self.subjectLabel"
            modal.subject.placeholder = "self.subjectPlaceholder"
            modal.message.label = "self.messageLabel"
            modal.message.placeholder = "self.messagePlaceholder"
            modal.message.style = "self.messageStyle"
            modal.user = interaction.user
            await interaction.response.send_modal(modal)