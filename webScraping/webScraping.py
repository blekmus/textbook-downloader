# function Two
# it takes parameter of an html file path and uses beautifulSoup to filter required content and creates
# a new file and saves the filter data into it and returns file path of new file

# function Three
# takes in a parameter of filtered html file path and loads the data into beautifulSoup and goes through
# tags and find them and download them and replace the image tag(href) with # and returns a list of
# image file names

# look into https://github.com/SergeyPirogov/webdriver_manager for managing driver

import os
from bs4 import BeautifulSoup
from selenium import webdriver
import tempfile


def downloadWebpage(workingDir, webpageUrl, driverPath):
    """
    Downloads the webpage and saves it as an HTML file
    :param webpageUrl: URL of the webpage to be downloaded
    :param driverPath: Path to the chrome web driver
    :return: Absolute path of the saved HTML file
    """

    # Default output file path
    outputFile = os.path.join(workingDir, 'webpage.html')

    # Initialize chrome web driver and get the webpage
    driver = webdriver.Chrome(driverPath)
    driver.get(webpageUrl)

    # Get html content
    webpageContent = driver.page_source

    # Close the webdriver
    driver.quit()

    # Saving html content to file
    with open(outputFile, 'w', encoding='utf-8') as f:
        f.write(webpageContent)

    print(f"Webpage downloaded and saved to '{outputFile}'")

    return outputFile


def filterContentAndImages(htmlFilePath):
    # Read the html file
    with open(htmlFilePath, 'r', encoding='utf-8') as file:
        htmlContent = file.read()

    # Parse the html file using BeautifulSoup
    soup = BeautifulSoup(htmlContent, 'html.parser')

    # Find all <p> tags
    pTags = soup.find_all('p')

    # Find all image tags within <div> tags
    divTags = soup.find_all('div')
    imgTags_within_div = []
    for div in divTags:
        imgTags_within_div.extend(div.find_all('img'))

    # Concatenate <p> tags with newline characters
    requiredContent = '\n'.join(str(p) for p in pTags) + '\n' + str(imgTags_within_div)

    # Create a new HTML file with the filtered content
    filteredOutputFile = 'filteredContent.html'
    with open(filteredOutputFile, 'w', encoding='utf-8') as f:
        f.write(requiredContent)

    print(f"Filtered content saved as '{filteredOutputFile}'")

    return os.path.abspath(filteredOutputFile)


driverPath = "C:\\Users\\naved\\Downloads\\chromedriver_win32\\chromedriver.exe"
url = "https://chem.libretexts.org/Bookshelves/Introductory_Chemistry/Basics_of_General_Organic_and_Biological_Chemistry_(Ball_et_al.)/02%3A_Elements_Atoms_and_the_Periodic_Table/2.02%3A_Atomic_Theory"

# create a temporary directory to store data
workingDir = tempfile.mkdtemp()

# download the webpage
htmlFilePath = downloadWebpage(workingDir, url, os.path.abspath(driverPath))
print("Path of saved HTML file", htmlFilePath)

# delete the temporary directory for now
# remove it if you're using it later
os.rmdir(workingDir)

# get the main content from the html file
filteredFilePath = filterContentAndImages(htmlFilePath)
print("Path of filtered html file", filteredFilePath)
