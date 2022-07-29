# Import Required Modules
from bs4 import BeautifulSoup
import requests
import re
import random
import pandas as pd
from fake_useragent import UserAgent
import os
from dotenv import load_dotenv
import requests, json

#Use webscraping and wikipedia to acquire list of all 50 states. 
states = []
real_states = []
page = requests.get("https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States")
soup = BeautifulSoup(page.content, 'html.parser')
object = soup.find(id="bodyContent")
items = object.find_all(scope="row")
for result in items:
    states.append(result.find_all(title= (re.compile("."))))
#print(len(states))
for item in states:
    try:
        real_states.append(str(*item[0]))
    except:
        continue
        
#cleaning the data to make it usable for next phase
real_states = real_states[0:50]
states = []
for item in real_states:
    states.append(item.replace(" ","_"))

#randomly select a state and look up cities in that state using wikipedia
final_state = random.choice(states)
print(final_state)
page = requests.get("https://en.wikipedia.org/wiki/List_of_cities_in_"+final_state)
table_class = "wikitable sortable jquery-tablesorter"
soup = BeautifulSoup(page.text, 'html.parser')
city_raw = soup.find('table',{'class':'wikitable'})

#import raw city data into dataframe
df= pd.read_html(str(city_raw))
df=pd.DataFrame(df[0])

#Cleaning city name data to make usable for next phase.
try:
    cities= df['Name'].values.tolist()
except KeyError:
    try:
        cities= df['City'].values.tolist()
    except KeyError:
        try:
            cities= df['Place Name'].values.tolist()
        except KeyError:
            try:
                cities= df['Municipality'].values.tolist()
            except:
                cities= df['County seat[5][6]'].values.tolist()

#This is to correct an error that occurs later on...although it might not be necessary anymore.                
errorfix = []

#web scrape Bar data from Untappd as a possible location for our adventure.
ua = UserAgent()
headers = {'User-Agent': ua.chrome}
rancity = random.choice(cities)
rancityurl = rancity
for item in rancityurl:
    rancityurl = item.replace(" ", "+")
made_up = ["The Wandering Jackalope", "The Nasty Dog", "Bad Decision Depot", "The Leaky Catheter"]
list1 = []
if rancity[0].isalpha() == False:
    rancity = re.sub(r"[^a-zA-Z0-9]","",rancity)
final_stateurl = final_state
for item in final_stateurl:
    final_stateurl = final_stateurl.replace("_", "+")
final_state = final_state.replace("_"," ")
page = requests.get("https://untappd.com/search?q="+rancityurl+"%2C+"+final_stateurl+"&type=venues&sort=",headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
object = soup.find(class_="main")
items = object.find_all(class_="venue-details")
for result in items:
    list2 = result.find_all(class_="name")
    list1.append(str(list2))
CLEANR = re.compile('<.*?>') 

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext
final_beer = []
for x in list1:
    y = []
    y.append(cleanhtml(x))
    for z in y:
        a = z.replace("]","")
        b = a.replace("[","")
        final_beer.append(b)
        
#Use a list of made up bar names just in case Tappd comes up with nothing.
if items == []:
    final_beer = made_up

#Using google places for additional locations of interest.    
#load API Keys for google places
load_dotenv()
resultz = []
api_key = os.environ.get("GOOGLEKEY")

# url variable store url
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
locations= ['police stations','fire department','city hall','restaurants','amusement parks','parks','rivers','barbershops','refuse collection','ice cream','car dealerships','auto repair','department stores']

# The text string on which to search
query = "{} near {},{}".format(random.choice(locations),rancity,final_state)

# get method of requests module

# return response object
r = requests.get(url + 'query=' + query +
						'&key=' + api_key)

# json method of response object convert
# json format data into python format data
x = r.json()

# now x contains list of nested dictionaries
# we know dictionary contain key value pair
# store the value of result key in variable y
y = x['results']

# keep looping upto length of y
for i in range(len(y)):
	
	# Print value corresponding to the
	# 'name' key at the ith index of y
	resultz.append(y[i]['name'])
realresultz = random.choice(resultz)
realfinal_beer = random.choice(final_beer)
randomlocationlist = [realresultz,realfinal_beer]

try:
    print('So this one time I was in '+rancity+", "+final_state+ " with Ginger from the Spice Girls at the "+random.choice(random.choice(randomlocationlist) +" when...")


except TypeError:
    for item in cities:
        errorfix.append(*item)
    cities = errorfix
    rancity=random.choice(cities)
    print('So this one time I was in '+rancity+", "+final_state+ " with Ginger from the Spice Girls at "+str(random.choice(randomlocationlist) +" when...")

#That is it for now. More updates as I learn more about how to polish this and make it usable. 
