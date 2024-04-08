import discord
import sys
import json
import os
import asyncio
from discord.ext import commands
from discord.gateway import DiscordWebSocket, _log
async def identify(self):
    payload = {
        'op': self.IDENTIFY,
        'd': {
            'token': self.token,
            'properties': {
                '$os': sys.platform,
                '$browser': 'Discord Android',
                '$device': 'Discord Android',
                '$referrer': '',
                '$referring_domain': ''
            },
            'compress': True,
            'large_threshold': 250,
            'v': 3
        }
    }

    if self.shard_id is not None and self.shard_count is not None:
        payload['d']['shard'] = [self.shard_id, self.shard_count]
    state = self._connection
    if state._activity is not None or state._status is not None:
        payload['d']['presence'] = {
            'status': state._status,
            'game': state._activity,
            'since': 0,
            'afk': False
        }
    if state._intents is not None:
        payload['d']['intents'] = state._intents.value
    await self.call_hooks('before_identify', self.shard_id, initial=self._initial_identify)
    await self.send_as_json(payload)
    _log.info('Shard ID %s has sent the IDENTIFY payload.', self.shard_id)
DiscordWebSocket.identify = identify


def prefix(client, message):
    with open("data/prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]


intents = discord.Intents().default()
intents.members = True
intents.message_content = True
intents.messages = True
intents.dm_messages = True
client = commands.Bot(intents = intents, command_prefix = prefix, help_command = None, owner_ids = [1168186952772747364, 921148808551870484, 958607606241447936, 1163174089083592786])

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')       
@client.event
async def on_ready():
    await client.load_extension('jishaku')
    await load()
    print("""

██╗░░██╗███████╗░█████╗░████████╗███████╗██████╗░
██║░░██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
███████║█████╗░░███████║░░░██║░░░█████╗░░██║░░██║
██╔══██║██╔══╝░░██╔══██║░░░██║░░░██╔══╝░░██║░░██║
██║░░██║███████╗██║░░██║░░░██║░░░███████╗██████╔╝
╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═════╝░
""")

          

client.run('MTIxNTc3OTM0NTc5MzI4NjE5NA.Gf0HqK.WS9VMpbKUVTArBx_HnflH0E1jH5_J-SDgxA_aA')