#!/usr/bin/python3

import os
import subprocess as sp
 
import pyfiglet
from rich import print

import imports
import utility
import auth_sorter as auth
import logec ## aka parent shell

import signal

## log_functions imports

## tab completion imports:
import readline
readline.parse_and_bind("tab: complete")

def loop():
    while True:
        main()

def main():
    ## setting up tab completer
    readline.set_completer(tab_completion)

    user_input = input("\n|logec: Auth-log> ")
    c = command(user_input)

    if c != None:
        print(c)

def tab_completion(text,state):  
    # autofill words   
    vocab = ['log','search','info']
    results = [x for x in vocab if x.startswith(text)] + [None]
    return results[state]

def ctrl_c(signum, frame):
    print("\n|logec: exiting")
    exit()
signal.signal(signal.SIGINT, ctrl_c)

## could and should use match case here, but for compatability gonna stick to if elifs
def command(input):
    if input == "exit":
        exit()

    elif input == "home":
        logec.main()

    elif input == "clear":
        loop_func.cli_clear()
        return None

    elif input == "whoami":
        return(loop_func.os_whoami())

    elif input == "banner":
        return(loop_func.logec_banner())

    elif input == "info":
        print("""Auth is a module which pulls successful logins from the auth.log file in linx.

        Pros:
            - Easy view of current/past sessions
        Cons:
            - Does not include all of auth.log, only succesful (and potentially local) logins

Example Log:
   TIME      TTY    USER  DIR           COMMAND  
2  14:35:42  pts/1  root  /var/log      /usr/bin/nano auth.log  
        """)


    elif input == "log":
        auth.sorter.sort()
        print(auth.display.dataframe.df)

    elif "search" in input:
        search_term = input.replace("search ", "")
        auth.sorter.search(search_term)
        print(auth.display.dataframe_search.df)

    else:
        #print("TEMP DEBUG FEATURE. DANGEROUS")
        #os.system(input)
        return("Invalid Command")


class loop_func:
    def __init__(self):
        self.self = self
    
    def cli_clear():
        if os.name == 'nt':
            _ = os.system('cls')
    
        else:
            _ = os.system('clear')

    def os_whoami():
        a = sp.getoutput("whoami")
        return(a)
    def logec_banner():
        banner = pyfiglet.figlet_format("LOGEC: WEBSERVER", font = "pagga")
        return(f"[green]{banner}")

import yaml

class log_function():
    def __init__(self):
        self.self = self
    
    def config_file():

        with open("config/log_locations.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)
        return (cfg["webserver"]["dir"])



if __name__ == "__main__":
    print(loop_func.logec_banner())
    while True:
        loop()

## need to implement os passthrough option so user can stay in this shell and issue os commands, have to get autocomplete 
# and history working though

## maybe create a nested shell for each program (wathcer etc) and have it use this ^ template.
## then the shell name will be either "logec/watcher" for directory based or just "logec-watcher>"