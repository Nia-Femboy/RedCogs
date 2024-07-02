import discord

from .functions import Functions

class TicketButton(discord.ui.View):

    def __init__(self, buttonText: str, style: discord.ButtonStyle, modalTitle: str, modalNameLabel: str, modalNamePlaceholder: str, modalMailLabel: str, modalMailPlaceholder: str, modalSubjectLabel: str, modalSubjectPlaceholder: str, modalMessageLabel: str, modalMessagePlaceholder: str, modalMessageStyle: discord.TextStyle, interaction: discord.Interaction, func):
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
        self.interaction = interaction
        self.func = func
        self.add_button()

    def add_button(self):
        button = discord.ui.Button(label=self.buttonText, style=self.style)

        button.callback = Functions.create_ticket_modal(self.interaction, self.func)
        self.add_item(button)