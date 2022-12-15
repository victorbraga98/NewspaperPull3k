from newspaper import Article
from datetime import datetime
import os
import urllib.request

#create job ID and output file
ID = datetime.now().strftime("%Y-%m-%d_%H%M%S")

#get current user and prepare system
os.system("clear")
currentUser = os.getlogin()

url = input("\nPaste the article URL here:\n")


article = Article(url) #pipe article into function
article.download() #download to memory

article.parse() #read it

authors = article.authors #get authors
pubDate = article.publish_date
artText = article.text
artImage = article.top_image
artMovie = article.movies
artKeywords = article.keywords
artSummary = article.summary
artTitle = article.title
artLink = article.url

#write to text file
with open(f'/Users/{currentUser}/Desktop/{ID}.txt', 'w') as f:
    f.write(f"***** JOB: {ID} *****\n\n")
    f.write(f"Title: {artTitle} \n\n")
    for names in authors:
        f.write(f"Authors: {names} \n\n")
    f.write(f"Summary: {artSummary} \n\n")
    f.close()


#save top artImage
urllib.request.urlretrieve(artImage, f'/Users/{currentUser}/Desktop/{ID}.jpg')
