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
                ITEM = extract._ITEM(i) 


                ## Doc: https://www.geeksforgeeks.org/creating-a-pandas-dataframe-using-list-of-tuples/
                ## optmizing tuple: https://www.geeksforgeeks.org/tips-to-reduce-python-object-size/
                ## tuple in a list, much easier on memry than dict in a list

                data_format = [(ITEM)]

                ## The for loop is for the formatting so pandas can read/index it properly
                for i in data_format:
                    data.lst_init.df_list.append(i)

            display.dataframe()
            main()


    def search(search_term):
        print(utility.size_check(LOG_DIR))
        print(f"[blue]Search Term: {search_term}")

        with open(LOG_DIR, "r") as log_contents:

            for i in track(log_contents, description="Loading log file...", total = utility.file_count(LOG_DIR)):
                ITEM = extract._ITEM(i) 

                data_format = [(ITEM)] ## list of what is ablove, ex ip, host, etc
                
                ## temp try except to fix search issues
                try:
                    if search_term in ITEM_FUNCTION:
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
        df = pd.DataFrame(data.lst_init.df_list, columns=['IP', 'TIME', 'LOCATION', 'METHOD', 'RESPONSE_CODE', 'URL', 'AGENT'])
        #df.style.set_properties(**{'text-align': 'left'})
        #To reduce mem usage, can set types like this (int8 = -128 to 127, int16 = -32k to 32k)
        ## However, still getting mem spikes, so maybe these need to go infront somehow
        #doc: https://skytowner.com/explore/reducing_dataframe_memory_size_in_pandas#:~:text=There%20are%20two%20main%20ways%20to%20reduce%20DataFrame,types%202%20Convert%20object%20columns%20to%20categorical%20columns
        
        ## Setting astype which vastly reduces memory usage
        df["ITEM"] = df["ITEM"].astype('category') #int16
    
          
        display.dataframe.df = df

    def dataframe_search():
        display.dataframe_config()
        df = pd.DataFrame(data.lst_init.df_list_search, columns=['ITEM'])
        
        #df.style.set_properties(**{'text-align': 'left'})
        #To reduce mem usage, can set types like this (int8 = -128 to 127, int16 = -32k to 32k)
        ## However, still getting mem spikes, so maybe these need to go infront somehow
        #doc: https://skytowner.com/explore/reducing_dataframe_memory_size_in_pandas#:~:text=There%20are%20two%20main%20ways%20to%20reduce%20DataFrame,types%202%20Convert%20object%20columns%20to%20categorical%20columns
        
        ## Setting astype which vastly reduces memory usage
        df["ITEM"] = df["ITEM"].astype('category') #int16

        display.dataframe_search.df = df

    def dataframe_config():
        # == DF options - need to go into config file eventaully
        pd.options.display.max_rows = 30
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
    
    ## used for freeing memory at the end of whatever
    def cleanup():
        data.lst_init()



class extract:
    def __init__(self):
        self.self = self
    
    def _ITEM(iter):
        ITEM = re.compile(r'???')
        try:
            extracted_ITEM = ITEM.search(iter)[0]
        except:
            extracted_ITEM  = None
            #print("Error Occured")
        return extracted_ITEM 
    


def main():
    data.lst_init()
    
main()