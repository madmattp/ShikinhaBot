# Made by madmattp (https://github.com/madmattp)

import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure
from wikipedia import random, page, summary, set_lang
import asyncio
from random import choice
from e621 import E621
from rule34Py import rule34Py
import openai
import wavelink
import secret  # API keys and the Lavalink server credentials

tok = secret.disc_token # Discord API token

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=";", intents=intents)
client.remove_command('help')

openai.api_key = secret.openai_token  # OpenAi API (DALL-E e ChatGPT)

set_lang("pt") # Wikipedia API

@client.event
async def on_ready(): # Boot message
    client.loop.create_task(connect_nodes())
    change_status.start()
    print("=========================")
    print(f" Running Shikinha...")
    print(f" Ping {round(client.latency * 1000)}ms")
    print("=========================")

@tasks.loop(minutes=4)
async def change_status():
    sts = {1:[discord.ActivityType.playing, ";help 📜"],
        2:[discord.ActivityType.watching, "a vida passar 🍃"],
        3:[discord.ActivityType.watching, "A Revolução das maquinas 🤖"], 
        4:[discord.ActivityType.listening, "uma ligação do Putin 📞"],
        5:[discord.ActivityType.watching, "o mundo queimar 🔥"],
        6:[discord.ActivityType.listening, "RADIOHEAD 🎵🔥"],
        7:[discord.ActivityType.playing, "SNAKE 🐍"],
        8:[discord.ActivityType.playing, "o lixo fora 🚮"]}
    chosen_state = sts[choice(range(1, len(sts) + 1))]
    
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=chosen_state[0], name=chosen_state[1]))

async def main():
    print("Booting...")
    await client.start(tok)

class CustomPlayer(wavelink.Player):
    def __init__(self):
        super().__init__()
        self.queue = wavelink.Queue()

async def connect_nodes():
    await client.wait_until_ready()
    await wavelink.NodePool.create_node(
        bot=client,
        host=secret.host,
        port=secret.port,
        password=secret.wv_node_password
    )

@client.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f'Node: <{node.identifier}> is ready!')

@client.event
async def on_wavelink_track_end(player: CustomPlayer, track: wavelink.Track, reason):
    if not player.queue.is_empty:
        next_track = player.queue.get()
        await player.play(next_track)

############# ACTUAL COMMANDS #########################

@client.command(aliases=["h"])
async def help(ctx):
    embed = discord.Embed(
        title = ":sparkles: COMANDOS :sparkles: ",
        description=" (Meu prefixo é ';')",
        colour = discord.Colour.from_rgb(177, 164, 154)
    )
    embed.set_footer(text=f"Shikinha")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/767002076257452053/758bef70a617ebb543bcf154341a5e5a.png?size=1024")
    embed.add_field(name="help", value="● Retorna a minha lista de Comandos.", inline=False)
    embed.add_field(name="clear <num>", value="● Apaga quantia <num> de mensagens.\n__(Necessária a permissão de gerenciar mensagens)__", inline=False)
    embed.add_field(name="wiki <pesquisa>", value="● Retorna sumário da página da wikipédia sobre <pesquisa>.", inline=False)
    embed.add_field(name="random_wiki", value="● Retorna sumário de uma página aleatória da wikipedia.", inline=False)
    embed.add_field(name="ping", value="● Retorna a latência em milissegundos.", inline=False)
    embed.add_field(name="gpt <prompt>", value="● Interage com ChatGPT da OpenAI", inline=False)
    embed.add_field(name="dalle <prompt>", value="● Gera uma imagem baseada no prompt <prompt> usando a DALL-E da OpenAI", inline=False)
    embed.add_field(name="rule34 <tags>   (NSFW)", value="● Pesquisa um post aleatório no Rule34 que possua as tags <tags>.", inline=False)
    embed.add_field(name="e621 <tags>     (NSFW)", value="● Pesquisa um post aleatório no E621 que possua as tags <tags>.", inline=False)
    embed.add_field(name="connect", value='● Conecta o bot ao canal de voz.', inline=False)
    embed.add_field(name="disconnect", value='● Desconecta o bot do canal de voz.', inline=False)
    embed.add_field(name="play <nome/link>", value="● Busca pelo Youtube pelo áudio desejado (<nome/link>).", inline=False)
    embed.add_field(name="skip", value="● Pula para o próximo áudio.", inline=False)
    embed.add_field(name="pause", value="● Pausa o áudio atual.", inline=False)
    embed.add_field(name="resume", value="● Retoma o áudio atual.", inline=False)

    await ctx.message.add_reaction("📜")
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! **{round(client.latency * 1000)}ms**")

@client.command(aliases=["c"])  
@has_permissions(manage_messages=True)
async def clear(ctx, *, amount):
    try:
        amount = int(amount)
        if(amount < 51):
            await ctx.channel.purge(limit=amount)
            await ctx.send(f"{amount} mensagem(ns) apagada(s) por {ctx.message.author.mention}")
        else:
            await ctx.message.add_reaction("❗")
            await ctx.send("O parâmetro para o comando deverá ser um número inteiro menor que 50.")
    except Exception as e:
        print(e)
        await ctx.message.add_reaction("🛑")
        await ctx.send("Parâmetro inválido! O parâmetro não é um número inteiro.")

@client.command(aliases=["w"])  
async def wiki(ctx, *, pesquisa):
    await ctx.send("Um segundinho...")
    try:
        sugest = pesquisa
        await ctx.send(f"** #=- {page(sugest).title} -=#**\n {summary(sugest, sentences=3)} [...] \n \n Clique para ler mais: {page(sugest).url}")
    except:
        await ctx.send("Algo deu errado.\nSeu parâmetro não existe ou é muito 'vago'")

@client.command(aliases=["rw"])
async def random_wiki(ctx):
    await ctx.send("Um segundinho...")
    sugest = random(pages=1)
    await ctx.send(f"** #=- {sugest} -=#**\n {summary(sugest, sentences=3)} [...] \n \n Clique para ler mais: {page(sugest).url}")

@client.command(aliases=["e621"])  # NSFW
async def e6(ctx, *, tags):
    api = E621()

    posts = api.posts.search(f"{str(tags)} -webm")
    post = choice(posts)
    img = post.file_obj.url
    
    tags_obj = post.tags
    tags = tags_obj.general + tags_obj.species + tags_obj.character + tags_obj.copyright + tags_obj.invalid + tags_obj.lore + tags_obj.artist
    tags = " ".join(tags)

    embed = discord.Embed(colour = discord.Colour.from_rgb(2, 54, 102))
    embed.set_image(url=f"{img}")
    embed.set_footer(text=f"Tags: {tags}")

    await ctx.send(embed=embed)

@client.command(aliases=["rule34", "r3"])  # NSFW
async def r34(ctx, *, tags):
    tags = tags.split()

    while("video" in tags):
        tags.remove("video")
    tags.append("-video")
    
    r34Py = rule34Py()

    result_random = r34Py.random_post(tags)
    img = result_random.image
    tags = result_random._tags   
    tags = " ".join(tags)

    embed = discord.Embed(colour = discord.Colour.from_rgb(170, 229, 164))
    embed.set_image(url=f"{img}")
    embed.set_footer(text=f"Tags: {tags}")
    
    await ctx.send(embed=embed)

@client.command(aliases=["img", "dall-e"])  # OpenAI DALL-E
async def dalle(ctx, *, prompt):
    try:
        response = openai.Image.create(
        prompt=str(prompt),
        n=1,
        size="1024x1024"
        )
        image_url = response['data'][0]['url']

        await ctx.reply(image_url)
    except Exception as e:
        await ctx.reply(f'{e}')

@client.command(aliases=["gpt-3", "chat", "chatgpt"])   # OpenAI ChatGPT
async def gpt(ctx, *, prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"{prompt}"}],
            temperature=0.9,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1, 
        )
        text = completion.choices[0].message["content"]
        if len(text) <= 2000:  
            await ctx.reply(str(text))
        else:   # If the message is too long, it will split the output in two parts and send them individually
            met = int(len(text) / 2)
            met1 = met + 1
            await ctx.reply(str(text[0:met]))
            await ctx.send(str(text[met1:len(text)]))
    except Exception as e:
        await ctx.reply(str(e))


###### MUSIC STUFF #######

@client.command(aliases=["conectar"])
async def connect(ctx):
    vc = ctx.voice_client # represents a discord voice connection
    try:
        channel = ctx.author.voice.channel
    except AttributeError:
        return await ctx.send("Entre num canal de voz antes de me chamar!")

    if not vc:
        await ctx.author.voice.channel.connect(cls=CustomPlayer())
    else:
        await ctx.send("Já estou conectado num canal de voz!")

@client.command(aliases=["desconectar"])
async def disconnect(ctx):
    vc = ctx.voice_client
    if vc:
        await vc.disconnect()
    else:
        await ctx.send("Não estou conectado num canal de voz!")

@client.command(aliases=["p", "tocar"])
async def play(ctx, *, search: wavelink.YouTubeTrack):
    vc = ctx.voice_client
    if not vc:
        custom_player = CustomPlayer()
        vc: CustomPlayer = await ctx.author.voice.channel.connect(cls=custom_player)

    if vc.is_playing():
        vc.queue.put(item=search)

        embed = discord.Embed(
            title="✋ Na fila...",
            description=f"{search.title}",
            colour = discord.Colour.from_rgb(255, 220, 93))
        embed.set_thumbnail(url=f"{search.thumbnail}")
        await ctx.message.add_reaction("🎶")
        await ctx.reply(embed=embed)
        
        embed = discord.Embed(
            title="Fila:",
            colour = discord.Colour.from_rgb(255, 220, 93),
            description="")

        index = 0    
        for track in vc.queue:
            embed.description += f"[{index}] - {track.title}\n"
            index += 1

        await ctx.send(embed=embed)

    else:
        await vc.play(search)

        embed = discord.Embed(
            title="🎙️ 🎶 Tocando agora...",
            description=f"{search.title}",
            colour = discord.Colour.from_rgb(93, 173, 236))
        embed.set_thumbnail(url=f"{search.thumbnail}")
        await ctx.message.add_reaction("🎶")
        await ctx.reply(embed=embed)

@client.command(aliases=['s', 'pular'])
async def skip(ctx):
    vc = ctx.voice_client
    if vc:
        await ctx.message.add_reaction("⏭️")
        if not vc.is_playing():
            return await ctx.send("Nada está tocando...")
        if vc.queue.is_empty:
            return await vc.stop()

        await vc.seek(vc.track.length * 1000)
        if vc.is_paused():
            await vc.resume()
        
    else:
        await ctx.send("Não estou conectado num canal de voz!")

@client.command(aliases=['pausa', 'stop'])
async def pause(ctx):
    vc = ctx.voice_client
    if vc:
        if vc.is_playing() and not vc.is_paused():
            await vc.pause()
            await ctx.message.add_reaction("⏸️")
        else:
            await ctx.send("Nada está tocando...")
    else:
        await ctx.send("Não estou conectado num canal de voz!")

@client.command(aliases=['unpause', 'voltar', 'continuar'])
async def resume(ctx):
    vc = ctx.voice_client
    if vc:
        if vc.is_paused():
            await ctx.message.add_reaction("▶️")
            await vc.resume()
        else:
            await ctx.send("Nada está pausado...")
    else:
        await ctx.send("Não estou conectado num canal de voz!")

@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Não consegui achar o que você queria... Desculpa 😥")    

asyncio.run(main())
