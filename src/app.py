import customtkinter
from tkinter.filedialog import askdirectory
from src.state import State
from src.webscrape import WebScrape
import subprocess
import sys
import os

customtkinter.set_appearance_mode("System")


class App(customtkinter.CTk):
    def __init__(self, state: State):
        super().__init__()

        # set state
        self.appState = state

        # configure window
        self.title("Webpage Downloader")
        self.geometry(f"{600}x{360}")

        # configure grid layout
        self.grid_columnconfigure(4, weight=0)
        self.grid_columnconfigure((1, 2, 3, 5), weight=1)
        # self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure((1, 2, 3, 5), weight=0)
        self.grid_rowconfigure((6, 7), weight=1)

        # title label
        self.logoLabel = customtkinter.CTkLabel(
            self,
            text="Webpage Downloader",
            font=customtkinter.CTkFont(size=22, weight="bold"),
        )
        self.logoLabel.grid(
            row=1, column=1, columnspan=5, padx=20, pady=(20, 10), sticky="new"
        )

        self.credit = customtkinter.CTkLabel(
            self,
            text="Made by Dinil & Mohd Naved",
            font=customtkinter.CTkFont(size=14),
        )
        self.credit.grid(
            row=2, column=1, columnspan=5, padx=0, pady=(0, 20), sticky="new"
        )

        # save path label
        self.savePathLabel = customtkinter.CTkLabel(
            self, text="Save downloaded document to:", anchor="w"
        )
        self.savePathLabel.grid(
            row=3, column=1, padx=20, pady=(10, 0), columnspan=5, sticky="nw"
        )

        # save path entry
        self.saveEntry = customtkinter.CTkEntry(self)
        self.saveEntry.grid(
            row=4, column=1, padx=20, pady=(10, 0), sticky="nwe", columnspan=4
        )
        self.saveEntry.insert(0, self.appState.savePath)

        # save path button
        self.savePathButton = customtkinter.CTkButton(
            self, text="Select Folder", command=self.openSavePathSelector
        )
        self.savePathButton.grid(
            row=4, column=4, padx=20, pady=(10, 0), sticky="ne", columnspan=2
        )

        # download path label
        self.urlLabel = customtkinter.CTkLabel(self, text="Document URL:", anchor="w")
        self.urlLabel.grid(
            row=5, column=1, padx=20, pady=(10, 0), columnspan=5, sticky="nw"
        )

        # download path entry
        self.urlEntry = customtkinter.CTkEntry(
            self, placeholder_text="Paste the URL here"
        )
        self.urlEntry.grid(
            row=6, column=1, padx=20, pady=(10, 0), sticky="nwe", columnspan=6
        )
        self.urlEntry.insert(0, self.appState.downloadURL)

        # download button
        self.downloadButton = customtkinter.CTkButton(
            self, text="Download", command=self.handleDownload
        )
        self.downloadButton.grid(
            row=7, column=1, padx=20, pady=(10, 0), sticky="nw", columnspan=4
        )

    def openSavePathSelector(self):
        directory = os.path.abspath(askdirectory())
        self.appState.setSavePath(directory)
        self.saveEntry.delete(0, "end")
        self.saveEntry.insert(0, directory)

    def handleDownload(self):
        self.appState.setDownloadURL(self.urlEntry.get())
        scraper = WebScrape(self.appState)

        # download the webpage
        scraper.downloadWebpage()

        # filter the main content
        scraper.filterMainContent()

        # handle the images
        scraper.handleImages()

        # save the file to the save path
        scraper.saveFiles()

        self.downloadButton.configure(
            text="Downloaded!", fg_color="green", state="normal"
        )

        if sys.platform == 'darwin':
            subprocess.check_call(["open", "--", self.appState.outputDir])
        elif sys.platform == 'linux2':
            subprocess.check_call(["xdg-open", "--", self.appState.outputDir])
        elif sys.platform == 'win32':
            subprocess.check_call(["explorer", self.appState.outputDir])
