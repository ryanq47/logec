from turtle import setundobuffer
## startup scripting based on settings
import yaml
from rich import print

import imports
import update
import logec

## This exsits to call this function/module, yes I know this is not the best way to do this
def main():
    pass

## == Loading config file
with open("config/general_config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)


## == startip values
AUTO_UPDATE = cfg["startup"]["auto-update"]
PRINT_ON_STARTUP = cfg["startup"]["print-settings-on-startup"]


## == Logic
if  AUTO_UPDATE == True:
    update.main()

if PRINT_ON_STARTUP == True:
    print(f'''
AUTO_UPDATE: {AUTO_UPDATE}
PRINT_ON_STARTUP: {PRINT_ON_STARTUP}
    ''')