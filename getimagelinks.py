# -*- coding: utf-8 -*-
# Web - Scraping pictures online from google

# Import Libraries 
import os
import json 
import requests
from bs4 import BeautifulSoup
import re

# Get image links from google image search

GOOGLE_IMAGE = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

# The User-Agent request header contains a characteristic string 
# that allows the network protocol peers to identify the application type, 
# operating system, and software version of the requesting software user agent.
# needed for google search (Know this from: Patrick Loeber)
usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

def main():
    find_images()
    
def find_images():

    boolean = True
    while boolean:
      data = input('What are you looking for? ')
      n_images = int(input('How many images do you want? '))
      boolean = input(f'Search for: {n_images} \n Is this correct? (y/n)')
      if boolean == 'y':
        boolean = False
      else:
        boolean = True 

    print('Start searching...')
    
    # When you search on google is url is https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q=
    # the query is then added to the end. Example for seaching dog, you have 
    # https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q=dog
    # So, get url query string
    searchurl = GOOGLE_IMAGE + 'q=' + data
    print(searchurl)

    # Request url, without usr_agent permission will get denied
    response = requests.get(searchurl, headers=usr_agent)
    html = response.text

    # Find all img where class='t0fcAb'
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.findAll('img', {'class': 't0fcAb'}, limit=n_images)
  
    # Get just the link from img tag
    imagelinks= []
    for ree in results:
      txt = str(ree)
      spl_word_start = 'src="'
      res = txt.partition(spl_word_start)[2]
      spl_word_end = '"/'
      text = res.partition(spl_word_end)[0]
      imagelinks.append(text)

    print(f'\nFound {len(imagelinks)} images')
    print('\n The image links found are:')
    for i in imagelinks:
        print(f'        {i}\n')

    print('Completed.')

if __name__ == '__main__':
    main()
