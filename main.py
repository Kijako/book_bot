import os
import discord
#from dotenv import load_dotenv
import requests
import json
from pprint import pprint

from books import *
from Pattern import *
from RecommendedSystem import *

import random

pattern_dict = Create_Pattern()


# from BotFile import *

# botModel()
#from NLU_rasa import *

# TOKEN ='OTUyODQ0MDgyNTY3MzQ4Mjg3.Yi77NA.YPkFAAWFEOkQ8XeTNHMZ7AMU_Es'

#We used these variables with Replit, but had to change them when we started working local for the recommendation

# TOKEN = os.environ['DISCORD_TOKEN']
# GUILD = os.environ['DISCORD_GUILD']
# BOOKS_KEY = os.environ['GOOGLE_BOOKS_KEY']

TOKEN = 'OTUyODQ0MDgyNTY3MzQ4Mjg3.Yi77NA.YPkFAAWFEOkQ8XeTNHMZ7AMU_Es'
GUILD = 'TheBookServer'
BOOKS_KEY = 'AIzaSyCi2GBSO-PA-sf65Zvl7J6hRMXt9cdZ4_Q'

#load_dotenv()

client = discord.Client()

### HERE WE CREATE THE DIFFERENTS VARIABLES ###


# global actual_book
actual_book =""

# global liste_intent
liste_intent = []

# global boolReco
boolReco = False

helloList = ['Hello my friend','Hello amigo','Hello!', 'Hi', 'Hi!']
goodbyeList = ['Bye my friend','goodbye.','See you soon!', 'Bye-Bye!', 'GoodBye!']

# RecommendedSystem :
final_rating, model, book_pivot, books = CreateNewModel()
# print(final_rating)

def answerToIntent(intent):

  global actual_book
  # if we received a hello
  if intent[0] == 'Hello':
    res = str(random.choice(helloList)) + ''',

    Here are a few explanations to use this e-book bot :
    This bot can be useful in 2 specific situations : 

    1. You have read a book that you liked and you want some other 
       suggestions related to this specific book.
    2. You want to chat with me about any books, I am happy to help you find some informations.

    In case you find yourself in the second situation, I can find these informations for you :

        \u2022  Price,
        \u2022  Description,
        \u2022  Author(s),
        \u2022  Number of pages

    You can also use the keyword 'help' if you need any help on how to forumlate your questions !
    '''
    return res
  # if we received a goodbye
  elif intent[0] == 'Exit':
    return random.choice(goodbyeList)

  # if we received a Recommendation
  elif intent[0] == 'Recommendation':
    return "What is the last book you read ?"

 # if we received a Recommendation
  elif intent[0] == 'Help':

    ans = '''
    If you want to get books recommendations, you can use the command 'Recommendation',
    else, you can ask questions about any book you want :

    You want to find information about the Price of a specific book,
    you can ask questions such as :

        \u2022  Please, could you tell me the price of YourBook?
        \u2022  tell me the price of YourBook.
        \u2022  could you tell me how much is the LOTR?
        \u2022  How much is YourBook?
    

    You want to find information about the Author of a specific book,
    you can ask questions such as :

        \u2022  I wanna know who is the author of YourBook.
        \u2022  Who wrote YourBook?
        \u2022  I'd like to know who wrote YourBook?


    You want to find information about the number of pages of a specific book,
    you can ask questions such as :

        \u2022  I'd like to know how many pages are there in YourBook.
        \u2022  Please, what is the length of YourBook?
        \u2022  What is the length of YourBook?


    You want to find information about the description of a specific book,
    you can ask questions such as :

        \u2022  What can you tell me about YourBook?
        \u2022  Tell me about YourBook.
        \u2022  What is the description of YourBook?
    '''
    return ans

# if we received a Recommendation

  elif intent[0] == 'RecoAnswer':
    books_reco = 'I would then recommend you to read the following books :\n\n \u2022   '
    books_reco += ',\n \u2022   '.join(intent[1])

    sorryTxt = 'Your book is not in our data, choose another one please'

    if intent[1] == sorryTxt:
        return sorryTxt
    else :
        return  books_reco
 
  # if we received a goodbye
  elif intent[0] == 'Error':
    return "I don't know which book you're talking about! (type 'help' if you need some questions examples)"

  # if we received a goodbye
  elif intent[0] == 'No':
    return "Ok no problem you can ask questions about other books."

  #if we received a description question
  elif intent[0] == 'Description':
    url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{intent[1][2]}&filter=ebooks&orderBy=relevance&key={BOOKS_KEY}'
    data = json.loads(requests.get(url).content)
    data = parse_data(data)
    
    actual_book = str(intent[1][2])
    return books_message(data, intent[1][2], intent[0])

  #if we received a Author question
  elif intent[0] == 'Author':
    url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{intent[1][1]}&filter=ebooks&orderBy=relevance&key={BOOKS_KEY}'
    data = json.loads(requests.get(url).content)
    data = parse_data(data)
    actual_book = str(intent[1][1])
    return books_message(data, intent[1][1], intent[0])

  #if we received a Price question
  elif intent[0] == 'Price':
    url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{intent[1][2]}&filter=ebooks&orderBy=relevance&key={BOOKS_KEY}'
    data = json.loads(requests.get(url).content)
    data = parse_data(data)
    actual_book = str(intent[1][2])
    return books_message(data, intent[1][2], intent[0])

  #if we received a Length question
  elif intent[0] == 'Length':
    #print(intent[1][3])
    url = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{intent[1][3]}&filter=ebooks&orderBy=relevance&key={BOOKS_KEY}'
    data = json.loads(requests.get(url).content)
    data = parse_data(data)
    #we modify actual book:
    actual_book = intent[1][3]
    return books_message(data, intent[1][3], intent[0])
  
  else:
    return "Sorry I don't understand. (type 'help' if you need some questions examples)"




new_intent_dict = {
'Description' : 'Would you like to know what this book is about? (yes/no)',
'Author' : 'Would you like to know who is(are) the author(s) of this book? (yes/no)',
'Price' : 'Would you like to know the price of this book? (yes/no)',
'Length' : 'Would you like to know the Length of this book? (yes/no)'
}

# book = name of actual book
# liste_intent = the list of intent already asked
# intent
def creationIntent(book, liste_intent, intentDict) :
  new_intent = random.choice([x for x in intentDict if x not in liste_intent])
  res = [new_intent,[book,book,book,book]]
  print(res)
  return res
  



@client.event
async def on_ready():
  print("Le bot est prêt !")
  await client.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = 'Narcos'))


#intent
intent_creationPattern = []


@client.event
async def on_message(message):
  #print(message.content)
  if message.author != client.user :
    intent = searchPattern(pattern_dict, message.content)
    print('intent = ', intent[0])
    
    global actual_book
    global liste_intent
    global new_intent_dict
    global intent_creationPattern
    global boolReco
    print(boolReco)
    
    if intent[0] == 'Recommendation':
        boolReco = True

    elif boolReco == True :
        recommendation = CreateNewRecommendation(message.content, final_rating, model, book_pivot, books)

        intent = ['RecoAnswer', recommendation]
        boolReco = False

    else :

        if intent[0] == 'Yes': #Here we have to use actual_book and new_intent_dict
            if actual_book != "":
                print('intent_creation_debut :', intent_creationPattern)
                intent = intent_creationPattern 
                liste_intent.append(intent[0])
            else:
                intent = ["Error"]
        else:
            liste_intent=[]
            liste_intent.append(intent[0])

        if intent[0]=='No':
            actual_book=""
    
    answer = answerToIntent(intent)  
    # print('answer = ', answer)

    if isinstance(answer, str):
      await message.channel.send(answer)
    else:
      await message.channel.send(embed=answer)

    if intent[0] not in ['Hello', 'Help', 'Exit', 'Error', 'No_Match','No', 'Recommendation', 'RecoAnswer']:
    
      try:
        intent_creationPattern = creationIntent(actual_book, liste_intent, new_intent_dict)
        print('intent_creation_fin :', intent_creationPattern)
        print('list_intent_fin :', liste_intent)
        
        relance = new_intent_dict[intent_creationPattern[0]]
        await message.channel.send(relance)
        
      except:
        liste_intent=[]
        liste_intent.append(intent[0])
        actual_book=""
        await message.channel.send('You requested all the informations available about this book. You can ask about other books if you want, or get a recommendation!')
   
    # book = message.content
    # url = f'https://www.googleapis.com/books/v1/volumes?q={book}&key={BOOKS_KEY}'
    # data = json.loads(requests.get(url).content)
    # data = parse_data(data)
    # await message.channel.send(embed = books_message(data, book))
    #pprint(data)

    



client.run(TOKEN)






