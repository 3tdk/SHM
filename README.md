# SHM
SHM (SmartHubMonitor)

	usage: SHM.py [-h] [--engine [{chromium,firefox}]] [--printonly]
	              [--config_file CONFIG_FILE]
	
	Read connection stats from web interface of BT Smart Hub 2 and post them to a
	ThingSpeak channel. Command line parameters are intended for developer / debug
	use only. The main configuration is performed withint he text of the script
	and cnanot be set on the command line
	
	optional arguments:
	
	  -h, --help            show this help message and exit
	
	  --engine [{chromium,firefox}]
	                        Select the selenium engine to use: chromium, or
	                        firefox (default: chromium)
	
	  --printonly           Print only mode: Stop after capturing data, i.e. don't
	                        post to ThingSpeak (default: False)
	
	  --config_file CONFIG_FILE
	                        Configuration options file (default:
	                        SHM_config_default)

## User notes
The script is designed to be executed on a system running cron (e.g. to enable data capture every x minutes) therefore minimal error recovery / retries are implemented.

Collects connection stats from the web interface of a modem / hub, and publishes the captured data to a location.
By default the decide to capture data from is a BT Smart Hub 2. The system to publish data to is Mathworks ThingSpeak. The web browser is Chromium.

The terms "Hub" and "modem" are used fairly interchangeably in this script. Sorry.

## Configuration
To configure:
1. Edit the parameters *modemOptions* and *publisherOptions* in SHM_config_default.py (you can also create a new file and pass the name in at the command line e.g. --config_file SGM_config_mysetup)
2. Set geckodriverpath if required (as a firefox user)

## Execution
1. Run the script using the command-line parameters above. Note that the name defined in --config_file does not require the '.py' extension

## Installation
This script is designed for installation on Raspberry PI. These instructions assume you already have a functional X desktop (the browser won't install without it even though the script itself is command-line only).
* An X install with a browser. Chromium is easiest.

		sudo apt-get install chromium-browser

* A Selenium driver for the browser

		sudo apt-get install chromium-chromedriver

* Python3

		sudo apt-get install python3

* Selenium (an automatic test environment for web browsers <https://pypi.org/project/selenium/>)

		sudo pip3 install selenium

* Paho (an MQTT library required for posting your stats using MQTT <https://pypi.org/project/paho-mqtt/>)

		sudo pip3 install paho-mqtt

* Copy all the release files into a folder
* Configure the settings for your hub as per "Configuration"
* The script is designed to be executed using crontab

		crontab -e

* To monitor every 5 minutes, add the following line, editing <where...is> and <config_filename> as needed:

			*/5 * * * * python3 <where...is>/SHM.py --config_file <config_filename> &

## Thingspeak configuration
The script posts data to ThingSpeak using MQTT, but ThingSpeak needs to know what to do with it. Once you have set up your free account, and found the API keys, suitable channel settings are:
|Field|Label|
|---|---|
|Field1|DSL Uptime|
|Field2|UP Data Rate|
|Field3|DOWN Data Rate|
|Field4|UP MaxDataRate|
|Field5|DOWN MaxDataRate|
|Field6|UP SNR|
|Field7|DOWN SNR|

Matlab scripts for the visualisations are included in the ts_info folder.

## Developer notes
* Additional modem / hubs / data to collect can be defined in SHM_HubStatsCollector
* Additional publish routes can be defined in SHM_HubStatsPublisher
