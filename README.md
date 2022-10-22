# Linkedin enriched posts metrics data

## Challengue
Currently, Linkedin doesn't provide good metrics about posts metrics, so anybody is able to know wich is the best time to post. So I wanted to do a better analysis of my Linkedin posts by developing a RPA python script based on using selenium python library in order to log into my account and scrap that info in a hourly basis. 

## Outcome
In this github repository you will find a python script wich will log into your account, so for that you need to amend you email and password with wich you log into linkedin and it will loop on a timeframe basis your linkedin posts metrics in order to get snapshots of that and store the data into a PostgreSql database. Take into accout that you will need to install different modules required for running the RPA python script so please find that info as following in the requirements sections.

## Requirements
1. Install the different python libraries used for running the RPA python script. You will find that at the beginning of the .py script (in the jyputer notebook provided as well).
2. Install the Selenium webdriver of you choise. You can find the link as following
https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
3. Create the tables needed in a linkedin PostgreSql database. Please find attached to this repository the Sql scripts for doing that. 
4. If your machine is Windows, you can download any task scheduler software of your choise or use by default windows task scheduler and set a job scheduler for running execpython.bat file every 5 min. The RPA script will run if there the last snapshot taken is later than 15 min, otherwise it will be executed after 5 min and so on. Once the RPA start running it will be running for quite a lot of time so it will get the data in same session avoiding to log everytime the RPA script run in order to block your Linkedin account (or needed to pass a security check next time you log in).

## Data you get
Once you have install all python libraries needed and created the tables in a PostgreSql database call linkedin you will get your linkedin posts metrics and content of your Linkedin posts in a timeframe basis of you choise (you can parametrize the timeframe in the RPA script, check that in the bottom of the script). 

<img src='images/snapshots posts content.png'></img>
<img src='images/snapshots post metrics.png'></img>

## Queries to use


## Next steps
1. Once you get the data you will be able to develop a Power Bi or a Tablaeu dashbaord. 
2. Do some text clustering in order to know wich kind of content resonate more with your connections and followers. 
