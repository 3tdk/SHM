# coding=utf-8
"""
SHM (SmartHubMonitor)

Collects connection stats from the web interface of a modem / hub, and publishes the captured data to a location.
By default the decide to capture data from is a BT Smart Hub 2. The system to publish data to is Mathworks ThingSpeak. The web browser is Chromium.

The terms "Hub" and "modem" are used fairly interchangeably in this script. Sorry.

To configure:
1: Update the details in "modemOptions" to match the details of your network and those provided with your Smart Hub 2
2: Update the details in "publisherOptions" to match those provided from thingspeak.com
3: If you are using Firefox, update the path to GeckoDriver

Developer notes:
The script is designed to be executed on a system running cron (e.g. to enable data capture every x minutes) therefore minimal error recovery / retries are implemented.

Additional modem / hubs can be defined in SHM_HubStatsCollector
Additional publish routes can be defined in SHM_HubStatsPublisher

"""


# Import Argparse to manage command line aguments
import argparse
# Import Importlib to allow dynamic configuration
import importlib
# Import Selenium library (note additional imports below depending on the specific driver chosen)
from selenium import webdriver

# Read the user command line arguments
parser=argparse.ArgumentParser(description="Read connection stats from web interface of BT Smart Hub 2 and post them to a ThingSpeak channel. Command line parameters are intended for developer / debug use only. The main configuration is performed withint he text of the script and cnanot be set on the command line\n")
parser.add_argument('--engine', choices=['chromium','firefox'], default='chromium', nargs='?', help='Select the selenium engine to use: chromium, or firefox (default: %(default)s)')
parser.add_argument('--printonly', action='store_true',help='Print only mode: Stop after capturing data, i.e. don\'t post to ThingSpeak (default: %(default)s)')
parser.add_argument('--config_file', action='store', default='SHM_config_default', help='Configuration options file (default= %(default)s)')
args = parser.parse_args()
print("SmartHubMonitor: Using Selenium engine \'"+args.engine+"\' and config file \'"+args.config_file+"\'\n")

#Import user configuration file
SHM_Config = importlib.import_module(args.config_file) 

#Set up Webdriver
if args.engine=='firefox':
    from selenium.webdriver.firefox.options import Options as FireFoxOptions
    firefox_options = FireFoxOptions()
    firefox_options.headless = True
    driver = webdriver.Firefox(options=firefox_options, executable_path=SHM_Config.geckodriverpath)

if args.engine=='chromium':
    from selenium.webdriver.chrome.options import Options as ChromiumOptions
    chrome_options = ChromiumOptions()  
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('disable-infobars')
    driver = webdriver.Chrome(options=chrome_options)

# Apply the user configuration to the modem and publisher (so any failures due to misconfiguration happen quickly)
modem = SHM_Config.modem(SHM_Config.modemOptions)
publisher = SHM_Config.publisher(SHM_Config.publisherOptions)

# Capture the data from the hub
DataRecord = modem.CaptureStats(driver)

print("Reported stats\n--------------\n"+\
    "Uptime : " + str(DataRecord.Uptime) +" hours\n"+\
    "Sync rate UP : " + str(DataRecord.DataRate_Upload) +" Mbps\n"+\
    "Sync rate DOWN : " + str(DataRecord.DataRate_Down) +" Mbps\n"+\
    "Max sync rate UP :" + str(DataRecord.MaxDataRate_Up) +" Mbps \n"+\
    "Max sync rate DOWN : " + str(DataRecord.MaxDataRate_Down) +" Mbps\n"+\
    "SNR UP : " + str(DataRecord.SNR_Up) +" dB\n"+\
    "SNR DOWN : " + str(DataRecord.SNR_Down)+" db")

# Publish data
if args.printonly == False:
    print("\nPosting data\n--------------")
    publisher.PublishData(DataRecord)
else:
    print("Printonly mode defined - did not post data")

