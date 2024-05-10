import os
from bs4 import BeautifulSoup
from selenium import webdriver
import tempfile
import requests
from src.state import State
from datetime import datetime
from selenium.webdriver.chrome.options import Options as ChromeOptions
import shutil


class WebScrape:
    def __init__(self, state: State):
        self.workingDir = tempfile.mkdtemp(prefix="webpage-downloader-")
        self.appState = state

        # set working path in state
        state.setWorkingPath(self.workingDir)

    def downloadWebpage(self):
        """
        Downloads the webpage and saves it as an HTML file
        """

        # Default output file path
        self.originalPage = os.path.join(self.workingDir, "originalPage.html")

        chromeOptions = ChromeOptions()
        chromeOptions.add_argument("--headless")
        driver = webdriver.Chrome(options=chromeOptions)

        # Initialize chrome web driver and get the webpage
        driver.get(self.appState.downloadURL)

        # Get html content
        webpageContent = driver.page_source

        # save page title
        self.pageTitle = driver.title

        # Close the webdriver
        driver.quit()

        # Saving html content to file
        with open(self.originalPage, "w", encoding="utf-8") as f:
            f.write(webpageContent)

    def filterMainContent(self):
        """
        Filters the main content from the HTML file and saves it to a new file
        """

        # open html file and read it's content
        with open(self.originalPage, "r", encoding="utf-8") as file:
            htmlContent = file.read()

        # parse the html content using beautifulSoup
        soup = BeautifulSoup(htmlContent, "html.parser")

        # find the section with a specific class name
        contentSection = soup.find("section", class_="mt-content-container")

        # check if required section is found
        if not contentSection:
            # Print a message if no section with class 'mt-content-container' is found
            print("No section with class 'mt-content-container' found.")
            return

        # remove footer
        footer = contentSection.find("footer", class_="mt-content-footer")
        if footer:
            footer.decompose()

        # remove all elements with class MathJax_Processing
        for element in contentSection.find_all(class_="MathJax_Processing"):
            element.decompose()

        # replace all MathJax_Display divs with their text content
        for element in contentSection.find_all(class_="MathJax_Preview"):
            element.replace_with(element.get_text())

        # remove all script tags
        for script in contentSection.find_all("script"):
            script.decompose()

        # convert content section to string
        requiredContent = str(contentSection)

        # Create a temporary HTML file in the working directory
        self.contentFilterPage = os.path.join(self.workingDir, "contentfilter.html")

        with open(self.contentFilterPage, "w", encoding="utf-8") as f:
            f.write(requiredContent)

    def handleImages(self):
        """
        Downloads images from the HTML file and saves them to the working directory
        """

        # open html file and read it's content
        with open(self.contentFilterPage, "r", encoding="utf-8") as file:
            htmlContent = file.read()

        # parse the html content using beautifulSoup
        soup = BeautifulSoup(htmlContent, "html.parser")

        # find all image tags
        imageTags = soup.find_all("img")

        # list to store image file names
        self.imageFileNames = []

        # loop through all image tags
        for index, imageTag in enumerate(imageTags):
            # get the image source URL
            imageUrl, imageExt = self.stripURL(imageTag["src"])

            # download the image content
            imageContent = requests.get(imageUrl).content

            # save the image content to a file
            imageFileName = f"image_{index}.{imageExt}"
            imageFilePath = os.path.join(self.workingDir, imageFileName)

            with open(imageFilePath, "wb") as f:
                f.write(imageContent)

            # append the image file name to the list
            self.imageFileNames.append(imageFileName)

            # replace the image tag with the image file name
            imageTag["src"] = imageFileName

        # save the updated html content to a file
        self.imageFilterPage = os.path.join(self.workingDir, "imageFilterPage.html")

        with open(self.imageFilterPage, "w", encoding="utf-8") as f:
            f.write(str(soup))

    def saveFiles(self):
        """
        Saves the files to the save directory
        """

        # create dir name in format pagetitle | YYYY-MM-DD_HH-MM-SS
        now = datetime.now()
        dirTitle = now.strftime("%Y-%m-%d_%H-%M-%S")

        # Create a new directory in the output directory
        self.appState.outputDir = os.path.join(self.appState.savePath, dirTitle)
        os.makedirs(self.appState.outputDir)

        # Copy the files to the output directory
        os.rename(
            self.imageFilterPage, os.path.join(self.appState.outputDir, "index.html")
        )

        for imageFileName in self.imageFileNames:
            os.rename(
                os.path.join(self.workingDir, imageFileName),
                os.path.join(self.appState.outputDir, imageFileName),
            )

    def cleanup(self):
        """
        Cleans up the working directory
        """

        # Remove the working directory
        shutil.rmtree(self.workingDir)

    def stripURL(self, urlString):
        """
        Strips the URL to get the base URL and file extension
        :param urlString: URL string to be stripped
        :return: A list containing the base URL and file extension
        """

        # Split the URL string to get the base URL and parameters
        baseURL = urlString.split("?", 1)[0]

        # Split the base URL to get the file extension
        fileExtension = baseURL.rsplit(".", 1)[1]

        return [baseURL, fileExtension]
