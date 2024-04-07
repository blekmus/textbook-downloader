# TODO
# look into https://github.com/SergeyPirogov/webdriver_manager for managing driver
# look into deleting the temp directory that was made when script was run last or when script is closed

import os
from bs4 import BeautifulSoup
from selenium import webdriver
import tempfile
import requests


def stripURL(urlString):
    """
    Strips the URL to get the base URL and file extension
    :param urlString: URL string to be stripped
    :return: A list containing the base URL and file extension
    """
    
    # Split the URL string to get the base URL and parameters
    baseURL, params = urlString.split("?", 1)

    # Split the base URL to get the file extension
    filePath, fileExtension = baseURL.rsplit(".", 1)

    return [baseURL, fileExtension]


def downloadWebpage(workingDir, webpageUrl):
    """
    Downloads the webpage and saves it as an HTML file
    :param webpageUrl: URL of the webpage to be downloaded
    :param driverPath: Path to the chrome web driver
    :return: Absolute path of the saved HTML file
    """

    # Default output file path
    outputFile = os.path.join(workingDir, "webpage.html")

    # Initialize chrome web driver and get the webpage
    driver = webdriver.Chrome()
    driver.get(webpageUrl)

    # Get html content
    webpageContent = driver.page_source

    # Close the webdriver
    driver.quit()

    # Saving html content to file
    with open(outputFile, "w", encoding="utf-8") as f:
        f.write(webpageContent)

    print(f"Webpage downloaded and saved to '{outputFile}'")

    return outputFile


def filterMainContent(workingDir, htmlFilePath):
    """
    Filters the main content from the HTML file and saves it to a new file
    :param htmlFilePath: Path of the HTML file to be filtered
    :return: Absolute path of the filtered HTML file
    """

    # open html file and read it's content
    with open(htmlFilePath, 'r', encoding='utf-8') as file:
        htmlContent = file.read()

    # parse the html content using beautifulSoup
    soup = BeautifulSoup(htmlContent, 'html.parser')

    # find the section with a specific class name
    contentSection = soup.find('section', class_='mt-content-container')

    # check if required section is found
    if not contentSection:
        # Print a message if no section with class 'mt-content-container' is found
        print("No section with class 'mt-content-container' found.")
        return

    # remove footer
    footer = contentSection.find("footer", class_="mt-content-footer")
    if footer:
        footer.decompose()

    # convert content section to string
    requiredContent = str(contentSection)

    # Create a temporary HTML file in the working directory
    tempHtmlFilePath = os.path.join(workingDir, "filteredWebpage.html")

    with open(tempHtmlFilePath, 'w', encoding='utf-8') as f:
        f.write(requiredContent)

    print(f"Filtered content saved as '{tempHtmlFilePath}'")

    return tempHtmlFilePath


def handleImages(workingDir, htmlFilePath):
    """
    Downloads images from the HTML file and saves them to the working directory
    :param htmlFilePath: Path of the HTML file
    :return: Absolute path of the updated HTML file
    """

    # open html file and read it's content
    with open(htmlFilePath, 'r', encoding='utf-8') as file:
        htmlContent = file.read()

    # parse the html content using beautifulSoup
    soup = BeautifulSoup(htmlContent, 'html.parser')

    # find all image tags
    imageTags = soup.find_all('img')

    # list to store image file names
    imageFileNames = []

    # loop through all image tags
    for index, imageTag in enumerate(imageTags):
        # get the image source URL
        imageUrl, imageExt = stripURL(imageTag['src'])

        # download the image content
        imageContent = requests.get(imageUrl).content

        # save the image content to a file
        imageFileName = f"image_{index}.{imageExt}"
        imageFilePath = os.path.join(workingDir, imageFileName)

        with open(imageFilePath, 'wb') as f:
            f.write(imageContent)

        # append the image file name to the list
        imageFileNames.append(imageFileName)

        # replace the image tag with the image file name
        imageTag['src'] = imageFileName

    # save the updated html content to a file
    finalHtmlFilePath = os.path.join(workingDir, "finalWebpage.html")

    with open(finalHtmlFilePath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"Images downloaded and saved as '{imageFileNames}'")
    print(f"Final HTML content saved as '{finalHtmlFilePath}'")

    return finalHtmlFilePath


# driverPath = r"C:\Users\naved\Downloads\chromedriver_win32\chromedriver.exe"
url = "https://chem.libretexts.org/Bookshelves/Physical_and_Theoretical_Chemistry_Textbook_Maps/Physical_Chemistry_(LibreTexts)/01%3A_The_Dawn_of_the_Quantum_Theory/1.01%3A_Blackbody_Radiation_Cannot_Be_Explained_Classically"

# create a temporary directory to store data
workingDir = tempfile.mkdtemp()

# download the webpage
htmlFilePath = downloadWebpage(workingDir, url)
print("Path of saved HTML file", htmlFilePath)

# get the main content from the html file
filteredFilePath = filterMainContent(workingDir, htmlFilePath)
print("Path of filtered html file", filteredFilePath)

# download images from the html file
finalFilePath = handleImages(workingDir, filteredFilePath)
print("Path of final html file", finalFilePath)

# open html file folder in the browser (windows only)
os.startfile(workingDir)
