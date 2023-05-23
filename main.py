import os
import re
import logging
import discord
import wavelink
import functools
from wavelink.ext import spotify
from discord.ext.commands import Context
from discord.ext import commands as command

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = command.Bot(command_prefix='-', intents=intents)
Client = discord.Client(intents = intents)
client.remove_command('help')


@client.event 
async def on_ready():
    print("En línea")
    await client.add_cog(Music(client))

    
class CustomPlayer(wavelink.Player):
    def __init__(self):
        super().__init__()
        self.queue = wavelink.Queue()

class Music(command.Cog):

    def __init__(self, bot: command.Bot):
        self.bot = bot
        self.song_queue = {}
        self.cid = '[CLIENT ID]'
        self.csecret = '[CLIENT SECRET]'
        bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Conecta a los nodos de Lavalink"""
        await self.bot.wait_until_ready()
        sc = spotify.SpotifyClient(
            client_id=self.cid, client_secret=self.csecret
        )
        node: wavelink.Node = wavelink.Node(
            uri='[HOST]', password='[PASSWORD]', secure=True)
        await wavelink.NodePool.connect(client=self.bot, nodes=[node], spotify=sc)

    @command.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):
        player = payload.player
        if not player.queue.is_empty:
            next_track = player.queue.get()
            await player.play(next_track)

    @command.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'El nodo: <{node}> está listo!')

    @command.command()
    async def join(self, ctx):
        vc = ctx.voice_client
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            return await ctx.send("No puedo unirme a un canal si tu no estás en uno previamente")
        if vc:
            await vc.disconnect()
        await channel.connect(cls=CustomPlayer())

    @command.command()
    async def leave(self, ctx):
        vc = ctx.voice_client
        if vc:
            await vc.disconnect()
        else:
            await ctx.send("¿Cómo puedo desconectarme cuando no estoy conectado?")

    @command.command()
    async def play(self, ctx: command.Context, *, search: str = command.parameter(
            description="Reproduce la canción (url o playlist). Agrega a la cola si la canción ya se está reproduciendo.")):
        """
        Reproduce la canción (url o playlist). Agrega a la cola si la canción ya se está reproduciendo.
        uso:
        !play <busqueda>
        """
        url_type = self.check_string(search)
        action = self.url_type_mapping.get(url_type, None)
        vc = ctx.voice_client
        if not vc:
            custom_player = CustomPlayer()
            vc: CustomPlayer = await ctx.author.voice.channel.connect(
                cls=custom_player)
        if action:
            await action(self, ctx, search, vc)
        else:
            # handle text input
            await ctx.send("no se enlace es ese. Vuelve a intentarlo.")

    @command.command()
    async def pause(self, ctx):
        """Pausa a la siguiente canción"""
        vc = ctx.voice_client
        if vc:
            if vc.is_playing() and not vc.is_paused():
                await vc.pause()
            else:
                await ctx.send("No está sonando nada")
        else:
            await ctx.send("El bot no está conectado a un canal de voz")

    @command.command()
    async def resume(self, ctx):
        """Reanuda la repoducción"""
        vc = ctx.voice_client
        if vc:
            if vc.is_paused():
                await vc.resume()
            else:
                await ctx.send("Nada está pausado")
        else:
            await ctx.send("El bot no está conectado a un canal de voz")

    @command.command()
    async def skip(self, ctx):
        """Pasa a la siguiente canción"""
        vc = ctx.voice_client
        if vc:
            if not vc.is_playing():
                return await ctx.send("Nada está soanando")
            if vc.queue.is_empty:
                return await vc.stop()

            await vc.seek(vc.current.length * 1000)
            if vc.is_paused():
                await vc.resume()
        else:
            await ctx.send("El bot no está conectado a un canal de voz")

    async def play_spotify_track(self, ctx: discord.ext.commands.Context, track: str, vc: CustomPlayer):
        track = await spotify.SpotifyTrack.search(track, return_first=True)
        if vc.is_playing() or not vc.queue.is_empty:
            vc.queue.put(item=track)
            await ctx.send(embed=discord.Embed(
                title=track.title,
                url=track.uri,
                description=f"Agregada {track.title} en\n <#{vc.channel.id}>"
            ))
        else:
            await vc.play(track)
            await ctx.send(embed=discord.Embed(
                title=track.title,
                url=track.uri,
                description=f"Agregada {track.title} en\n <#{vc.channel.id}>"
            ))

    async def play_spotify_playlist(self, ctx: discord.ext.commands.Context, playlist: str, vc: CustomPlayer):
        await ctx.send("Cargando Playlist")
        async for partial in spotify.SpotifyTrack.iterator(query=playlist):
            if vc.is_playing() or not vc.queue.is_empty:
                vc.queue.put(item=partial)
            else:
                await vc.play(partial)
                await ctx.send(embed=discord.Embed(
                    title=vc.current.title,
                    description=f"Sonando {vc.current.title} en\n <#{vc.channel.id}>"
                ))

    async def play_youtube_song(self, ctx: discord.ext.commands.Context, query: str, vc: CustomPlayer):
        try:
            query = re.sub(r'&t=\d+', '', query)
            track = await wavelink.NodePool.get_node().get_tracks(wavelink.YouTubeTrack, query)
            track = track[0]
            if vc.is_playing() or not vc.queue.is_empty:
                vc.queue.put(item=track)
                await ctx.send(embed=discord.Embed(
                    title=track.title,
                    url=track.uri,
                    description=f"agregada {track.title} en\n <#{vc.channel.id}>"
                ))
            else:
                await vc.play(track)
                await ctx.send(embed=discord.Embed(
                    title=vc.current.title,
                    url=vc.current.uri,
                    description=f"Sonando {vc.current.title} en\n <#{vc.channel.id}>"
                ))
        except Exception as e:
            await ctx.send(f"Ese vínculo es extraño. Asegúrese de que no haya una marca de tiempo al final.")

    async def play_youtube_playlist(ctx: discord.ext.commands.Context, playlist: str):
        pass

    async def play_query(self, ctx: discord.ext.commands.Context, search: str, vc: CustomPlayer):
        track = await wavelink.YouTubeTrack.search(search, return_first=True)
        if vc.is_playing() or not vc.queue.is_empty:
            vc.queue.put(item=track)
            await ctx.send(embed=discord.Embed(
                title=track.title,
                url=track.uri,
                description=f"Agregado {track.title} en\n <#{vc.channel.id}>"
            ))
        else:
            await vc.play(track)
            await ctx.send(embed=discord.Embed(
                title=vc.current.title,
                url=vc.current.uri,
                description=f"Agregado {vc.current.title} en\n <#{vc.channel.id}>"
            ))

    url_type_mapping = {
        'Spotify Track': play_spotify_track,
        'Spotify Playlist': play_spotify_playlist,
        'Spotify Album': play_spotify_playlist,
        'YouTube Song': play_youtube_song,
        'YouTube Playlist': play_youtube_playlist,
        'Text': play_query,
    }

    def check_string(self, input_string):

        youtube_pattern = re.compile(
            (r'https?://(www\.)?(youtube|youtu)(\.com|\.be)/'
             '(playlist\?list=|watch\?v=|embed/|)([a-zA-Z0-9-_]+)(\&t=\d+s)?'
             '|https://youtu.be/([a-zA-Z0-9-_]+)(\?t=\d+s)?'))
        spotify_pattern = re.compile(
            (r'https?://open\.spotify\.com/(album|playlist|track)'
             '/([a-zA-Z0-9-]+)(/[a-zA-Z0-9-]+)?(\?.*)?'))

        youtube_match = youtube_pattern.match(input_string)
        spotify_match = spotify_pattern.match(input_string)

        if youtube_match:
            return self.get_youtube_pattern(youtube_match)
        elif spotify_match:
            return self.get_spotify_pattern(spotify_match)
        return 'Text'

    def get_spotify_pattern(self, spotify_match):
        if spotify_match:
            if 'track' in spotify_match.group():
                return 'Spotify Track'
            elif 'playlist' in spotify_match.group():
                return 'Spotify Playlist'
            elif 'album' in spotify_match.group():
                return 'Spotify Album'
            else:
                return 'Spotify URL'

    def get_youtube_pattern(self, youtube_match):
        if youtube_match:
            if 'watch?v=' in youtube_match.group() or 'youtu.be' in youtube_match.group():
                return 'YouTube Song'
            elif 'playlist?list=' in youtube_match.group():
                return 'YouTube Playlist'
            else:
                return 'YouTube URL'

client.run("[BOT TOKEN]")

