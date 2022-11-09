import re
from netaddr import IPNetwork
from rich import print
from rich.progress import track
import os
import subprocess

import logec

## bad ip test: 205.151.128.1

BAD_DOMAINS_COMPILED = "Modules/tools/ip_rep/bad_domains_compiled.txt"


## == Filter/sort/crossrefrence functions
class profile:
    
    def __init__(self):
        self.self = self
    
    def lst():
        ## Initiating lists
            ## yo future ryan these names suck and are confusing, change them
        ## IP's to be checked
        profile.lst.input_ips = []
        ## List of malicious IP's
        profile.lst.bad_ip_list = []
        # bad IP's that have been checked against the bad ip list
        profile.lst.bad_ip_confirmed = []
        
    ## == input types
    def user_input(user_input):
        ## Change this to if not an IP (!= regex), look for file
        if "txt" in user_input:
            with open(user_input, "r") as user_file:
                profile.lst.input_ips = user_file.read()
        else:
            profile.lst.input_ips.append(user_input)

    # for module inputs
    def module_input(user_input):
        ## Change this to if not an IP (!= regex), look for file
        if "txt" in user_input:
            with open(user_input, "r") as user_file:
                profile.lst.input_ips = user_file.read()
        else:
            profile.lst.input_ips.append(user_input)           

    ## == bad domain checking
    def bad_dom_load():
        with open(BAD_DOMAINS_COMPILED, "r") as bad_dom:
            profile.lst.bad_ip_list = bad_dom.read()

    def bad_dom_check():
        for i in profile.lst.input_ips:
            if i in profile.lst.bad_ip_list:
                profile.lst.bad_ip_confirmed.append(i)
                print(f"Appended {i}")
            else:
                continue
            
        if profile.lst.bad_ip_confirmed != []:
            return set(profile.lst.bad_ip_confirmed)
        else:
            return "No Malicious IP's found"

 

## == a set of pre defined functions to run for different actions
class main_functions:
    def __init__(self):
        self.self = self
        
    ## A control to make sure that the full IP list is there when running this tool
    def full_ip_check():
        if os.path.exists(BAD_DOMAINS_COMPILED) is True:
            pass
        else:
            update() 
        
    def main_shell():
        ## == checks for if full IP list exists
        main_functions.full_ip_check()
        ## == resets lists
        profile.lst()
        ## == loads bad IP list
        profile.bad_dom_load()
        ## == Get's user input
        user_input = input("Enter IP, or file with IP's to check: ")
        ## Sees if input is a file or an IP
        profile.user_input(user_input)
        ## == returns cross refrence with malicious IP's
        return profile.bad_dom_check()

    def module_shell():
        main_functions.full_ip_check()
        
        profile.lst()
        profile.bad_dom_load()
        return profile.bad_dom_check()


## == Update 
def update():
    ## first, grab results of the website with the IP's and put them into the bad_dom list

    # Init list to be written
    bad_ip_full = []
    
    ## Deleting previous expanded IP file if present
    try:
        os.remove(BAD_DOMAINS_COMPILED)
    except:
        print("Malicious Domain list not present...")

    # == get the current bad domains 
    try:
        with open("Modules/tools/ip_rep/bad_domains.txt", "r") as bad_dom:
            ip_cidr = re.compile(r'(?:\d{1,3}\.){3}\d{1,3}(?:/\d\d?)?')
            try:
                cidr_bad_dom = ip_cidr.findall(bad_dom.read())

            except OSError as e:
                print(e)

        # == expand CIDR to full IP, somewhat slow
        for i in track(cidr_bad_dom, description="Expanding CIDR to full IP addresses..."):
            for ip in IPNetwork(i):
                bad_ip_full.append('%s' % ip)
        
        ## Checking if file exists, and creating if not
        if os.path.exists(BAD_DOMAINS_COMPILED) == True:
            pass
        else:
            print("Malicious Domain list does not exist, creating...")
            with open(BAD_DOMAINS_COMPILED, "w+") as f:
                pass
            ## reloading
            logec.shell_func.reload()
            
        # == write full bad IP's to file, 242 MB so maybe load in as a tuple?
        with open(BAD_DOMAINS_COMPILED, "a+") as bad_dom_compiled:
            for i in bad_ip_full:
                bad_dom_compiled.write(i + "\n")
        
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

#for testing
#print(function.module_shell())



