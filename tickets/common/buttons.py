import discord

class TicketButton(discord.ui.View):

    def __init__(self, buttonText: str, style: discord.ButtonStyle, modal):
        super().__init__(timeout=None)
        self.buttonText = buttonText
        self.style = style
        self.modal = modal
        self.add_button()

    def add_button(self):
        button = discord.ui.Button(label=self.buttonText, style=self.style)

        async def create_tickets(interaction: discord.Interaction):
            self.modal.user = interaction.user
            await interaction.response.send_modal(self.modal)

        button.callback = create_tickets
        self.add_item(button)