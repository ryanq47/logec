## sorter v2 auth.log -- only going for catching logins here 
## naming: item_action,

## error handling for imports
try:
    # == data handling
    import yaml

    # == data transformation
    import re

    # == data formatting
    import pandas as pd
    from tabulate import tabulate

    # == bells & whistles
    from rich.progress import track
    from rich import print

    # Debug/performance
    import imports
    import utility
    import logec

## == The goal with the error catching is to kick you back to the main shell if things are broken, thus leaving the program somewhat useable
## == most common error catching

except ModuleNotFoundError as e:
    ## termcolor *should* be installed by default
    from termcolor import colored
    print(colored("Missing a module, try pip install MODULE (printed below)", "yellow"))
    print(colored(e,"yellow"))

    ## == juming back to main loop on failure
    import logec
    logec.main()
    
## == Handling for any further unexepcted weird errors
except Exception as e:
    print(e)
    import logec
    logec.main()
    

## Loading all the data
class inits:
    def __init__(self):
        self.self = self

    def log_dir():
        with open("config/log_locations.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)
        return (cfg["syslog"]["auth"]["dir"])

    # Needs to be called from the shell script
    def search_term(input):
        return input

# == Constants

LOG_DIR = inits.log_dir()
#LOG_LINES/LIMIT =
SEARCH_TERM = inits.search_term


def debug():
    print(LOG_DIR)

class sorter:
    def __init__(self):
        self.self = self

    def sort():
        print(utility.size_check(LOG_DIR))
        ## File open
        with open(LOG_DIR, "r") as log_contents:
        
            ## filtering for each value
            for i in track(log_contents, description="Loading log file...", total=utility.file_count(LOG_DIR)):
                command = extract.command(i) 
                time = extract.time(i) 
                tty = extract.TTY(i)
                dir = extract.dir(i)
                user = extract.user(i)
                
                data_format = [(time, tty, user, dir, command)]

                ## line to filter out non shell login logs - need to get the session opened ones in as well
                if 'TTY' in i:
                    ## The for loop is for the formatting so pandas can read/index it properly
                    for i in data_format:
                        data.lst_init.df_list.append(i)
                else:
                    pass
                    #print("skipping line")

            display.dataframe()
            main()

    def search(search_term):
        print(utility.size_check(LOG_DIR))
        print(f"[blue]Search Term: {search_term}")

        with open(LOG_DIR, "r") as log_contents:

            for i in track(log_contents, description="Loading log file...", total = utility.file_count(LOG_DIR)):
                command = extract.command(i) 
                time = extract.time(i) 
                tty = extract.TTY(i)
                dir = extract.dir(i)
                user = extract.user(i)
                
                data_format = [(time, tty, user, dir, command)] ## list of what is ablove, ex ip, host, etc
                
                ## temp try except to fix search issues
                try:
                    if search_term in command:
                        add = True
               
                    else:
                        add = False
                        pass
                except Exception as e:
                    add = False
                    #print(e)
                    
                if add == True: 
                    for i in data_format:
                        data.lst_init.df_list_search.append(i)
            display.dataframe_search()
            main()
        
class display:
    
    ## seperate for my sanity
    def dataframe():
        display.dataframe_config()
        df = pd.DataFrame(data.lst_init.df_list, columns=['TIME','TTY','USER', 'DIR', 'COMMAND'])

        ## Setting astype which vastly reduces memory usage
        df["COMMAND"] = df["COMMAND"].astype('category').str[:45] #int16
        df["TTY"] = df["TTY"].astype('category')
        df["USER"] = df["USER"].astype('category') 
        df["DIR"] = df["DIR"].astype('category') 
        df["TIME"] = df["TIME"].astype('category')

    
        display.dataframe.df = df

    def dataframe_search():
        display.dataframe_config()
        df = pd.DataFrame(data.lst_init.df_list_search, columns=['TIME','TTY','USER', 'DIR', 'COMMAND'])
        
        ## Setting astype which vastly reduces memory usage
        df["COMMAND"] = df["COMMAND"].astype('category') #int16
        df["TTY"] = df["TTY"].astype('category') 
        df["USER"] = df["USER"].astype('category') 
        df["DIR"] = df["DIR"].astype('category') 
        df["TIME"] = df["TIME"].astype('category') 


        display.dataframe_search.df = df

    def dataframe_config():
        # == DF options - need to go into config file eventaully
        pd.options.display.width = 1
        #pd.set_option('display.max_columns', None)
        pd.options.display.max_rows = 100
        pd.options.display.max_colwidth = 1 # tightens up DF 
        
        pd.set_option("display.colheader_justify","left")

class data:
    def __init__(self):
        self.self = self
    # == call this function to reset lists back to 0 for memory cleanup, otherwise it just holds the lists in one spot
    def lst_init():
        
        data.lst_init.df_list = []
        data.lst_init.df_list_search = []
        ## any other lists init here
    
    def cleanup():
        data.lst_init()



class extract:
    def __init__(self):
        self.self = self
    
    def command(iter):
        command = re.compile(r'(COMMAND=).*')
        try:
            extracted_command = command.search(iter)[0]
            #print(extracted_command)
        except:
            extracted_command = "EMPTY"
        return extracted_command.replace("COMMAND=","")

    def TTY(iter):
        tty = re.compile(r'(TTY=)([^\s]+)')
        try:
            extracted_tty = tty.search(iter)[0]
            #print(extracted_command)
        except:
            extracted_tty = "EMPTY"
        return extracted_tty.replace("TTY=","")

    def dir(iter):
        dir= re.compile(r'(PWD=)([^\s]+)')
        try:
            extracted_dir = dir.search(iter)[0]
            #print(extracted_command)
        except:
            extracted_dir = "EMPTY"
        return extracted_dir.replace("PWD=","")

    def user(iter):
        user = re.compile(r'(USER=)([^\s]+)')
        try:
            extracted_user = user.search(iter)[0]
            #print(extracted_command)
        except:
            extracted_user = "EMPTY"
        return extracted_user.replace("USER=","") 


    def time(iter):
        time = re.compile(r'..:..:..')
        try:
            extracted_time = time.search(iter)[0]
            #print(extracted_command)
        except:
            extracted_time = "EMPTY"
        return extracted_time
    
def main():
    data.lst_init()
    
main()

