import discord

from zammad_py import ZammadAPI

class TicketCreateModal(discord.ui.Modal, title="Ticket"):

    name = discord.ui.TextInput(label="Name")
    mail = discord.ui.TextInput(label="E-Mail")
    ticket__title = discord.ui.TextInput(label="Betreff")
    anielgen = discord.ui.TextInput(label="Dein Anliegen", style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Erhalten, danke {self.name.value}")

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