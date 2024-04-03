#function One
#download the webpage
#function must take parameter of link and it returns a file path to an already downloaded html

#function Two
#it takes parameter of an html file path and uses beautifulSoup to filter required content and creates 
#a new file and saves the filter data into it and returns file path of new file

#function Three
#takes in a parameter of filtered html file path and loads the data into beautifulSoup and goes through 
#tags and find them and download them and replace the image tag(href) with # and returns a list of 
#image file names

import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium import webdriver

def downloadWebpage(webpageUrl):
    # Set the path to the ChromeDriver executable
    driverPath = "C:\\Users\\naved\\Downloads\\chromedriver_win32\\chromedriver.exe"

    # Default output file path
    outputFile = 'downloadedHtml.html'

    # Initialize chrome web driver
    driver = webdriver.Chrome()

    # Get webpage url
    driver.get(webpageUrl)

    # Getting html content
    webpageContent = driver.page_source

    # Close the webdriver
    driver.quit()

    # Saving html content to file
    with open(outputFile, 'w', encoding='utf-8') as f:
        f.write(webpageContent)

    print(f"Webpage downloaded and saved as '{outputFile}'")

    return os.path.abspath(outputFile)

def filterContent(htmlFilePath):
    with open(htmlFilePath, 'r', encoding='utf-8') as file:
        htmlContent = file.read()

    soup = BeautifulSoup(htmlContent, 'html.parser')

    contentSection = soup.find('section', class_='mt-content-container')

    if contentSection:
        requiredContent = str(contentSection)

        filteredOutputFile = 'filteredContent.html'
        with open(filteredOutputFile, 'w', encoding='utf-8') as f:
            f.write(requiredContent)

        print(f"Filtered content saved as '{filteredOutputFile}'")

        return os.path.abspath(filteredOutputFile)
    else:
        print("No section with class 'mt-content-container' found.")
        return None

requiredFilePath = downloadWebpage(r"https://chem.libretexts.org/Bookshelves/Introductory_Chemistry/Basics_of_General_Organic_and_Biological_Chemistry_(Ball_et_al.)/02%3A_Elements_Atoms_and_the_Periodic_Table/2.02%3A_Atomic_Theory")
print("Path of saved HTML file", requiredFilePath)
htmlFilePath = requiredFilePath
filteredFilePath = filterContent(htmlFilePath)
print("Path of filtered html file",filteredFilePath)






