import urllib
import urllib.request
import yaml

CONFIG_URL = "https://raw.githubusercontent.com/jackshanks/Hull-Uni-Discord-Bot/refs/heads/dev/config.yml"


class Config:
    _instance = None
    config: dict = dict()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self.config == dict():
            self.LoadConfig()

    def LoadConfig(self):
        x = urllib.request.urlopen(CONFIG_URL)
        self.config = yaml.safe_load(x)

    @property
    def guild_ids(self):
        return self.config['guild_ids']
