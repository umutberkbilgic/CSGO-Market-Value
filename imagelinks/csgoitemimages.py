import requests
from requests.exceptions import HTTPError
import sys
from math import ceil
from time import sleep
import urllib.request



# set some const and var
sleep_timer = 15 # sleep timer to go around pesky status code 429s (valve pls fix)
current = 0 # page item offset
increment = 100 # number of items in page
total_items = 15190 # rough number of items in the entire market
desired_number_of_pages = 155 # number of pages we want. (152 for everything)               
sum = 0 # final sum dolla dolla billz

print('\n' + str(desired_number_of_pages * increment)  + " number of items will be scanned.")
print("This will take around " + str(sleep_timer * desired_number_of_pages / 60) + " minutes.")

for j in range(0, desired_number_of_pages):

  url = "https://steamcommunity.com/market/search/render/?query=&start=" + str(current) + "&count=" + str(current + increment) + "&search_descriptions=0&sort_column=price&sort_dir=des&appid=730&norender=0"

  # housekeeping
  try:
    response = requests.get(url)
  except HTTPError:
    print("Couldn't reach page." + "\n")
  except:
    print("Unexpected error:", sys.exc_info()[0] + "\n")
  else:

    if response.status_code  != 200:
      print("Server returned bad response.")
      print("Terminating ...")
      exit(0)

    else:
      # get text as a py string and lets go
      src = response.text
      print("\n - Status OK for page " + str(j+1) + "...")

      # remove bits and bobs from the query result to clean it up a bit (I am going to hell for this line)
      src = src.replace('\\n', '').replace('\\r', '').replace('\\t', '').replace('\\', '').replace('u20ac', '').replace('u2605', '').replace('u2122', '')

      if src.find('There were no items matching your search. Try again with different keywords') != -1:
        print('reached premature end of query chain, returning')
        break

      # set split substrings to find the name price and quantity data
      images = src.split('1x, ')
      names = src.split('market_listing_item_name"')

      # fix up images list
      for i in range(1, increment + 1):
        images[i] = images[i][:images[i].find('62fx62fdpx2x')]

      # fix up name list
      for i in range(1, increment + 1):
        names[i] = (names[i][ (names[i].find('>')) + 1 : (names[i].find('<')) ])
        if (names[i][0] == ' '):
          names[i] = names[i][1:]
      
      # write corresponding imagelinks and names
      namestxt = open('names.txt', 'a')
      linkstxt = open('links.txt', 'a')

      for i in range(1, increment + 1):
        namestxt.write(names[i] + '\n')
        linkstxt.write(images[i] + '\n')

      sleep(sleep_timer)

      current += increment

  namestxt.close()
  linkstxt.close()