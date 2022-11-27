from typing import Type

from discord import ActivityType, BaseActivity, Game, Streaming, CustomActivity


class Presence:
    def __init__(self, activity_type: int, activity_text: str):
        self.activity_type = ActivityType(activity_type)
        self.activity_text = activity_text

    @property
    def activity_class(self) -> Type[BaseActivity]:
        if self.activity_type is ActivityType.playing:
            return Game

        if self.activity_type is ActivityType.streaming:
            return Streaming

        if self.activity_type is ActivityType.custom:
            return CustomActivity

    def __str__(self):
        return f"Presence {self.activity_text} ({self.activity_type})"
