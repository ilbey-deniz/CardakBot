import discord
from discord.ext import commands
from discord import ClientException
import yt_dlp
from discord.ext import commands
from ytmusicapi import YTMusic
from service.music.playlist import Playlist
from service.music.song import Song
from service.music.utils import YTMusicUtils
import os

class YoutubeMusic(commands.Cog):
    def __init__(self, bot):
        self.ffmepg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        self.bot = bot
        self.ytmusic_utils = YTMusicUtils()
        self.ydl = yt_dlp.YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'})
        self.autoplay = True
        self.playlist = Playlist()

    @commands.Cog.listener()
    async def on_ready(self):
        print("YoutubeMusic cog is ready")

    @commands.command(name='p')
    async def play(self, ctx, *, arg):
        #join the channel of the typed user, if they are in one
        if ctx.author.voice:
            try:
                await ctx.author.voice.channel.connect()
            except ClientException:
                pass

        else:
            await ctx.send("You are not in a voice channel")
            return
        
        # search_results = self.ytmusic.search(query=arg, filter="songs")
        # song_video_id = search_results[0]["videoId"]
        # similar_songs = self.ytmusic.get_watch_playlist(song_video_id)
        # similar_songs = similar_songs["tracks"]
        # similar_songs = [song["videoId"] for song in similar_songs]
        #playlist.addPlaylist(similar_songs)
        
        #start a seperate thread to download the song and play it
        #this is so we can continue to take commands while the song is playing

        #change download location to "temp" folder and name the file the video id
        # ydl.download(["https://www.youtube.com/watch?v=" + playlist.getCurrentSong()])

        # voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        # voice.play(discord.FFmpegPCMAudio("temp/" + playlist.getCurrentSong() + ".webm"))
        
        self.playlist = self.ytmusic_utils.get_playlist_by_query(arg)
        song = self.playlist.next_song()
        
        video_url = song.url
        song_info = self.ydl.extract_info(video_url, download=False)
        song_info = self.ydl.sanitize_info(song_info)
        url = song_info['url']
        
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        try:
            voice.play(discord.FFmpegPCMAudio(url, **self.ffmepg_options))
            await ctx.send(f"Playing {song_info['title']} - {song_info['uploader']}")
        except ClientException as e:
            await ctx.send(e)
            pass
        
    @commands.command(name='s')
    async def stop(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        await voice.disconnect()

    @commands.command(name='n')
    async def next(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        song = self.playlist.next_song()
        video_url = song.url
        song_info = self.ydl.extract_info(video_url, download=False)
        song_info = self.ydl.sanitize_info(song_info)
        url = song_info['url']
        voice.play(discord.FFmpegPCMAudio(url, **self.ffmepg_options))
        await ctx.send(f"Playing {song_info['title']} - {song_info['uploader']}")

async def setup(bot):
    await bot.add_cog(YoutubeMusic(bot))