# sorter take 2
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

    # == Module Use
    from user_agents import parse

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
        return (cfg["webserver"]["dir"])

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
                ip = extract.ip(i) #"127.0.0.1"
                data.lst_stats.ip.append(ip)
                time = extract.time(i) #"TIME"
                geo = extract.geo(i) #"GEO"
                code = extract.code(i) #"400"
                data.lst_stats.code.append(i)
                method = extract.method(i) #"test"
                url = extract.url(i) #"test"
                agent = extract.user_agent(i) ## << SLOW

                data_format = [(ip, time, geo, method, code, url, agent)]

                ## The for loop is for the formatting so pandas can read/index it properly
                for i in data_format:
                    data.lst_init.df_list.append(i)
            display.dataframe()



    def search(search_term):
        print(utility.size_check(LOG_DIR))
        print(f"[blue]Search Term: {search_term}")

        with open(LOG_DIR, "r") as log_contents:

            for i in track(log_contents, description="Loading log file...", total = utility.file_count(LOG_DIR)):
                ip = extract.ip(i) #"127.0.0.1"
                data.lst_stats.ip.append(ip)
                time = extract.time(i) #"TIME"
                geo = extract.geo(i) #"GEO"
                code = extract.code(i) #"400"
                data.lst_stats.code.append(i)
                method = extract.method(i) #"test"
                url = extract.url(i) #"test"
                agent = extract.user_agent(i) ## << SLOW
                

                data_format = [(ip, time, geo, method, code, url, agent)]
                
                ## temp try except to fix search issues
                try:
                    if search_term in ip:
                        add = True
                    elif search_term in time:
                        add = True        
                    elif search_term in geo:
                        add = True
                    elif search_term in code:
                        add = True   
                    elif search_term in method:
                        add = True
                    elif search_term in url:
                        add = True         
                    elif search_term in str(agent):
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

class display:
    
    ## seperate for my sanity
    def dataframe():
        display.dataframe_config()
        df = pd.DataFrame(data.lst_init.df_list, columns=['IP', 'TIME', 'LOCATION', 'METHOD', 'RESPONSE_CODE', 'URL', 'AGENT'])

        df["RESPONSE_CODE"] = df["RESPONSE_CODE"].astype('category') #int16
        df["IP"] = df["IP"].astype('category') 
        df["TIME"] = df["TIME"].astype('category') 
        df["LOCATION"] = df["LOCATION"].astype('category') 
        df["METHOD"] = df["METHOD"].astype('category') 
        df["URL"] = df["URL"].astype('category') 
        df["AGENT"] = df["AGENT"].astype('category')      
          
        display.dataframe.df = df

    def dataframe_search():
        display.dataframe_config()
        df = pd.DataFrame(data.lst_init.df_list_search, columns=['IP', 'TIME', 'LOCATION', 'METHOD', 'RESPONSE_CODE', 'URL', 'AGENT'])

        df["RESPONSE_CODE"] = df["RESPONSE_CODE"].astype('category') #int16
        df["IP"] = df["IP"].astype('category') 
        df["TIME"] = df["TIME"].astype('category') 
        df["LOCATION"] = df["LOCATION"].astype('category') 
        df["METHOD"] = df["METHOD"].astype('category') 
        df["URL"] = df["URL"].astype('category') 
        df["AGENT"] = df["AGENT"].astype('category')
        
        display.dataframe_search.df = df

    def dataframe_config():
        # == DF options - need to go into config file eventaully
        pd.options.display.max_rows = 30
        pd.options.display.max_colwidth = 1 # tightens up DF 
        
        pd.set_option("display.colheader_justify","left")
    
    def stats():
        try:
            message = (f"Unique IP's: {utility.stats.num_unique(data.lst_stats.ip)} ")
            ## Nuking the lists after they hit the last function to be called, stats
            data.cleanup()
            return(message)
        except:
            data.cleanup()
            return("Data not found")
        

class data:
    def __init__(self):
        self.self = self
    # == call this function to reset lists back to 0 for memory cleanup, otherwise it just holds the lists in one spot
    def lst_init():
        
        data.lst_init.df_list = []
        data.lst_init.df_list_search = []
        ## any other lists init here
    def lst_stats():
        data.lst_stats.ip = []
        data.lst_stats.code = []
        
    ## used for freeing memory at the end of whatever
    def cleanup():
        data.lst_init()
        data.lst_stats()



class extract:
    def __init__(self):
        self.self = self
    
    def ip(iter):
        ip_address = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        try:
            extracted_ip = ip_address.search(iter)[0]
        except:
            extracted_ip = None
            #print("Error Occured")
        return extracted_ip
    
    def time(iter):
        time = re.compile(r'\[(.*?)\]')
        try:
            extracted_time = time.search(iter)[0]
        except Exception as e:
            extracted_time = None
        return extracted_time

    def geo(iter):
        time = re.compile(r'\d{3}')
        try:
            extracted_geo = time.search(iter)[0]
        except Exception as e:
            extracted_geo = None
        return extracted_geo

    def code(iter):
        code = re.compile(r'HTTP/1.1" (200|304|401|403|404|^400$|^500$)')
        try:
            #extracted_code = re.search('HTTP/1.1" (200|304|401|403|404|^400$|^500$)', iter)[0]
            extracted_code = code.search(iter)[0]
        except Exception as e:
            extracted_code = None
        return extracted_code

    def method(iter):
        method = re.compile(r'(GET|POST|HEAD|DELETE|PUT|CONNECT|OPTIONS|TRACE|PATCH)')
        try:
            extracted_method = method.search(iter)[0]
        except Exception as e:
            extracted_method = None
        return extracted_method

    def url(iter):
        url = re.compile(r'(GET|POST|HEAD|DELETE|PUT|CONNECT|OPTIONS|TRACE|PATCH) ([^\s]+)')
        try:
            extracted_url = url.search(iter)[0]
        except Exception as e:
            extracted_url = None
        return extracted_url

    def user_agent(iter):
        user_agent = re.compile(r'\(([^(]*)\)')
        try:
            extracted_user_agent_raw = user_agent.search(iter)[0]
            
            extracted_user_agent = parse(extracted_user_agent_raw)
            
        except Exception as e:
            extracted_user_agent = None
        return extracted_user_agent
        ## doc: https://www.otsukare.info/2013/10/02/ua-parsing
        ##      https://pypi.org/project/user-agents/


## Main function, will run no matter what is called from a shell, so handy if you need to do things
## such as initializing lists or variables
def main():
    ## This is here to fix the dataframes getting wiped on multiple calls to parse the logs
    data.lst_init()
    data.lst_stats()
    
main()