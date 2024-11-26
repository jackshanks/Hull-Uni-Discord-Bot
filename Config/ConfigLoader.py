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

    @property
    def welcome_role(self):
        return self.config['welcome_role']

    @property
    def colour(self):
        return self.config['colour']

    @property
    def quote_channels(self):
        return self.config['quote_channels']

    @property
    def star_ratio(self):
        return self.config['star_ratio']

    @property
    def star_quote_channel(self):
        return self.config['star_quote_channel']

    @property
    def delete_ratio(self):
        return self.config['delete_ratio']

    @property
    def delete_channel(self):
        return self.config['delete_channel']

    @property
    def game(self):
        return self.config['game']


