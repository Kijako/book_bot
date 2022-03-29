import discord
from pprint import pprint

def parse_data(data):
  # data = data.items[0]['description']
  data = data['items']
  return data 

def books_message(data, book, intent_regex):
  #pprint(data)
  if intent_regex == 'Description':
    #pprint(data[0])
    #pprint(data[1])
    title_ = f'{book} description'
    try:
        first_data = data[0]['volumeInfo']['description']
    except:
        return 'It seems like this information is unavailable'

  elif intent_regex == 'Author':
    #pprint(data)
    try:
        first_data=""
        liste_auteur = data[0]['volumeInfo']['authors']
        first_data += ', '.join(liste_auteur)
    except:
        return 'It seems like this information is unavailable'
    title_ = f'{book} author(s) :'

  elif intent_regex == 'Price':
    if str(data[0]['saleInfo']['saleability']) == 'FREE':
      first_data = 'This book is free'
    elif str(data[0]['saleInfo']['saleability']) == 'FOR_SALE' :
      first_data = str(data[0]['saleInfo']['listPrice']['amount'])+ '€'
    else:
      first_data = 'This book is not for sale'
    #pprint(data[0]['saleInfo'])
    # for i in range(len(data)):
    #   try:
    #     first_data = str(data[i]['saleInfo']['listPrice']['amount'])+ '€'
    #     break
    #   except :
    #     first_data = "This book is not for sale"        
    title_ = f'{book} price :'

  elif intent_regex == 'Length':
    try:
          first_data = data[0]['volumeInfo']['pageCount']
    except:
        return 'It seems like this information is unavailable'
    title_ = f'{book} has a number of pages equals to :'

  #pprint(first_data)
  book = book.title()
  message = discord.Embed(
    title = title_,
    value = str(first_data),
    description = str(first_data)
  )
  return message


def error_message(book):
  print('error')