try:
    import os, sys
    import psutil
    import subprocess as sp
    import re


    # getting time
    from datetime import datetime

except ModuleNotFoundError as e:
    ## termcolor *should* be installed by default
    from termcolor import colored
    print(colored(f"[{__name__}.py Error]","red"))
    print(colored("Missing a module, try pip install MODULE (printed below)", "yellow"))
    print(colored(e,"yellow"))

    ## == juming back to main loop on failure
    import logec
    logec.main()

except Exception as e:
    print("PY: utility.py")
    print(f"Error: \n{e}")
    import logec
    logec.main()

def time():
    time = datetime.now()
    current_time = time.strftime("%H:%M:%S")
    return current_time

# getting user

def user():
    current_user = sp.getoutput("whoami")
    return current_user

# getting current dir
def current_dir():
    cwd = os.getcwd()
    return(cwd)


## scalable banner based on term size

def term_size():
    size_raw = os.get_terminal_size()
    #print(size_raw)
    #return size_raw
    size_raw_2 = re.search(r'columns=\d{1,3}', str(size_raw))[0]
    size = size_raw_2.strip("columns=")
    return(size)



# Doc: https://www.geeksforgeeks.org/how-to-get-file-size-in-python/

## Sidenote, do a ram check (https://stackoverflow.com/questions/11615591/available-and-used-system-memory-in-python) to see if enough ram is availbe for large queries, if not, give a warning and 
## then break if a bypass warning flag is not given
def size_check(filename):
    file_size = os.stat(filename)
    if 100000000 <= file_size.st_size <= 1000000000:
        return f"'{filename}' size over 100 MB, this may take a second..."
    if 1000000000 <= file_size.st_size <= 10000000000:
        return f"'{filename}' size over 1 GB, this will take a second & use ~1 GB of RAM"
    if 1000000000 <= file_size.st_size <= 20000000000:
        return f"'{filename}' size over 2 GB, this will take a second & use ~1-3 GB of RAM due to overhead"    
    if file_size.st_size > 10000000000: 
        return f"Why the fuck is your log {filename} 10+ GB? This is gonna take a minute or 5 and eat all of your RAM..."
    else:
        return "File size looks good, continuing..."


def file_count(file):
    num_lines = sum(1 for line in open(file))
    return num_lines



class performance:

    def memcheck(message):
        print("==========")
        print(message)
        print(f"Ram Usage: {psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2} MB")  
        print("==========")  
        
    def memsize(object, name):
        print("==========")
        print(f"DEBUG: Size of {name} is {sys.getsizeof(object)/1000000} MB")
        print("==========")


    
class stats:
    def num_unique(item):
        number = len(set(item))
        return(number)
    def num_count(item):
        number = len(item)
        return(number)