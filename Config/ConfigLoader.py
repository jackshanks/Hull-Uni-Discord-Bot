import urllib
import urllib.request
import json

CONFIG_URL = "https://raw.githubusercontent.com/jackshanks/Hull-Uni-Discord-Bot/refs/heads/dev/config.json"

def SafeError(func):
    def wrapper():
        try:
            func()
        except Exception:
            print(Exception)
    return wrapper

class Config():
    config : dict = dict()

    @SafeError
    def LoadConfig():
        x = urllib.request.urlopen(CONFIG_URL)
        out = ""
        for line in x:
            out += line.decode('utf-8') + "\n"
        out = out.strip()
        Config.config = json.loads(out)
    
Config.LoadConfig()