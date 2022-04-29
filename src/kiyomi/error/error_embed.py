import random

from discord import Embed, Color


class ErrorEmbed(Embed):
    error_images = [
        "https://share.lucker.xyz/qahu5/LOXaLeTU55.png",
        "https://share.lucker.xyz/qahu5/tAyitEVO25.png"
    ]

    def __init__(self, message: str):
        super().__init__()

        self.colour = Color.from_rgb(255, 0, 0)
        self.add_field(name="\u200b", value=message)

        self.set_thumbnail(url=self.error_thumbnail)

    @property
    def error_thumbnail(self):
        random_image_index = random.randint(0, len(self.error_images) - 1)

        return self.error_images[random_image_index]
