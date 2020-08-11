import requests
from requests.exceptions import HTTPError
import sys
from math import ceil
from time import sleep

from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("csgo_report_%d-%m-%Y_%H-%M-%S.txt")

report = open(dt_string, 'w')
textstr = ""

current = 0
increment = 100
total= ceil(500/increment)
sum = 0

for j in range(0, total):

  url = "https://steamcommunity.com/market/search/render/?query=&start=" + str(current) + "&count=" + str(current + increment) + "&search_descriptions=0&sort_column=price&sort_dir=des&appid=730&norender=0"

  # housekeeping
  try:
    response = requests.get(url)
  except HTTPError:
    textstr += ("Couldn't reach page." + "\n")
  except:
    textstr += ("Unexpected error:", sys.exc_info()[0] + "\n")
    textstr += ("Terminating ..." + "\n")
  else:
    status = "OK" if (response.status_code == 200) else str(response.status_code)
    # textstr += ("STATUS: " + str(status))

    if status != "OK":
      print("Server returned bad response.")
      print("Terminating ...")
      textstr += ('Partial CS:GO market evaluated at: $' + str(sum)) + "\n"
      textstr += ("Got up to " + str(j * increment) + " items." + "\n")
      exit(0)

    else:
      # get text as a py string and lets go
      src = response.text
      print("Status OK for page " + str(j+1) + "...")

      # remove bits and bobs from the query result to clean it up a bit
      src = src.replace('\\n', '')
      src = src.replace('\\r', '')
      src = src.replace('\\t', '')
      src = src.replace('\\', '')
      src = src.replace('u20ac', '')
      src = src.replace('u2605', '')
      src = src.replace('u2122', '')

      quantities = src.split('data-qty=')
      prices = src.split('class="normal_price"')
      names = src.split('market_listing_item_name"')

      # fix up quantity list
      for i in range(1, len(quantities)):
        quantities[i] = int(quantities[i][1 : quantities[i][1:].find('"') + 1])

      # fix up price list
      for i in range(1, len(prices)):
        prices[i] = float( (prices[i][ (prices[i].find('>')) + 2 : (prices[i].find('<')) - 4 ]).replace(',','') )

      # fix up name list
      for i in range(1, len(names)):
        names[i] = (names[i][ (names[i].find('>')) + 1 : (names[i].find('<')) ])
        if (names[i][0] == ' '):
          names[i] = names[i][1:]

      pagesum = 0
      textstr += ('\n|---------------------------------------------------------------|' + "\n")
      textstr += ('\n|--------------------------- PAGE ' + str(j) + '-----------------------------|' + "\n")
      textstr += ('\n|---------------------------------------------------------------|' + "\n")

      textstr += ('Query URL: ' + url + "\n")
      textstr += ('\n' + "\n")

      # multip
      for i in range(1, increment+1):
        textstr += (str(prices[i]) + '\t\t' + str(quantities[i]) + '\t\t' + str(names[i])  + "\n")
        pagesum += quantities[i] * prices[i]

      textstr += ("\n\nPage sum: $" + str(pagesum) + "\n")

      sum += pagesum
      current += increment
      sleep(10)


textstr += ('Entire CS:GO market evaluated at: $' + str(sum) + "\n")
n = report.write(textstr)
report.close()
    


    
    
