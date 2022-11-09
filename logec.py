#!/usr/bin/python3
import sys
from xml.dom.minidom import Attr
try:
    ## This is the top level shell, it will reach out to a per module shell based on inputs given to it

    import os
    import subprocess as sp
    import time
    
    import pyfiglet
    from rich import print

    import imports 
    import startup
    ## Note, each import is within its own elif statement to save startup time
    ## importing readline for tab compeltion and history
    import readline
    readline.parse_and_bind("tab: complete")

    ## This function is for callback from child shells to run this whole thing (name = main does not work cause it's not being run directly)
    def main():
        while True:
            loop()

    def loop():
        ## setting up tab completer
        readline.set_completer(tab_completion)

        user_input = input("\n|logec> ")
        c = command(user_input)

        if c != None:
            print(c)

    def tab_completion(text,state):
        vocab = ['help','whoami', 'banner', 'exit', 'clear', 'webserver','auth', 'reputation']
        results = [x for x in vocab if x.startswith(text)] + [None]
        return results[state]

    ## Importing modules at runtime to speed up initial loading
    def command(input):
        if input == "exit":
            exit()
            ## Need a way to not prevent exiting if usr shell is the python/logec shell
        elif input == "help":
            print("""
Type any one of these commands: 

Modules:
    webserver (apache2)
    auth      (auth.log)

Tools: 
    reputation  -  Check the reputation of an IP
    integrity   -  Check if your files have been tampered with by comparing with
                   a local copy! (Not Fully Functional yet)

Hit tab for all commands, or autofill

                  """)

        elif input == "reload":
            shell_func.reload()

        elif input == "clear":
            shell_func.cli_clear()
            return None
        
        elif input == "update":
            import update
            update.main()

        elif input == "whoami":
            return(shell_func.os_whoami())

        elif input == "banner":
            return(shell_func.logec_banner())

        # == Log Modules 
        
        elif input == "webserver":
            import ws_shell as wss
            wss.loop()

        elif input == "auth":
            import auth_shell as ass
            ass.loop()
     
        # == Tools
        elif input == "tools":
            print("tools: iprep")

            #ip_rep
        elif input == "reputation":
            import ip_rep
            print(f"Malicious IP's: {ip_rep.main_functions.main_shell()}")

        elif input == "integrity":
            import integrity
            integrity.main_shell()

        ## PIP -- !! Warning, potentially dangerous, can possibly pop a shell with this!!
        elif "pip" in input:
            ## official reccomended way of installing packages
            import subprocess
            package = input.replace("pip install ", "")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            ## Reload to fix import error
            ## maybe fix with os.system("/opt/logec/logec.py")    
            print("Please restart shell, exiting in 3 seconds")
            time.sleep(3)
            exit()
        ## ==  Extra responses
        elif input == "home":
            print("You are already home")
        else:
            print("DANGEROUS< for debig only")
            os.system(input)
            #return("Invalid Command")


    class shell_func:
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
            banner = pyfiglet.figlet_format("LOGEC", font = "pagga")
            return(f"[green]{banner}")

        def reload():
            shell_func.cli_clear()
            print("Reloading...")
            exec(open("logec.py").read())

except Exception as e:
    print(e)



if __name__ == "__main__":
    startup.main()
    print(shell_func.logec_banner())
    while True:
        loop()
