from discord import Guild

from src.kiyomi.base_view import BaseView
from ..components.buttons.invite_button import InviteButton
from src.kiyomi import Kiyomi


class InviteView(BaseView):
    def __init__(self, bot: Kiyomi, guild: Guild):
        super().__init__(bot, guild)

    def update_buttons(self):
        self.add_item(InviteButton(self.bot, self))
