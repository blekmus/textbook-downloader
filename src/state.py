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

        # check if savepath is in config
        if "savePath" not in config:
            config["savePath"] = ""
        if "downloadURL" not in config:
            config["downloadURL"] = ""

        self.savePath: str = config["savePath"]
        self.downloadURL: str = config["downloadURL"]

    def setSavePath(self, savePath):
        self.savePath = savePath

        with open(self.configPath, "w") as f:
            json.dump({"savePath": self.savePath, "downloadURL": self.downloadURL}, f)

        return True

    def setDownloadURL(self, downloadURL):
        self.downloadURL = downloadURL

        with open(self.configPath, "w") as f:
            json.dump({"savePath": self.savePath, "downloadURL": self.downloadURL}, f)

        return True
