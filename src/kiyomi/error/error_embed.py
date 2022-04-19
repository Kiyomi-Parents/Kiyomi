import random

from discord import Embed, Color


class ErrorEmbed(Embed):
    def __init__(self, message: str):
        super().__init__()

        self.colour = Color.from_rgb(255, 0, 0)
        self.add_field(name="\u200b", value=message)

        if random.randint(0, 1) == 1:
            self.set_thumbnail(url="https://share.lucker.xyz/qahu5/LOXaLeTU55.png")
        else:
            self.set_thumbnail(url="https://share.lucker.xyz/qahu5/tAyitEVO25.png")
