import random

import discord
import Paginator
import unidecode
from discord.ext import commands
from pymongo import MongoClient

# Create the Discord Embed for a given card
def createEmbed(anime):
    genres = " - ".join(anime['genres'])
    embed = discord.Embed(title=anime['name_en'], color=random.choice(colors))

    embed.add_field(name= "Status", value= anime['status'],  inline= True)
    embed.add_field(name= "Episodes", value= anime['nb_episodes'], inline= True)
    embed.add_field(name= "Synopsis", value= anime['synopsis'], inline= False)
    if (anime['date_sortie'] != ''):
        embed.add_field(name= "First Episode", value= anime['date_sortie'], inline= True)
    if (anime['date_dernier_episode'] != ''):
        embed.add_field(name= "Last Episode", value= anime['date_dernier_episode'], inline= True)
    if (len(anime['themes']) > 0):
        themes = " - ".join(anime['themes'])
        embed.add_field(name= "Themes",  value= themes, inline= False)
    embed.add_field(name= "Genres", value= genres, inline= False)

    embed.set_image(url=anime['image'])
    return embed


# Connect to MongoDB
client = MongoClient('SuperCoolMongoAddress')
db = client['kamisama']
print('Connected to MongoDB')
db_anime = db['anime']

# Color Array (for the embeds)
colors = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000, 0x4682B4, 0x006400, 0x808080, 0xA0522D, 0xF08080, 0xC71585, 0xFFB6C1, 0x00CED1]

#Init the bot (with the right prefix and intents)
bot = commands.Bot(command_prefix='!kami ', intents=discord.Intents.all())

# When the bot is ready
@bot.event
async def on_ready():
    print('Je suis disposée à vous aider !')

# Command to get informations about the bot
@bot.command()
async def info(ctx):
    await ctx.send('Bonjour, je suis la déesse des animés, mais tu peux m\'appeler Kami-sama !\n\nVoici la liste des prières à effectuer pour user de mes (incroyales) services :\n\n- **!kami info** : Pour en savoir plus sur ta déesse préférée 🙏♥️\n- **!kami all** : Pour avoir la liste de tous les animés disponibles 📚\n- **!kami theme <thème>** : Pour avoir la liste des animés correspondant au thème demandé 🎭\n- **!kami genre <genre>** : Pour avoir la liste des animés correspondant au genre demandé 🏳️‍🌈\n- **!kami name <nom>** : Pour trouver un animé en fonction de son nom 🫵\n- **!kami lucky** : Pour avoir 10 animés au hasard (et faire de bonnes découvertes) 🎲\n- **!kami secret** : Pour que je te partage un secret connu des Dieux seulement ! 🤫\n\n\nSi tu as des questions, n\'hésite pas à me contacter !\nTrès bonne recherche à toi, Shōnen ! 🌸😇🌸')

# Command to list all the animes in the database
@bot.command()
async def all(ctx):
    liste=[]
    for anime in db_anime.find():
        embed = createEmbed(anime)
        liste.append(embed)

    if len(liste) > 0:
        await ctx.send('Voici la liste de tous les animes disponibles :')
        await Paginator.Simple().start(ctx, pages=liste)
    else:
        await ctx.send('Aucun anime ne correspond à ce thème')

# Command to search an anime by theme
@bot.command()
async def theme(ctx, *, theme_name):
    liste=[]
    for anime in db_anime.find({'themes': { '$regex': theme_name, '$options': 'i' }}):
        embed = embed = createEmbed(anime)
        liste.append(embed)
    
    if len(liste) > 0:
        await ctx.send('Voici la liste des animes correspondant au thème demandé :')
        await Paginator.Simple().start(ctx, pages=liste)
    else:
        await ctx.send('Aucun anime ne correspond à ce thème')

# Command to search an anime by genre
@bot.command()
async def genre(ctx, *, genre_name):
    liste=[]
    for anime in db_anime.find({'genres': { '$regex': genre_name, '$options': 'i' }}):
        embed = embed = createEmbed(anime)
        liste.append(embed)

    if len(liste) > 0:
        await ctx.send('Voici la liste des animes correspondant au genre demandé :')
        await Paginator.Simple().start(ctx, pages=liste)
    else:
        await ctx.send('Aucun anime ne correspond à ce genre')

# Command to search an anime by name
@bot.command()
async def name(ctx, *, name):
    liste=[]
    # re.compile((name), re.IGNORECASE
    for anime in db_anime.find({'name_en': { '$regex': name, '$options': 'i' }}): 
        embed = embed = createEmbed(anime)
        liste.append(embed)
    
    if len(liste) > 0:
        await ctx.send('Voici la liste des animes correspondant au nom demandé :')
        await Paginator.Simple().start(ctx, pages=liste)
    else:
        await ctx.send('Aucun anime ne correspond à ce nom')

# Command to get 5 random animes
@bot.command()
async def lucky(ctx):
    liste=[]
    for anime in db_anime.aggregate([ { "$sample": { "size": 10 } } ]):
        embed = embed = createEmbed(anime)
        liste.append(embed)
    
    if len(liste) > 0:
        await ctx.send("Fellin' Lucky? Voici 10 animés sélectionnés au hasard, J'espère qu'ils te plairont! 😘 :")
        await Paginator.Simple().start(ctx, pages=liste)
    else:
        await ctx.send('Aucun anime ne correspond à ce nom')

# Troll Command 1
@bot.command()
async def tg(ctx):
    await ctx.send('https://tenor.com/view/judging-really-huh-judgingyou-gif-4584562')

# Troll Command 2
@bot.command()
async def secret(ctx):
    await ctx.send('https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713')
    
# Run the bot
bot.run('SuperCoolDiscordBotKey')
