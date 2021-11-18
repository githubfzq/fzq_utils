from configparser import ConfigParser
import os.path
from .. import root_dir, package_root

module_root = os.path.join(package_root, 'ip_util')
__config_file__ = os.path.join(root_dir, 'config.ini')

config = ConfigParser()

if os.path.exists(__config_file__):
    config.read(__config_file__)
else:
    raise FileExistsError('Please create "config.ini" from example "config.example.ini".')