Getting started:
To get up and running, first run 'pip install -r requirements.txt' to install needed packages
Then, run 'event_generate.sh' to generate some data to look at!

Logec! 

Have you ever needed to really dig through some log files, but find yourself frustrated with AWK, GREP, and/or other tools? Well here is your solution!
Logec is a localized SIEM, meant to help you get to the bottom of any troubles you have quickly. No forwarders, agents, or server isntances, just download and go!

Some important definitions:

Module: A grouping of 2 programs (sorter, and shell) related to a single log (confusing I know)
  Shell: The shell is the frontend for the sorter, its main functions are to interact with the sorter via commands, and display results. 
  Sorter: The sorter is where all the heavy lifting happens, it searches, and sorts its respective log file for values via regex. Fromt here, it adds
          this data to a dataframe, and returns it to the shell to display

Here is a handy chart showing a map of this, with explanations as well:
![image](https://user-images.githubusercontent.com/91687869/200751535-36431c39-8345-40b4-b094-774eaa396648.png)


Here is the main page, where you can access different modules 
![image](https://user-images.githubusercontent.com/91687869/200749965-538642b5-0a8f-41c9-a897-a0923b80be8a.png)
