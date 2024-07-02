import discord

from discord.utils import MISSING
from .functions import Functions

class TicketCreateModal(discord.ui.Modal):

    def __init__(self, *, title: str) -> None:
        super().__init__(title=title)

    name = discord.ui.TextInput(label="")
    mail = discord.ui.TextInput(label="")
    subject = discord.ui.TextInput(label="")
    message = discord.ui.TextInput(label="")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Erhalten, danke {self.user.display_name}")

        await Functions.create_ticket(self, interaction, self.name.value, self.mail.value, self.subject.value, self.message.value)