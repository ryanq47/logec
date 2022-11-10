## The imports file

import sys
## importing Modules
sys.path.append('Modules/')
## tools
sys.path.append('Modules/tools/')
sys.path.append('Modules/tools/ip_rep')
sys.path.append('Modules/tools/integrity')
##Per Log Modules
sys.path.append('Modules/webserver/')
sys.path.append('Modules/syslogs/auth/')
sys.path.append('Modules/syslogs/dpkg/')

## Importing config dir
sys.path.append('config/')