import discord

from .modals import TicketCreateModal

class TicketButton(discord.ui.View):

    def __init__(self, buttonText: str, style: discord.ButtonStyle, modalTitle: str, modalNameLabel: str, modalNamePlaceholder: str, modalMailLabel: str, modalMailPlaceholder: str, modalSubjectLabel: str, modalSubjectPlaceholder: str, modalMessageLabel: str, modalMessagePlaceholder: str, modalMessageStyle: discord.TextStyle):
        super().__init__(timeout=None)
        self.buttonText = buttonText
        self.style = style
        self.title = modalTitle
        self.nameLabel = modalNameLabel
        self.namePlaceholder = modalNamePlaceholder
        self.mailLabel = modalMailLabel
        self.mailPlaceholder = modalMailPlaceholder
        self.subjectLabel = modalSubjectLabel
        self.subjectPlaceholder = modalSubjectPlaceholder
        self.messageLabel = modalMessageLabel
        self.messagePlaceholder = modalMessagePlaceholder
        self.messageStyle = modalMessageStyle
        self.add_button()

    def add_button(self):
        button = discord.ui.Button(label=self.buttonText, style=self.style)

        async def create_tickets(interaction: discord.Interaction):
            modal = TicketCreateModal(title=self.title)
            modal.name.label = self.nameLabel
            modal.name.placeholder = self.namePlaceholder
            modal.mail.label = self.mailLabel
            modal.mail.placeholder = self.mailPlaceholder
            modal.subject.label = self.subjectLabel
            modal.subject.placeholder = self.subjectPlaceholder
            modal.message.label = self.messageLabel
            modal.message.placeholder = self.messagePlaceholder
            modal.message.style = self.messageStyle
            modal.user = interaction.user
            await interaction.response.send_modal(modal)

        button.callback = create_tickets
        self.add_item(button)