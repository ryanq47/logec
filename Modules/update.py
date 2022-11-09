## a global updater, need to include update function to each module/tool to update it's respective compnents if possible
## A good update will return true, a bad one, false

import imports
import logec


##== Tool Imports:
import ip_rep

## == Tool Updates:
def main():
    ## == ip_rep updaate
    ip_rep_result = ip_rep.update()
    print("ip_rep Success") if ip_rep_result == True else print("ip_rep Failed")


logec.shell_func.reload()
#exit()
