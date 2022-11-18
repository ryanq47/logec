## sorter v2
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
        return (cfg["syslog"]["dpkg"]["dir"])

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
                time = extract.time(i) 
                date = extract.date(i) 
                message = extract.dpkg_message(i) 
                
                data_format = [(date, time, message)]
                
                if "status installed" in i:
                    data.lst_stats.installed_package.append(i)
                else:
                    pass

                ## The for loop is for the formatting so pandas can read/index it properly
                for i in data_format:
                    data.lst_init.df_list.append(i)

            display.dataframe()


    def search(search_term):
        print(utility.size_check(LOG_DIR))
        print(f"[blue]Search Term: {search_term}")

        with open(LOG_DIR, "r") as log_contents:

            for i in track(log_contents, description="Loading log file...", total = utility.file_count(LOG_DIR)):
                time = extract.time(i)
                date = extract.date(i) 
                message = extract.dpkg_message(i) 

                data_format = [(date, time, message)] ## list of what is ablove, ex ip, host, etc
                
                ## temp try except to fix search issues
                try:
                    if search_term in time:
                        add = True
                    elif search_term in date:
                        add = True     
                    elif search_term in message:
                        add = True             
                    else:
                        add = False
                        pass
                except Exception as e:
                    add = False
                    print(e)
                    
                if add == True: 
                    if "succesfully installed" in i:
                        data.lst_stats.installed_package.append(i)
                        
                    for i in data_format:
                        data.lst_init.df_list_search.append(i)
                        

                    
            display.dataframe_search()
        
    
class display:
    
    ## seperate for my sanity
    def dataframe():
        display.dataframe_config()
        df = pd.DataFrame(data.lst_init.df_list, columns=['DATE','TIME','MESSAGE'])
        
        ## Setting astype which vastly reduces memory usage
        df["TIME"] = df["TIME"].astype('category') #int16
        df["DATE"] = df["DATE"].astype('category') #int16    
        df["MESSAGE"] = df["MESSAGE"].astype('category')          
        display.dataframe.df = df

    def dataframe_search():
        display.dataframe_config()
        df = pd.DataFrame(data.lst_init.df_list_search, columns=['DATE','TIME','MESSAGE'])
        
        df["TIME"] = df["TIME"].astype('category')
        df["DATE"] = df["DATE"].astype('category') 
        df["MESSAGE"] = df["MESSAGE"].astype('category')
        display.dataframe_search.df = df

    def dataframe_config():
        # == DF options - need to go into config file eventaully
        pd.options.display.max_rows = 30
        pd.options.display.max_colwidth = 1 # tightens up DF 
        
        pd.set_option("display.colheader_justify","left")

    def stats():
        try:
            message = (f"Installed Packages (according to log) {utility.stats.num_count(data.lst_stats.installed_package)}")
            print()
            ## Nuking the lists after they hit the last function to be called, stats
            data.cleanup()
            return(message)
        except:
            data.cleanup()
            return("stats not found")

class data:
    def __init__(self):
        self.self = self
    # == call this function to reset lists back to 0 for memory cleanup, otherwise it just holds the lists in one spot
    def lst_init():
        
        data.lst_init.df_list = []
        data.lst_init.df_list_search = []
        ## any other lists init here
    
    def lst_stats():
        data.lst_stats.installed_package = []
        
    ## used for freeing memory at the end of whatever
    def cleanup():
        data.lst_init()
        data.lst_stats()


class extract:
    def __init__(self):
        self.self = self
    
    def time(iter):
        time = re.compile(r'..:..:..')
        try:
            extracted_time = time.search(iter)[0]
            #print(extracted_command)
        except:
            extracted_time = "EMPTY"
        return extracted_time

    def date(iter):
        date = re.compile(r'....-..-..')
        try:
            extracted_date = date.search(iter)[0]
            #print(extracted_command)
        except:
            extracted_date = "EMPTY"
        return extracted_date
    
    def dpkg_message(iter):
        message = re.compile(r'.*')
        try:
            extracted_message = message.search(iter)[0]
            #print(extracted_command)
        except:
            extracted_message = "EMPTY"
            # was easier to grab whole message then just cut out first 20 lines, as those will stay the same
        return extracted_message[20:]


def main():
    data.lst_init()
    data.lst_stats()
    
main()