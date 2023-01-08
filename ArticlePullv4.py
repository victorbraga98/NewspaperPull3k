#! /usr/bin/env python3

# This script is used to pull article information into a text file saved into the Desktop of the running user.

#DEBUG CODE-----START
# import debugpy

# # 5678 is the default attach port in the VS Code debug configurations. Unless a host and port are specified, host defaults to 127.0.0.1
# debugpy.listen(5678)
# print("Waiting for debugger attach")
# debugpy.wait_for_client()
# print('break on this line')

#DEBUG CODE-----END

from datetime import datetime
import os
from pathlib import Path
import urllib.request
import re #regular expression used for summary
from newspaper import Article

__author__ = "Victor Braga"
__copyright__ = "Copyright 2022, Victor Braga"
__credits__ = ["Lucas Ou-Yang","Newspaper3k"]
__license__ = "GPL-3"
__version__ = "1.0.0"
__maintainer__ = "Victor Braga"
__email__ = "victorbraga98@gmail.com"
__status__ = "Production"

#create job ID and output file, then get current date
ID = datetime.now().strftime("%Y-%m-%d_%H%M%S")
currentYear = datetime.now().strftime("%Y")
currentMonth = datetime.now().strftime("%B")
#Number of articles listed count
count = 0


#get current user and prepare system
os.system("clear")
# TEMP set user to victorbraga
# currentUser = "victorbraga"
currentUser = os.getlogin()

# Lets pick up multiple links from the user. 
links = []
userInput = None

linkCount = 0
print("Paste links below. If multiple links, enter them in a new line.\nWhen finished, hit enter again.\n")
while userInput != "":
    linkCount += 1
    userInput = input(f"Link {linkCount}:  ")
    links.append(userInput)


# Now lets clean up empty list items.
while("" in links):
    links.remove("")

if not links:
    print("No links were provided. Stopping the script.")
    exit()


# TEMP skipped for debugging
# url = 'https://www.southerntidings.com/gsc/first-fully-digital-church-in-southern-union-launches/'
# url = 'https://www.kytn.net/news/kytn-adventurer-camporee-sees-a-40-attendance-increase'
# url = input("\nPaste the article URL here:\n")


def DownloadandSave(url,count):
    article = Article(url) #pipe article into function
    article.download() #download to memory


    article.parse() #read it

    authors = article.authors #get authors
    pubDate = article.publish_date
    artText = article.text
    artImage = article.top_image
    artMovie = article.movies
    artTitle = article.title
    artLink = article.url



    # Need to save paragraphs into a list and filter through them to find the core text
    paragraphs = []
    for i in artText.split('\n'):
        paragraphs.append(i)

    paragraphCount = len(paragraphs)



    # Function to count number of periods to find sentences in core text.
    def check_dots(string):
        # counter
        dotCount = 0
        # loop for search each index
        for i in range(0, len(string)):
            # Check each char
            # is period or not
            if string[i] == ".":
                dotCount += 1
        return dotCount


    # Loop through text and find the first useful sentence
    sentences = 0
    # print(f'\nParagraph count = {paragraphCount}')
    for iteration in range(paragraphCount):
        sentences = check_dots(paragraphs[iteration])
        # print(f'iteration number: {iteration}. Number of sentences = {sentences}') #DEBUG ONLY
        if sentences >= 4:
            coreStart = iteration #use corestart number as first paragraph.
            break
        else:
            continue


    # Remove first n items from paragraph as they are not useful.
    del paragraphs[:(coreStart-1)]
    # print(len(paragraphs))

    # Check Desktop to see if "Southern Tidings" exists as a directory.
    SouthernTidingsExists = Path(f"/Users/{currentUser}/Desktop/Southen_Tidings/{currentYear}/{currentMonth}").is_dir()

    # If Southern_Tidings does not exist, create one. 
    newCreatedPath = f'/Users/{currentUser}/Desktop/Southen_Tidings/{currentYear}/{currentMonth}'

    if SouthernTidingsExists == False:
        Path(newCreatedPath).mkdir(parents=True, exist_ok=True)
    else:
        print("Saving photo...\n")

    #save top artImage
    urllib.request.urlretrieve(artImage, f'{newCreatedPath}/{ID}-{count}.jpg')

    # Write to HTML file
    # to open/create a new html file in the write mode
    html = open(f'/Users/{currentUser}/Desktop/Southen_Tidings/{currentYear}/{currentMonth}/{ID}.html', 'a')

    # the html code which will go in the file HTML file. Commented out photo as Flocknote does not support it.
    html_template = f"""<html>
    <head>
    <title>{ID}</title>
    </head>
    <body>
    <h2>{artTitle}</h2>
    <!-- <img src="{newCreatedPath}/{ID}.jpg"> -->
    <p>{paragraphs[1]}</p>
    <p><a href="{url}">READ MORE</a></p>
    <p>- - - - - - - - - - - - - -</p>


    </body>
    </html>
    """

    # writing the code into the file
    html.write(html_template)
    # close the file
    html.close()

for i in links:
    count += 1
    print(f"downloading article {count}")
    DownloadandSave(i,count)





print("Files were written to the desktop.")
os.system(f"open /Users/{currentUser}/Desktop/Southen_Tidings/{currentYear}/{currentMonth}/")

