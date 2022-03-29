#Import librairies
from venv import create
import numpy as np
import os
import pandas as pd
import urllib.request
from PIL import Image
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


def CreateNewModel():

  #Import data
  #books = pd.read_csv(f"https://raw.githubusercontent.com/Kijako/book_bot/main/Books.csv", sep=';', encoding="latin-1",error_bad_lines=False)
  #users = pd.read_csv(f"https://github.com/Kijako/book_bot/blob/main/Users.csv", sep=';', encoding="latin-1")
  #ratings = pd.read_csv(f"https://raw.githubusercontent.com/Kijako/book_bot/main/Ratings.csv", sep=';',encoding="latin-1")

  books = pd.read_csv("https://raw.githubusercontent.com/Kijako/book_bot/main/Books.csv", sep=',',encoding="latin-1",error_bad_lines=False, low_memory=False) 
  users = pd.read_csv("https://raw.githubusercontent.com/Kijako/book_bot/main/Users.csv", sep=',',encoding="latin-1", error_bad_lines=False,low_memory=False)
  ratings = pd.read_csv("https://raw.githubusercontent.com/Kijako/book_bot/main/Ratings.csv",sep=',',encoding="latin-1", error_bad_lines=False)
  
  #error_bad_lines=False because there are lines with issues of commas.
  #encoding ="latin-1" to deal with the "utf-8 codec" error. 
  #Del the useless columns 
  
  del books["Image-URL-S"]
  del books["Image-URL-M"]
  
  #Rename the columns
  books.columns = ['ISBN', 'title', 'author','year','publisher','image']
  users.columns = ['user_id', 'location', 'age']
  ratings.columns = ['user_id', 'ISBN', 'book_rating']

  #print(books.head())
  
  #We drop the entries that not permit to make conclusions
  #We keep only the users who have rated more than 25 books
  
  x = ratings['user_id'].value_counts() > 25 #x = true ou false
  y = x[x].index 
  
  #We recover the ids of the users that we have kept
  ratings = ratings[ratings['user_id'].isin(y)]
  
  #We create a new DF with all the rates of all the users (if the user did not rate the book the rating is 0)
  rating_all = ratings.merge(books, on='ISBN')
  
  number_rating = rating_all.groupby('title')['book_rating'].count().reset_index()
  number_rating.columns = ['title','number_of_rating']
  
  final_rating = rating_all.merge(number_rating, on='title')
  
  #We keep only the books who have been rated more than 20 books
  final_rating = final_rating[final_rating['number_of_rating'] >= 20]
  
  #We remove the lines if a user has noted several times the same book
  final_rating.drop_duplicates(['user_id','title'], inplace=True)
  
  #Now, we create a pivot table where columns will be user ids, the index will be book title and the value is ratings.
  # Users who has not rated any book will have NAN value
  
  book_pivot = final_rating.pivot_table(columns='user_id', index='title', values="book_rating")
  book_pivot.fillna(0, inplace=True)
  book_sparse = csr_matrix(book_pivot)

  #print(book_sparse)
  
  #We use a KNN algorithm
  model = NearestNeighbors(algorithm='brute')
  model.fit(book_sparse)
  return final_rating, model, book_pivot, books
  
def CreateNewRecommendation(book, final_rating, model, book_pivot, books):
  #Test if a book is in the list
  if(book in list(final_rating.title)):
    distances, suggestions = model.kneighbors(book_pivot[book_pivot.index == book].values)

    sugg = list(book_pivot.index[suggestions[0]])
    del sugg[0]
    return sugg
  
      # for i in range(len(suggestions)):
      #     sugg = list(book_pivot.index[suggestions[i]])
      #     del sugg[0]
  
      #     print(sugg)
          
      #     see_image = input("Do you want to see the covers? ")
          
      #     if(see_image == 'yes'):
              
      #         for i in range(len(sugg)):
      #             print(sugg[i])
      #             urllib.request.urlretrieve(str(books['image'][i]), 'image_download')
      #             img = Image.open('image_download')
      #             img.show()
          
  else:
    return 'Your book is not in our data, choose another one please'


# final_rating, model, book_pivot, books = CreateNewModel()
# livre = input('Pour quel livre voulez vous une recommendation ?')


# CreateNewRecommendation(livre, final_rating, model, book_pivot, books)