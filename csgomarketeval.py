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

# open the report file with datetime name
report = open(dt_string, 'w')

# set some const and var
textstr = "" # accumulating string that will be written to text file at the end
sleep_timer = 15 # sleep timer to go around pesky status code 429s (valve pls fix)
current = 0 # page item offset
increment = 100 # number of items in page
total_items = 15150 # rough number of items in the entire market
desired_number_of_pages = 150 # number of pages we want. (152 for everything)               
sum = 0 # final sum dolla dolla billz

print('\n' + str(desired_number_of_pages * increment)  + " number of items will be scanned.")
print("This will take around " + str(sleep_timer * desired_number_of_pages / 60) + " minutes.")

try:
  for j in range(0, desired_number_of_pages):

    url = "https://steamcommunity.com/market/search/render/?query=&start=" + str(current) + "&count=" + str(current + increment) + "&search_descriptions=0&sort_column=price&sort_dir=des&appid=730&norender=0"

    # housekeeping
    try:
      response = requests.get(url)
    except HTTPError:
      print("Couldn't reach page." + "\n")
    except:
      print("Unexpected error:", sys.exc_info()[0] + "\n")
      textstr += ("Terminating ..." + "\n")
    else:

      if response.status_code  != 200:
        print("Server returned bad response.")
        print("Terminating ...")
        textstr += ('Partial CS:GO market evaluated at: $' + str(sum)) + "\n"
        textstr += ("Got up to " + str(j * increment) + " items." + "\n")
        textstr += ('Entire CS:GO market evaluated at: $' + str(sum) + "\n")
        n = report.write(textstr)
        report.close()
        exit(0)

      else:
        # get text as a py string and lets go
        src = response.text
        print("\n - Status OK for page " + str(j+1) + "...")

        # remove bits and bobs from the query result to clean it up a bit (I am going to hell for this line)
        src = src.replace('\\n', '').replace('\\r', '').replace('\\t', '').replace('\\', '').replace('u20ac', '').replace('u2605', '').replace('u2122', '')

        # set split substrings to find the name price and quantity data
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

        # just some pretty print stuff
        pagesum = 0
        textstr += ('\n|---------------------------------------------------------------|' + "\n")
        textstr += ('\n|--------------------------- PAGE ' + str(j) + '-----------------------------|' + "\n")
        textstr += ('\n|---------------------------------------------------------------|' + "\n")

        textstr += ('Query URL: ' + url + "\n")
        textstr += ('\n' + "\n")

        # multiply supply with base singular price to reach an eval and accumluate to the variables
        for i in range(1, increment+1):
          textstr += (str(prices[i]) + '\t\t' + str(quantities[i]) + '\t\t' + str(names[i])  + "\n")
          pagesum += quantities[i] * prices[i]

        textstr += ("\n\nPage sum: $" + str(pagesum) + "\n")

        # increment the overall sum and current to switch to the next page of data
        sum += pagesum
        current += increment

        # valve pls no ban timeout pls
        sleep(sleep_timer)

  # save report and close
  textstr += ('Entire CS:GO market evaluated at: $' + str(sum) + "\n")
  n = report.write(textstr)
  report.close()
  
except:
  # save report and close
  textstr += ('Entire CS:GO market evaluated at: $' + str(sum) + "\n")
  n = report.write(textstr)
  report.close()


    


    
    
