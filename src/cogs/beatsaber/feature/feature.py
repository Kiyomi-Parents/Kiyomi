class FeatureFlagNotFoundException(Exception):
    pass


class FeatureFlagException(Exception):
    pass


class Feature:
    def __init__(self, uow, db_guild, feature_flag):
        self.uow = uow
        self.db_guild = db_guild
        self.feature_flag = feature_flag

    def __has(self):
        return hasattr(self.db_guild, self.feature_flag)

    async def set(self, status):
        if not self.__has():
            raise FeatureFlagNotFoundException(f"Could not find feature flag: {self.feature_flag}")

        current_status = self.get()

        if current_status == status:
            raise FeatureFlagException(f"Feature flag {self.feature_flag} is already {'enabled' if status else 'disabled'}!")

        if current_status:
            await self.on_disable()
        else:
            await self.on_enable()

        self.uow.guild_repo.set_feature(self.db_guild, self.feature_flag, status)

    def get(self):
        if not self.__has():
            raise FeatureFlagNotFoundException(f"Could not find feature flag: {self.feature_flag}")

        return getattr(self.db_guild, self.feature_flag)

    async def on_enable(self):
        pass

    async def on_disable(self):
        pass
