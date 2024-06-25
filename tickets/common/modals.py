import discord

from discord.utils import MISSING
from zammad_py import ZammadAPI
from ..tickets import Tickets

class TicketCreateModal(discord.ui.Modal):

    def __init__(self, title: str) -> None:
        super().__init__(title=title)

    name = discord.ui.TextInput(label="")
    mail = discord.ui.TextInput(label="")
    subject = discord.ui.TextInput(label="")
    message = discord.ui.TextInput(label="")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Erhalten, danke {self.user.display_name}")

        client = ZammadAPI(url=self.config.guild(interaction.guild).host(), username=self.config.guild(interaction.guild).user(), password=self.config.guild(interaction.guild).password())

        params = {
            "title": self.ticket__title.value,
            "group": "Discord",
            "customer": self.mail.value,
            "article": {
                "from": self.name.value,
                "subject": self.ticket__title.value,
                "body": self.anielgen.value,
                "type": "note",
                "internal": False
            }
        }

        ticket = client.ticket.create(params=params)

        Tickets.create_text_channel(interaction, ticket.id)