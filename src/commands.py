from src.log import Logger
import re

class Commands:
    def __init__(self, uow, tasks, client):
        self.uow = uow
        self.tasks = tasks
        self.client = client
    
    @staticmethod
    async def can_execute(message):
        if not message.author.guild_permissions.administrator:
            await message.channel.send("You don't have access to this command")
            return False

        return True

    async def invalid_command(self, message, args=False):
        await message.channel.send('Sorry, something went wrong! Make sure your message is in the correct format.')

    async def hello(self, message, args=False):
        await message.channel.send('Hello there!')

    async def help_func(self, message, args=False):
        Logger.log_add(f'help_func()')
        m1 = '**To add/remove player:**\n`!player add/remove <ScoreSaber profile url/id> <discord user>`\n'
        m2 = '**To add/remove current channel:**\n`!channel add/remove`\n'
        m3 = '**To add/remove feature from Discord server:**\n`!feature add/remove [ppRoles]`\n'
        m4 = '**To update data:**\n`!update [players/roles/scores/notifications]`'
        msg = m1 + m2 + m3 + m4
        await message.channel.send(msg)

    async def player_func(self, message, args):
        Logger.log_add(f'player_func(message.content: {message.content}, args: {args})')

        async def add_player():
            if db_player in db_guild.players:
                await message.channel.send(f'Player ID {playerID} has already been added!')
                return

            new_player = self.uow.scoresaber.get_player(playerID)

            if new_player is None:
                await message.channel.send(f'Failed to add player!')
                return

            new_player.discord_user_id = discord_user_id

            self.uow.player_repo.add_player(new_player)
            self.uow.player_repo.add_to_guild(new_player.playerId, db_guild)

            # Get player scores and marked them sent to decrease spam
            await self.tasks.update_player_scores(new_player)
            await self.tasks.mark_all_player_scores_sent(new_player)

            # Add role to player if enabled
            if db_guild.pp_roles:
                await self.tasks.update_player_roles(db_guild, new_player)

            await message.channel.send(f'Player {new_player.playerName} successfully added!')
        
        async def remove_player():
            is_removed = False

            for db_player in db_guild.players:
                if playerID == db_player.playerId:
                    self.uow.guild_repo.remove_player(db_guild.discord_guild_id, db_player)
                    await self.tasks.remove_player_roles(db_guild, db_player)
                    await message.channel.send(f'Player ID {playerID} successfully removed!')
                    is_removed = True

            if not is_removed:
                await message.channel.send(f"Player ID {playerID} already doesn't exist in this Discord server's player list.")


        actiondict = {
            "add": add_player,
            "remove": remove_player
        }
        action = args[0]
        actionfunc = actiondict.get(action, False)
        if not actionfunc:
            message.channel.send(f'{action} is not an applicable action, possible actions are: {[i for i in actiondict]}')
            return
        
        guild_id = message.channel.guild.id
        try:
            pattern = re.compile(r'(https?://scoresaber\.com/u/)?(\d{17})')
            match = re.match(pattern, args[1])
            if match:
                playerID = match.group(2)
            else:
                await message.channel.send('ScoreSaber ID/URL in incorrect format.')
                return
        except IndexError:
            await message.channel.send('You need to provide a ScoreSaber profile ID/URL')
            return
        
        try:
            pattern = re.compile(r'<@!(\d+)>')
            match = re.match(pattern, args[2])
            if match:
                discord_user_id = args[2]
                # not sure if it is necessary to check if user id is real or exists in current guild
                # I think that should be handled by other functions (ppRoles function(s)?)
            else:
                await message.channel.send(f'Discord ID in incorrect format (received input was: {args[2]}). You can try omitting this argument if you just wanted to add yourself.')
                return
        except IndexError:
            discord_user_id = message.author.id


        Logger.log_add(f'player_func(guild_id: {guild_id}, playerID: {playerID}, discord_user_id: {discord_user_id}, action: {action})')

        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)
        db_player = self.uow.player_repo.get_player_by_player_id(playerID)

        await actionfunc()

    async def channel_func(self, message, args):
        if not await self.can_execute(message):
            return
        
        async def add_channel():
            if db_guild.recent_scores_channel_id is not None:
                await message.channel.send(f'Channel ID {message.channel.name} ({channel_id}) has already been added!')
                return

            self.uow.guild_repo.set_recent_score_channel_id(guild_id, channel_id)

            await self.tasks.mark_all_guild_scores_sent(db_guild)

            await message.channel.send(f'Channel ID {message.channel.name} ({channel_id}) successfully added!')
        async def remove_channel():
            if db_guild.recent_scores_channel_id is None:
                await message.channel.send(f"Channel ID {message.channel.name} ({channel_id}) already doesn't exist in the channel list for server {self.client.get_guild(guild_id)}.")
                return

            self.uow.guild_repo.set_recent_score_channel_id(guild_id, None)
            await message.channel.send(f'Channel ID {message.channel.name} ({channel_id}) successfully removed!')

        actiondict = {
            "add": add_channel,
            "remove": remove_channel
        }
        action = args[0]
        actionfunc = actiondict.get(action, False)
        if not actionfunc:
            message.channel.send(f'{action} is not an applicable action, possible actions are: {[i for i in actiondict]}')
            return
        
        channel_id = message.channel.id
        guild_id = message.channel.guild.id

        Logger.log_add(f'channel_func(channel: {channel_id}, guild: {guild_id}, action: {action})')
        db_guild = self.uow.guild_repo.get_guild_by_id(guild_id)

        await actionfunc()

    async def enable_feature(self, message, args):
        if not await self.can_execute(message):
            return
        
        async def add_feature():
            if feature_flag == "ppRoles":
                self.uow.guild_repo.set_feature(guild.id, feature_flag, True)
                await self.tasks.update_all_player_roles(guild)
                await message.channel.send("Enabled pp roles feature")
        
        async def remove_feature():
            if feature_flag == "ppRoles":
                self.uow.guild_repo.set_feature(guild.id, feature_flag, False)
                await self.tasks.remove_guild_roles(guild)
                await message.channel.send("Disabled pp roles feature")

        actiondict = {
            "add": add_feature,
            "remove": remove_feature
        }
        action = args[0]
        actionfunc = actiondict.get(action, False)
        if not actionfunc:
            await message.channel.send(f'{action} is not an applicable action, possible actions are: {[i for i in actiondict]}')
            return
        
        featurelist = [
            "ppRoles"
        ]
        feature_flag = args[1]
        if feature_flag not in featurelist:
            await message.channel.send(f'{feature_flag} is not an applicable action, possible actions are: {[i for i in featurelist]}')
            return
        
        guild = message.channel.guild

        await actionfunc()

    async def run_task(self, message, args=False):
        if not await self.can_execute(message):
            return

        actiondict = {
            "players": self.tasks.update_players,
            "roles": self.tasks.update_all_player_roles,
            "scores": self.tasks.update_players_scores,
            "notifications": self.tasks.send_notifications
        }
        if args:
            action = args[0]
            actionfunc = actiondict.get(action, False)
            if not actionfunc:
                await message.channel.send(f'{action} is not an applicable action, possible actions are: {[i for i in actiondict]}')
                return
        else:
            async def actionfunc(guild):
                await self.tasks.update_players(guild)
                await self.tasks.update_all_player_roles(guild)
                await self.tasks.update_players_scores(guild)
                await self.tasks.send_notifications(guild)

        Logger.log_add(f'update(guild: {message.guild}, args: {args})')
        await actionfunc(message.guild)

    async def get_pp(self, message, args=False):
        Logger.log_add(f'get_pp() ran by {message.author.name} ({message.author.id} in {message.channel.guild})')
        try:
            db_player = self.uow.guild_repo.get_player_by_discord_id(message.channel.guild, message.author.id)
            pp_size = round(db_player.pp / 100)
            await message.channel.send(f"{message.author.name}'s PP is this big:\n8{'=' * pp_size}D")
        except Exception as e:
            Logger.log_add(f'Exception {e} in get_pp(), message.content: {message.content}, author: {message.author}')
    

    async def command(self, message, command, args):
        command_dict = {
            "hello": [self.hello, 0],
            "help": [self.help_func, 0],
            "player": [self.player_func, 2],
            "channel": [self.channel_func, 1],
            "feature": [self.enable_feature, 2],
            "update": [self.run_task, 0],
            "showpp": [self.get_pp, 0]
        }
        func, required_args = [i for i in command_dict.get(command, [self.invalid_command, 0])]
        if len(args) >= required_args:
            await func(message, args)
        else:
            await message.channel.send(f'The {command} command requires {required_args} arguments')