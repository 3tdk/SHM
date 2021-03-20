# coding=utf-8
# Import library of hubstats collectors
import SHM_HubStatsCollector
import SHM_HubStatsPublisher

# -----USER CONFIG-------

###### Modem Settings
# Choose a modem type from one defined in SHM_HubStatsCollector
# e.g. modemType=SHM_HubStatsCollector.BTSmartHub2
modem=SHM_HubStatsCollector.BTSmartHub2
# Set modem options using a Dictionary object
#   sh2URI:  Modem IP address on your network
#   sh2AdminPassword: Modem  administrator password
#e.g. modemOptions={'sh2URI':'http://192.168.1.254/',
#                   'sh2AdminPassword':'1111xxxx'}
modemOptions={'sh2URI':'',
              'sh2AdminPassword':''}

###### Publisher Settings
# Choose a publisher from one defined in SHM_HubStatsPublisher
#e.g. publisher = SHM_HubStatsPublisher.ThingSpeakMQTTPublisher          
publisher = SHM_HubStatsPublisher.ThingSpeakMQTTPublisher

# Set publisher options using a Dictionary object
#   tsMQTTHost: The ThingSpeak host URL (probably mqtt.thingspeak.com)
#   tsChannelID: The Channel ID
#   tsWriteAPIKey: The Users Write API Key
#e.g. publisherOptions={'tsMQTTHost':'mqtt.thingspeak.com',
#                  'tsChannelID':'12222111',
#                  'tsWriteAPIKey':'AAAABBBBCCCCDDDD'}
publisherOptions={'tsMQTTHost':'mqtt.thingspeak.com',
                  'tsChannelID':'',
                  'tsWriteAPIKey':''}

#Set Geckodriver path (only required if using Firefox with GeckoDriver and it can't be found automatically e.g. geckodriverpath=r'C:\users\user1\Documents\python\bin\geckodriver.exe'
geckodriverpath=r''

# ------- END OF USER CONFIG -------