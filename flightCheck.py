from time import sleep
from selenium import webdriver
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import progressbar 
import random

# Validate user input
def takeUserInput(parameter):
    while True:
        user_input = input(f"{parameter}: ").upper()
        if len(user_input) != 3:
            print("Please type a valid Airport Code")
        else:
            break
    return user_input

def takeUserDate(parameter):
    today_date = (str(datetime.now()))[:10]
    today_year = int(today_date[0:4])
    today_month = int(today_date[5:7])
    today_day = int(today_date[8:10])

    while True:
        user_input = input(f"{parameter} Date (0000-00-00): ").upper()
        if len(user_input) != 10:
            print("Please type a valid Date")
        else:
            if user_input[4] == "-" and user_input[7] == "-":
                if user_input[0:4].isnumeric() and user_input[5:7].isnumeric() and user_input[8:10]:
                    if int(user_input[0:4]) >= today_year:
                        if int(user_input[5:7]) >= today_month and int(user_input[5:7]) < 12:
                            if (int(user_input[8:10]) >= today_day or int(user_input[5:7]) > today_month) and int(user_input[8:10]) <= 31:
                                break
                            else:
                                print("Please check this day and make sure this date in not in the past or out of range!")
                        else:
                            print("Please check the month and make sure this date in not in the past or out of range!")
                    else:
                        print("Please check the year and make sure this date is not in the past or out of range!")
                else:
                    print("Only integer values are allowed in the dates")
            else:
                print("Please type a date in the format 0000-00-00")
    return user_input

# ASK THE USER WHERE THEY WANT TO FLY
print("\n=================================================================================")
print("=================================================================================\n")
source = takeUserInput("Departure")
destination = takeUserInput("Destination")

#ASK THE USER WHAT DATE RANGE THEY WANT TO LOOK OVER - OVER MONTHS (USE OF TOOL) OR OVER SPECIFIC DATES
from_date = takeUserDate("Departure")
to_date = takeUserDate("Return")

length_of_stay = input("Expected duration of trip: ")

# #ASK THE USER IF THEY WANT A SPECIFIC AIRLINE
airline = input("Preferred Airline? (N = No preference): ")

# #ASK THE USER IF THEY WANT NON STOP FLIGHTS OR FLIGHTS WITH STOPS
stops = input("Stops? (N = No Stops, NP = No preference): ")

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
                wait = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='nrc6-inner']")))
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
                    data_holder.append(float(cost_data.text.replace("$", "").replace(",", "")))
                    data_holder.append(URL)

                    if stops.upper() == "N":
                        if "nonstop" not in data_holder[1] and "nonstop" not in data_holder[6]:
                            continue
                    if airline.upper() != "N":
                        if airline not in data_holder[0] and airline not in data_holder[5]:
                            continue
                    scrapedData.append(data_holder)
                break
            except:
                attempt+=1
                print("\n---Resending request!---")
        if attempt == 3:
            raise "ERROR: The Airport codes may be invalid! Please double check that you are using valid codes"

#Close driver
driver.quit()

# Create data frame
df = pd.DataFrame(scrapedData)
df.columns = ['AIRLINE (DEPARTURE)','STOPS','TIME1','DEPARTURE','ARRIVAL','AIRLINE (RETURN)','STOPS','TIME2','DEPARTURE','ARIVAL','COST', "URL"]

# Get cheapest flights to top
sortedDF = df.sort_values(by=['COST'])

# Output to .csv
sortedDF.to_csv('/Users/carlosinastrilla/Documents/Python Projects/scrapedData.csv')
