import os
from platformdirs import user_data_dir
import json


class State:
    def __init__(self):
        appDataDir = user_data_dir("webpage-downloader", appauthor="clientproject")

        # check if the directory exists
        if not os.path.exists(appDataDir):
            os.makedirs(appDataDir)

        # check if json config file exists
        configPath = os.path.join(appDataDir, "config.json")
        if not os.path.exists(configPath):
            with open(configPath, "w") as f:
                json.dump({"savePath": ""}, f)

        # read the config file
        with open(configPath, "r") as f:
            config = json.load(f)

        self.configPath: str = configPath

        # check if savePath is in config
        if "savePath" not in config:
            config["savePath"] = ""
        if "downloadURL" not in config:
            config["downloadURL"] = ""
        if "workingPath" not in config:
            config["workingPath"] = ""

        self.savePath: str = config["savePath"]
        self.downloadURL: str = config["downloadURL"]
        self.workingPath: str = config["workingPath"]

    def setSavePath(self, savePath):
        self.savePath = savePath
        self.saveConfig()

    def setDownloadURL(self, downloadURL):
        self.downloadURL = downloadURL
        self.saveConfig()

    def setWorkingPath(self, workingPath):
        self.workingPath = workingPath
        self.saveConfig()

    def saveConfig(self):
        """
        Saves the current state to the config file
        """

        with open(self.configPath, "w") as f:
            json.dump(
                {
                    "savePath": self.savePath,
                    "downloadURL": self.downloadURL,
                    "workingPath": self.workingPath,
                },
                f,
            )
