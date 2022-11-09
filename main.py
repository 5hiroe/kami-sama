import random
import unidecode
import discord
import Paginator
from discord.ext import commands
from pymongo import MongoClient

# Remove accents and special characters from a string (for the search)
def formatText(text):
    newText = unidecode.unidecode(text).lower()
    newText.replace(" ", "")
    newText.replace("-", "")
    newText.replace("_", "")
    newText.replace("'", "")
    return newText

# Create the Discord Embed for a given card
def createEmbed(anime):
    genres = " - ".join(anime['genres'])
    themes = " - ".join(anime['themes'])
    embed = discord.Embed(title=anime['name_en'], color=random.choice(colors))
    
    embed.add_field(name= "Status", value= anime['status'],  inline= True)
    embed.add_field(name= "Episodes", value= anime['nb_episodes'], inline= True)
    embed.add_field(name= "Synopsis", value= anime['synopsis'], inline= False)
    embed.add_field(name= "First Episode", value= anime['date_sortie'], inline= True)
    embed.add_field(name= "Last Episode", value= anime['date_dernier_episode'], inline= True)
    embed.add_field(name= "Themes",  value= themes, inline= False)
    embed.add_field(name= "Genres", value= genres, inline= False)

    embed.set_image(url=anime['image'])
    return embed


# Connect to MongoDB
client = MongoClient('mongodb+srv://discord:discord@cluster0.jjo7hnp.mongodb.net/?retryWrites=true&w=majority')
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
    await ctx.send('Je suis là pour vous aider !')

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
    for anime in db_anime.find({'themes': formatText(theme_name)}):
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
    for anime in db_anime.find({'genres': formatText(genre_name)}):
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
    for anime in db_anime.find({'name_lower': formatText(name)}): 
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
    for anime in db_anime.aggregate([ { "$sample": { "size": 5 } } ]):
        embed = embed = createEmbed(anime)
        liste.append(embed)
    
    if len(liste) > 0:
        await ctx.send("Fellin' Lucky? Voici 5 animés sélectionnés au hasard, J'espère qu'ils te plairont! 😘 :")
        await Paginator.Simple().start(ctx, pages=liste)
    else:
        await ctx.send('Aucun anime ne correspond à ce nom')


# Run the bot
bot.run('MTAzOTgyMTUyMTM4NTk1MTMwNA.G-TRi8.BZn-KXTJg_nCDpjlu6LkcsWbKhhSKL1G0T6KWI')
