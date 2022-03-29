# Book Bot by Group - DIA2

## Members
- Josselin Peniguel
- Amélie Noyelle
- Charlie Martin

## Description
Here are a few explanations about our bot :

This bot can be useful in 2 specific situations : 

    1. You have read a book that you liked and you want some other 
       suggestions related to this specific book.
    2. You want to chat with me about any books, I am happy to help you find some informations.

    In case you find yourself in the second situation, I can find these informations for you :

        •  Price,
        •  Description,
        •  Author(s),
        •  Number of pages

    You can also use the keyword 'help' if you need any help on how to forumlate your questions !


## Bot Info
- Chatbot platform: Discord
- [Chat with bot](https://discord.gg/KESXEUhx) (open on new tab)
  To run the bot, you need to join the discord server, then running our main.py python file. You can then start asking questions

- [Working video of this bot](https://www.youtube.com/watch?v=y6ZnMjMG8s8)

### Used API
We used Google Book API. This API lets us perform programmatically most of the operations that we wanted to do on the Google Books website. We had access to a complete database containing majority of e-books. [link]([https://link/](https://developers.google.com/books/docs/v1/using)) 

### Used Dataset
If you used an existing dataset,  please give a reference to Kaggle or the website [link]([https://link/](https://www.kaggle.com/arashnic/book-recommendation-dataset))

The data we use is divided into 3 CSVs: users, ratings and books. The books csv gives us a list of 271,360 books, the columns are: 'ISBN': the id of the book, 'title', 'author', 'year_of_publication', 'publisher', 'image_url_small', 'image_url_medium' and 'image_url_large'.
The csv gives us a list of 278,858 users who have rated books. The variables are: 'user_id', 'location' and 'age'.
The ratings csv gives us a list of 856,887 ratings given by users in the users csv on books in the oooks csv. We find the 'ratings' the 'ISBN' and the 'user_id'.


## Recommender System
The recommendation system is based on 3 datasets: users, books and ratings. We start by ordering and cleaning these data. The system works as follows: we enter a book that we liked and the system returns a list of 4 other books chosen according to the ratings of other users who have rated the book well. We have chosen to keep only the notes of the users who have rated more than 50 books and the books that have been rated more than 20 times so that our selection is adjusted to the maximum. In order to make a suggestion of 4 books we have implemented a KNN algorithm. If we enter a book that is not in our database, the user will be informed.

## Language Processing
We first tried to use 3rd party AI tools, but it turned out to be to complicated to link them with both python and discord, so we choose to use Regular expressions instead. 


Reg ex example: (we chose to put the intent in the sae table for clarity)

| Regex    | Example            |Intent |
|----------|--------------------|------ |
| (?i)\b(Hi\|Hello\|Hey\|hello\|hi)\b | hello<br> hi <br> HI<br> hEy| Hello |
| (?i)\b(bye\|exit\|quit\|leave\|stop)\b | Exit<br> exit <br> EXIT <br> bye <br> quit <br> leave| Exit|
| (?i).*(description\|describe\|tell me\|tell me more)\s+(about\|of\|in)\s+(.+)\W | What can you tell me about Moby Dick?<br> Tell me about Anna Karenina. <br>  What is the description of In Search of Lost Time?| Describe|
| (?i).*(price\|how much)\s+(about\|of\|in\|is)\s+(.+)\W | Please, could you tell me the price of Moby Dick?<br> tell me the price of Anna Karenina. <br> could you tell me how much is The Red and the Black?| Price|
|(?i).*(author of\|wrote)\s+(.+)\W| I wanna know who is the author of The Red and the Black.<br>Who wrote Anna Karenina?<br>I'd like to know who wrote Pride and Prejudice?|Author|
| (?i).\*(long\|length\|pages)(.\*?)\b(in\|of\|is)\b\s(.\*)\W | Please, what is the length of Moby Dick?| Length|
|(?i)\b(help)\b | help| Help|
| No regex |dzoznflznlfzj,foez| Error and NoMatch|
| (?i)^Recommendation$ | recommendation| Recommendation|
|No regex this intent is automatically created after a recommendation intent|--| RecoAnswer| 
|(?i)^yes$ |yes <br> YES <br> yEs | Yes|
|(?i)^no$ |no <br> No <br> NO | No|


## Scenarios
While thinking about the different functionalities of our bot, we found it more relevant not to have a predefined scenario. That's why there is no typical example. 
Our bot asks questions as long as the user has questions about a certain book. If he wants to search for information about other books, he can also, in the same scenario. 
Also, for the information given about each book, we coded our bot randomly so that it asks the user if he wants to get certain info, without ever asking the same questions.

.
### Example 1  : The user try to trap the bot
| User | Bot                                                     |
|------|---------------------------------------------------------|
| Hi   |Hi, + (general informations about the bot)|
|ouzebfkzbfqkezf   | Sorry I don't understand. (type 'help' if you need some questions examples)|
|yes  | I don't know which book you're talking about!|

### Example 2  : The user wants some informations about a book which is not in the API
| User | Bot                                                     |
|------|---------------------------------------------------------|
| Hi   |Hi, + (general informations about the bot)|
|ouzebfkzbfqkezf   | Sorry I don't understand. (type 'help' if you need some questions examples)|
|yes  | I don't know which book you're talking about!|

### Example 3: The user wants all informations about a book
| User              | Bot |
|-------------------|-----|
| tell me the price of snnnslapjzip.   | It seems like this information is unavailable<br> Would you like to know the price of this book? (yes/no)|


### Example 4: The user wants only one information about a book
| User              | Bot |
|-------------------|-----|
| Hello   |Hi, + (general informations about the bot)|
| what is the length of Anna Karenina?  | Anna Karenina has a number of pages equals to : <br>1127<br>Would you like to know what this book is about? (yes/no)|
| no   |Ok no problem you can ask questions about other books.|

### Example 5  : The user wants to read a new book
| User | Bot                                                     |
|------|---------------------------------------------------------|
| Hi   |Hi, + (general informations about the bot)|
|recommendation| What is the last book you read ?|
|Moby Dick  | I would then recommend you to read the following books :<br><br>North and South (North and South Trilogy, Book 1),<br>Evening Star,<br>False Witness,<br>The Curse of the Mummy's Tomb (Goosebumps, No 5)|

### Example 6  : The user wants to read a new book but the last one he read is not in our dataset:
| User | Bot                                                     |
|------|---------------------------------------------------------|
|recommendation| What is the last book you read ?|
|MobuDick  | Your book is not in our data, choose another one please|

### Example 7  : Complete example
| User | Bot                                                     |
|------|---------------------------------------------------------|
| Hi   |Hi, + (general informations about the bot)|
|ouzebfkzbfqkezf   | Sorry I don't understand. (type 'help' if you need some questions examples)|
|help  | if you want to get books recommendations, you can use the command 'Recommendation', else, you can ask questions about any book you want : ...|
|tell me about  In Search of Lost Time.  | In Search of Lost Time description <br><br>In Search of Lost Time (French: À la recherche du temps perdu)— previously also translated as Remembrance of Things Past, is a novel...<br><br>Would you like to know who is(are) the author(s) of this book? (yes/no)|
|yes  | In Search of Lost Time author(s) :<br><br>Marcel Proust, Golden Deer Classics<br><br>Would you like to know the Length of this book? (yes/no)|
|no  | Ok no problem you can ask questions about other books.r|



