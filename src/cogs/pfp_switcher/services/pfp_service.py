from typing import Optional, List

from src.cogs.pfp_switcher.services.pfp_switcher_service import PFPSwitcherService
from src.cogs.pfp_switcher.storage.model.profile_picture import ProfilePicture
from src.log import Logger


class PFPService(PFPSwitcherService):
    def is_current_pfp(self, profile_picture: ProfilePicture) -> bool:
        return self.uow.profile_pictures.get_current_hash() == profile_picture.hash

    async def set_pfp(self, profile_picture: ProfilePicture):
        with open(profile_picture.file_path, "rb") as file:
            await self.bot.user.edit(avatar=file.read())

        self.uow.profile_pictures.set_current_hash(profile_picture.hash)
        Logger.log("PFP Switcher", f"Changed to {profile_picture.name}")

    @staticmethod
    def _get_active_pfp(profile_pictures: List[ProfilePicture]) -> Optional[ProfilePicture]:
        for profile_picture in profile_pictures:
            for active_zone in profile_picture.active_zones:
                if active_zone.is_active:
                    return profile_picture

        return None

    def get_event_pfp(self) -> Optional[ProfilePicture]:
        profile_pictures = self.uow.profile_pictures.get_all_events()
        return self._get_active_pfp(profile_pictures)

    def get_seasonal_pfp(self) -> Optional[ProfilePicture]:
        profile_pictures = self.uow.profile_pictures.get_all_seasonal()
        return self._get_active_pfp(profile_pictures)

    def get_pfp(self) -> ProfilePicture:
        profile_picture = self.get_event_pfp()

        if profile_picture is None:
            profile_picture = self.get_seasonal_pfp()

        if profile_picture is None:
            profile_picture = self.uow.profile_pictures.get_default()

        return profile_picture
