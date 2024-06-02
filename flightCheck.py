from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import progressbar 
import random

def filterData(filterString, list, val):
    n=0
    while n < len(list):
        if list[n][val] == filterString:
            n+=1
        else:
            list.pop(n)
            n=0

def takeUserInput(parameter):
    while True:
        user_input = input(f"{parameter}: ").upper()
        if len(user_input) == 3:
            break
        else:
            print("Please type a valid Airport Code")
    return user_input

# ASK THE USER WHERE THEY WANT TO FLY
source = takeUserInput("DEPARTURE")

# #ASK THE USER WHERE THEY WANT TO FLY FROM - PROVIDE A LIST OF AIRPORTS
destination = takeUserInput("DESTINATION")

# #ASK THE USER WHAT DATE RANGE THEY WANT TO LOOK OVER - OVER MONTHS (USE OF TOOL) OR OVER SPECIFIC DATES
from_date = input("FROM DATE (xxxx-xx-xx): ")
to_date = input("TO DATE (xxxx-xx-xx): ")
length_of_stay = input("EXPECTED # OF DAYS TO BE GONE: ")

# #ASK THE USER IF THEY WANT NON STOP FLIGHTS OR FLIGHTS WITH STOPS
#stops = input("NONSTOP FLIGHTS? (N = NO PREFERENCE, Y = YES): ")

scrapedData = []
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
user_agent_string = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
chrome_options.add_argument(f"user-agent={user_agent_string}")
driver = webdriver.Chrome(options=chrome_options)

widgets = [progressbar.Percentage(),
    ' [', progressbar.GranularBar(), '] ',
    ' (', progressbar.ETA(), ') ',
]
limit = int(to_date[-2:]) - int(length_of_stay)
with progressbar.ProgressBar(max_value=limit, widgets=widgets) as bar:
    for x in range(int(from_date[-2:]),limit):
        bar.update(x)

        from_date_dyn = from_date[:8] + str('%02d' % x)
        to_date_dyn = to_date[:8] + str('%02d' % (x + int(length_of_stay)))

        URL = 'https://www.kayak.com/flights/{source}-{destination}/{from_date_dyn}/{to_date_dyn}'.format(source=source,destination=destination,from_date_dyn=from_date_dyn, to_date_dyn=to_date_dyn)
        sleep(random.random())
        driver.get(URL)
        attempt = 0
        while attempt < 3:
            try:
                #wait = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='nrc6-inner']")))
                webContent = BeautifulSoup(driver.page_source, "html.parser")
                informationAll = webContent.find_all("div", class_="nrc6-inner")
                for information in informationAll:
                    data_holder = []
                    data = information.find_all("li", class_="hJSA-item")
                    for single_data in data:
                        times = single_data.find("div", class_="VY2U").find_all("span")
                        data_holder.append(single_data.find("div", class_="c5iUd-leg-carrier").find("img")['alt'])
                        data_holder.append(single_data.find("span", class_="JWEO-stops-text").text)
                        data_holder.append((single_data.find("div", class_="xdW8").text)[:-7])
                        data_holder.append(times[0].text)
                        data_holder.append(times[2].text)
                    cost_data = information.find("div", class_="f8F1-price-text")
                    data_holder.append(cost_data.text.replace("$", "").replace(",", ""))
                    data_holder.append(URL)
                    scrapedData.append(data_holder)
                break
            except:
                attempt+=1
                print("Resending request!")

#Close driver
driver.quit()

#Pull cheapest flight to the top
scrapedData.sort(key=lambda x:x[-2])
#print(scrapedData)

# if stops.upper() == "Y":
filterData("nonstop", scrapedData, 1)

df = pd.DataFrame(scrapedData)
df.columns = ["AIRLINE (DEPARTURE)","STOPS","TIME1","DEPARTURE","ARRIVAL","AIRLINE (RETURN)","STOPS","TIME2","DEPARTURE","ARIVAL","COST (ROUND TRIP)", "URL"]
df.to_csv('/Users/carlosinastrilla/Documents/Python Projects/scrapedData.csv')
