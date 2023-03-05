from configparser import ConfigParser, NoSectionError
import os.path
from . import root_dir

__config_file__ = os.path.join(root_dir, "config.ini")

config = ConfigParser()

if os.path.exists(__config_file__):
    config.read(__config_file__)


def get_digitalocean_token():
    try:
        return config.get("digitalocean", "token")
    except NoSectionError:
        print(
            'DigitalOcean token not config. Please run "utils digitalocean config" to add token.'
        )
        return None


def set_digitalocean_token(token):
    try:
        config.set("digitalocean", "token", token)
    except NoSectionError:
        config["digitalocean"] = {"token": token}
    finally:
        with open(__config_file__, "w") as configfile:
            config.write(configfile)
        print("DigitalOcean token updated.")

def get_flomo_url():
    try:
        return config.get("flomo", "url")
    except NoSectionError:
        print(
            'Flomo url not config. Please run "utils note flomo config" to add url.'
        )
        return None


def set_flomo_url(url):
    try:
        config.set("flomo", "url", url)
    except NoSectionError:
        config["flomo"] = {"url": url}
    finally:
        with open(__config_file__, "w") as configfile:
            config.write(configfile)
        print("Flomo url updated.")