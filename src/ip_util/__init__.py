from configparser import ConfigParser
import os

__config_file__ = 'config.ini'

config = ConfigParser()

if os.path.exists(__config_file__):
    config.read(__config_file__)
else:
    raise FileExistsError('Please create "config.ini" from example "config.example.ini".')