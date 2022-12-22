import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib.request
import requests
import lxml.html
from pymongo import MongoClient
from datetime import datetime
import re

def get_database():
    # This function connects to the MongoDB database using the provided connection string and returns the database object
    CONNECTION_STRING = "mongodb+srv://discord:discord@cluster0.jjo7hnp.mongodb.net/?retryWrites=true&w=majority"
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)
    db_name = "kamisama"
    db = client[db_name]
    print('Connected to MongoDB')
    return db

# Get the database
dbname = get_database()

# Connect to MongoDB
db_anime = dbname['anime']

def retrievAllAnimesOfSinglePage():
    # This function iterates through a list of elements and retrieves information about each anime
    for n in range(len(elements)):
        title = elements[n].h3.a.text
        link = elements[n].h3.a.get('href')
        query = {"name_en": title}
        document = db_anime.find(query)
        error = False
        try:
            document[0]
        except:
            error = True
        if error == False:
            # If the document for the anime already exists in the database, retrieve its status
            rep = document[0]
            status = rep['status']
            if status != "Terminé":
                # If the anime is not finished airing in the database, retrieve more information about it
                response = requests.get(link)
                soup2 = bs(response.text, "html.parser")
                items2 = soup2.find(class_='title-name h1_bold_none').find('strong').text
                parent = soup2.findAll("div","spaceit_pad")
                statusLink = ((((parent[5].text).replace("\n", "")).replace(" ", "")).split(":"))[1]
                firstDate = ""
                secondDate = ""
                episodes = ""
                # In fuction of airing of the anime in site retrive differnet information
                if statusLink == "CurrentlyAiring":
                    statusLink = "En cours"
                    episodes = ((((parent[4].text).replace("\n", "")).replace(" ", "")).split(":"))[1]
                    aired = (((parent[6].text).replace("\n", "")).split(":")[1]).split("to")
                    firstDate = (aired[0].strip()).replace(",", "")
                    secondDate = (aired[1].strip()).replace(",", "")
                    #Format the start date and the end date if exist and doesnt egal ?
                    if firstDate != "?" and firstDate != "":
                        full_month_date = firstDate
                        full_month_format = "%b %d %Y"
                        try:
                            firstDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%d-%m-%Y')
                        except:
                            firstDate = (aired[0].strip()).replace(",", "")
                            full_month_date = firstDate
                            full_month_format = "%b %Y"
                            try:
                                firstDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%m-%Y')
                            except:
                                firstDate = firstDate.split()
                                full_month_date = firstDate
                                full_month_format = "%Y"
                                try:
                                    firstDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%Y')
                                except:
                                    firstDate = ""
                    if secondDate != "?" and secondDate != "":
                        full_month_date = secondDate
                        full_month_format = "%b %d %Y"
                        try:
                            secondDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%d-%m-%Y')
                        except:
                            secondDate = (aired[0].strip()).replace(",", "")
                            full_month_date = secondDate
                            full_month_format = "%b %Y"
                            try:
                                secondDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%m-%Y')
                            except:
                                secondDate = secondDate.split()
                                full_month_date = secondDate
                                full_month_format = "%Y"
                                try:
                                    secondDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%Y')
                                except:
                                    secondDate = ""
                elif statusLink == "FinishedAiring":
                    statusLink = "Terminé"
                    episodes = ((((parent[4].text).replace("\n", "")).replace(" ", "")).split(":"))[1]
                    aired = (((parent[6].text).replace("\n", "")).split(":")[1]).split("to")
                    firstDate = (aired[0].strip()).replace(",", "")
                    secondDate = (aired[1].strip()).replace(",", "")
                    if firstDate != "?" and firstDate != "":
                        full_month_date = firstDate
                        full_month_format = "%b %d %Y"
                        try:
                            firstDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%d-%m-%Y')
                        except:
                            firstDate = (aired[0].strip()).replace(",", "")
                            full_month_date = firstDate
                            full_month_format = "%b %Y"
                            try:
                                firstDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%m-%Y')
                            except:
                                firstDate = firstDate.split()
                                full_month_date = firstDate
                                full_month_format = "%Y"
                                try:
                                    firstDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%Y')
                                except:
                                    firstDate = ""
                    if secondDate != "?" and secondDate != "":
                        full_month_date = secondDate
                        full_month_format = "%b %d %Y"
                        try:
                            secondDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%d-%m-%Y')
                        except:
                            secondDate = (aired[0].strip()).replace(",", "")
                            full_month_date = secondDate
                            full_month_format = "%b %Y"
                            try:
                                secondDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%m-%Y')
                            except:
                                secondDate = secondDate.split()
                                full_month_date = secondDate
                                full_month_format = "%Y"
                                try:
                                    secondDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%Y')
                                except:
                                    secondDate = ""
                elif statusLink == "Notyetaired":
                    statusLink = "Pas encore diffusé"
                    firstDate = (aired[0].strip()).replace(",", "")
                    if firstDate != "?" and firstDate != "":
                        full_month_date = firstDate
                        full_month_format = "%b %d %Y"
                        try:
                            firstDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%d-%m-%Y')
                        except:
                            firstDate = (aired[0].strip()).replace(",", "")
                            full_month_date = firstDate
                            full_month_format = "%b %Y"
                            try:
                                firstDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%m-%Y')
                            except:
                                firstDate = firstDate.split()
                                full_month_date = firstDate
                                full_month_format = "%Y"
                                try:
                                    firstDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%Y')
                                except:
                                    firstDate = ""
                # Update anime informations in database based of his name
                db_anime.update_one(
                    {"name_en": title},
                    {"$set": {"status": statusLink, "nb_episodes": episodes, "date_sortie": firstDate,
                              "date_dernier_episode": secondDate}}, )
            else:
                # If the anime isn't in a database
                response = requests.get(link)
                # Go on the anime page in retrive all informatiosn for insert anime in database
                soup2 = bs(response.text, "html.parser")
                title2 = soup2.find(class_='title-name h1_bold_none').find('strong').text
                nameLower = (title2.lower()).replace(" ", "")
                parent = soup2.findAll("div", "spaceit_pad")
                picture = ((((soup2.find(class_='leftside')).div).a).img).get('data-src')
                synopsis = (soup2.find(itemprop="description"))
                #  None values must be empty
                statusLink = ""
                aired = ""
                episodes = ""
                genresLink = ""
                themesLink = ""

                for i in range(len(parent)):
                    testVariable = ((((parent[i].text).replace("\n", "")).replace(" ", "")).split(":"))[0]
                    if testVariable == "Status":
                        statusLink = ((((parent[i].text).replace("\n", "")).replace(" ", "")).split(":"))[1]
                    elif testVariable == "Aired":
                        aired = (((parent[i].text).replace("\n", "")).split(":")[1]).split("to")
                    elif testVariable == "Episodes":
                        episodes = ((((parent[i].text).replace("\n", "")).replace(" ", "")).split(":"))[1]
                    elif testVariable == "Genres":
                        genresLink = parent[i].findAll('a')
                    elif testVariable == "Genre":
                        genresLink = parent[i].findAll('a')
                    elif testVariable == "Themes":
                        themesLink = parent[i].findAll('a')
                    elif testVariable == "Theme":
                        themesLink = parent[i].findAll('a')

                if statusLink == "CurrentlyAiring":
                    statusLink = "En cours"
                elif statusLink == "FinishedAiring":
                    statusLink = "Terminé"
                elif statusLink == "Notyetaired":
                    statusLink = "Pas encore diffusé"

                firstDate = ""
                secondDate = ""

                # Verify the different format of date
                if len(aired) == 1:
                    firstDate = (aired[0].strip()).replace(",", "")
                elif len(aired) == 2:
                    firstDate = (aired[0].strip()).replace(",", "")
                    secondDate = (aired[1].strip()).replace(",", "")
                else:
                    firstDate = ""
                    secondDate = ""

                if firstDate != "?" and firstDate != "":
                    full_month_date = firstDate
                    full_month_format = "%b %d %Y"
                    try:
                        firstDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%d-%m-%Y')
                    except:
                        firstDate = (aired[0].strip()).replace(",", "")
                        full_month_date = firstDate
                        full_month_format = "%b %Y"
                        try:
                            firstDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%m-%Y')
                        except:
                            firstDate = firstDate.split()
                            full_month_date = firstDate
                            full_month_format = "%Y"
                            try:
                                firstDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%Y')
                            except:
                                firstDate = ""

                if secondDate != "?" and secondDate != "":
                    full_month_date = secondDate
                    full_month_format = "%b %d %Y"
                    try:
                        secondDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%d-%m-%Y')
                    except:
                        secondDate = (aired[0].strip()).replace(",", "")
                        full_month_date = secondDate
                        full_month_format = "%b %Y"
                        try:
                            secondDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%m-%Y')
                        except:
                            secondDate = secondDate.split()
                            full_month_date = secondDate
                            full_month_format = "%Y"
                            try:
                                secondDate = (datetime.strptime(full_month_date, full_month_format)).strftime('%Y')
                            except:
                                secondDate = ""
                # Retrive synopsis and the length doesn't is more than of 1024 caracters (a condition for the bot display)
                realSynopsis = ""
                for e in synopsis:
                    if len(e.text) != 0:
                        if len(e.text) != 1:
                            realSynopsis = realSynopsis + e.text
                realSynopsis = (re.sub("\[[^\]]*\]", "", realSynopsis)).strip()
                if len(realSynopsis) > 1024:
                    realSynopsis = realSynopsis[0:1024]
                    realSynopsis = (re.sub("[ \w]*$", "", realSynopsis)).strip()

                genres = []
                for e in genresLink:
                    genres.append(e.text)

                themes = []
                for e in themesLink:
                    themes.append(e.text)

                arrayLink = []
                try:
                    linkLink = soup2.findAll("div", "broadcast")
                    for element in linkLink:
                        url = (element.a).get('href')
                        nameUrl = ((element.a).div).text
                        object = {"nom:": nameUrl, "image": "", "url": url}
                        arrayLink.append(object)
                except:
                    arrayLink = []

                # Insert in Mongo Database
                db_anime.insert_one(
                    {"name_en": title2, "image": picture, "synopsis": realSynopsis, "genres": genres, "themes": themes,
                     "status": statusLink, "nb_episodes": episodes, "liens": arrayLink, "date_sortie": firstDate,
                     "date_dernier_episode": secondDate, "name_lower": nameLower})
# Define 2 count for launch an infinte loop
compteur = 0;
secondCompteur = -1;
globalError = False
while compteur > secondCompteur:
    # infinite loop for retrieve all animes on all pages of the site
    url = "https://myanimelist.net/topanime.php?limit=" + str(compteur)
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    elements = soup.findAll("div", 'detail')
    try:
        # Verify if there are elements to recover on the page
        retrievAllAnimesOfSinglePage();
    except:
        globalError = True
    if globalError == True:
        # If there are no elements on the page, we exit the loop
        print("Error" + str(compteur))
        break
        compteur = compteur + 50
        print(compteur)
        secondCompteur = secondCompteur + 50
        soup.clear()
    elif globalError == False:
        print("RetrieveTerminated")