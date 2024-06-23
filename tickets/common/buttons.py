import discord

from .modals import TicketCreateModal

class TicketButton(discord.ui.View):

    @discord.ui.button(label="asd", style=discord.ButtonStyle.gray)
    async def create_ticket(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(TicketCreateModal())
        await interaction.response.send_message("Heyho Url: " + str(button.url))
        print(self)