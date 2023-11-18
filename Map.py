

#This file is used to get the gps from an image. Do note that the image has to be a jpg to get the correct details. In order to maintain the metadata, save the image in google drive before downloading to PC
from selenium import webdriver
import webbrowser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import NoSuchElementException
import time 
import string
import os
import PIL.Image
import cmath



img = PIL.Image.open("IMG_4471.JPG") 
#image goes here

import PIL.ExifTags

exif ={
    PIL.ExifTags.TAGS[k]:v
    for k, v in img._getexif().items()
    if k in PIL.ExifTags.TAGS
}
exif['GPSInfo']

#test 1: Positive
#this should print out the overall coords of the location
print(exif['GPSInfo'])

north= exif['GPSInfo'][2]
east= exif['GPSInfo'][4]

#test 2: Positive
#This should only show the north and east coords
print(north)
print(east)

#Turns values into gmplot values
lat= ((((north[0] *60) + north[1]) *60) + north[2]) /60 /60
long= ((((east[0] *60) + east[1]) *60) + east[2]) /60 /60

lat,long= float(lat), float(long)

#test 3: Positive
#print(lat,long)


from gmplot import gmplot

gmap=gmplot.GoogleMapPlotter(lat,long,12)
gmap.marker(lat,long, "cornflowerblue")
gmap.draw("location.html")

from geopy.geocoders import Nominatim
geoLoc =Nominatim(user_agent= "GetLoc")



#webbrowser.open("location.html", new=2)
time.sleep(4)
print(lat,long)

#Loading Selenium Webdriver 

import webbrowser


# url1= "https://www.google.com/maps/@1.3734742,103.8332197,15z?entry=ttu "
# chrome_path= r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
# webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
# webbrowser.get('chrome').open_new_tab(url1)

options=Options()
options.add_experimental_option("detach",True)

driver =webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                         options=options)

# driver.get("https://www.google.com/maps/")
# driver.maximize_window()

# links = driver.find_elements("xpath","//a[@href]")
# for link in links:
#     if "searchbox" in link.get_attribute("innerHTML"):
#         link.click()
#         break
    

# searchBox="/html/body/div[3]/div[8]/div[3]/div[1]/div[1]/div/div[2]/form/input"
# searchBtn="/html/body/div[3]/div[8]/div[3]/div[1]/div[1]/div/div[2]/div[1]/button"
# searchBar = driver.find_element(searchBox)
# searchBar.SendKeys(lat,long)
# searchButton = driver.FindElement(By.XPath(searchBtn))
# searchButton.Click()

chrome_driver_path = 'C:\Program Files (x86)\Google\Chrome\Application.exe'
#This should be your chrome driver path. mine is the above mentioned one. Yours will be different.

# Create a new instance of the Chrome driver
#driver = webdriver.Chrome(executable_path=chrome_driver_path)

# Open Google Maps
driver.get("https://www.google.com/maps")
driver.maximize_window()

try:
    # Wait for the search box to be clickable
    search_box = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.NAME, "q"))
    )

    # Enter a location value
    search_box.send_keys(f"{float(lat)}, {float(long)}")

    # Press ENTER to trigger the search
    ActionChains(driver).send_keys(Keys.ENTER).perform()

    # Wait for the search results to load (you may need to adjust the time depending on your internet speed)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "hArJGc")))
    


except Exception as e:
    print(f"An error occurred: {e}")



