import yaml
import shutil
import os

import imports
import logec


with open("config/log_locations.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)

webserver = cfg["integrity"]["webserver"]["dir"]


def module_shell():
    pass


def main_shell():
    user_input = input("Choose an option: \n1) Compare \n2) Copy \n3) restore\n4) Home\n")
    if  user_input == "1":
        function.compare()
    elif user_input == "2":
        function.copy(webserver)
    elif user_input == "3":
        confirmation = input("Are you sure? (y/n)")
        if confirmation == "y":
            function.restore()
        else:
            main_shell()

    elif user_input == "4":
        logec.main()
    #print(cfg["integrity"]["webserver"]["dir"])


class function:

    def compare():
        pass
    ## Good way  to do it: https://www.geeksforgeeks.org/how-to-compare-two-text-files-in-python/

    def copy(file_path):
        basename = os.path.basename(file_path)
        shutil.copy(file_path, f"Modules/tools/integrity/golden_copies/{basename}")
        print(f"{basename} snapshotted")


    def restore():
        print("RESTORED FILES...")
        pass ## restores golden copies