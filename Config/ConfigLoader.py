import urllib
import urllib.request
import yaml

CONFIG_URL = "https://raw.githubusercontent.com/jackshanks/Hull-Uni-Discord-Bot/refs/heads/dev/config.yml"

class Config():
    config : dict = dict()

    def LoadConfig():
        x = urllib.request.urlopen(CONFIG_URL)
        Config.config = yaml.safe_load(x)