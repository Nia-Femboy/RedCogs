import discord

from zammad_py import ZammadAPI

embedSuccess = discord.Embed(description="# Erfolgreich\n**Es wurden folgende Werte gesetzt:**", color=0x0ffc03)
embedFailure = discord.Embed(color=0xff0000)
embedLog = discord.Embed(color=0xfc7f03)

class Functions():

    def __init__(self, config) -> None:
        self.config = config

    async def create_ticket(self, interaction: discord.Interaction, name: str, mail: str, subject: str, message: str):
        try:

            client = ZammadAPI(url=await self.config.guild(interaction.guild).host(), username=await self.config.guild(interaction.guild).user(), password=await self.config.guild(interaction.guild).password())

            print(client.user.me())

            params = {
                "title": "Test",
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

            ticket = await client.ticket.create(params=params)
            print(ticket)
        except Exception as error:
            #embedFailure.description = f"# Fehler\n### Es ist folgender Fehler aufgetreten:\n\n{error}"
            #await interaction.response.send_message(embed=embedFailure, ephemeral=True)
            print(f"Fehler bei create_ticket: {error}")

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

    async def update_modal(modal, *, modal_title: str = "", name_label: str = "", name_placeholder: str = "", mail_label: str = "", mail_placeholder: str = "", subject_label: str = "", subject_placeholder: str = "", message_label: str = "", message_placeholder: str = ""):
        try:
            modal.title = modal_title if modal_title != "" else modal.title
            modal.name.label = name_label if name_label != "" else modal.name.label
            modal.name.placeholder = name_placeholder if name_placeholder != "" else modal.name.placeholder
            modal.mail.label = mail_label if mail_label != "" else modal.mail.label
            modal.mail.placeholder = mail_placeholder if mail_placeholder != "" else modal.mail.placeholder
            modal.subject.label = subject_label if subject_label != "" else modal.subject.label
            modal.subject.placeholder = subject_placeholder if subject_placeholder != "" else modal.subject.placeholder
            modal.message.label = message_label if message_label != "" else modal.message.label
            modal.message.placeholder = message_placeholder if message_placeholder != "" else modal.message.placeholder
        except Exception as error:
            print(f"Fehler bei update_modal: {error}")