"""
Provides Publisher classes for HubStatsRecord classes

HubStatsPublisher: Abstract class defining clas interface
ThingSpeakMQTTPublisher: Publishes stats to a ThingSpeak MQTT channel

"""
from SHM_HubStatsCollector import HubStatsRecord
# Import paho library
import paho.mqtt.publish as publish

class HubStatsPublisher(object):
    """
    Abstract class defining an object which takes a HubStatsRecord class and publishes it to some service
    """

    def __init__(self, optionsDict: dict):
        """
        Abstract constructor
        
        :param optionsDict: A dictionary containing options for the publisher
        """
        raise NotImplementedError("")
        
    def PublishData(self,dr: HubStatsRecord):
        raise NotImplementedError("")

class ThingSpeakMQTTPublisher(HubStatsPublisher):
    """
    Concrete class implementing publication of HubStatsRecord to ThingSpeak MQTT
    """
    def __init__(self,optionsDict: dict):
        """
        Create a ThingSpeakPublisher class
        
        :param optionsDict: A Dictionary object containing the options for the publisher. 
            "tsMQTTHost": The ThingSpeak host URL (probably mqtt.thingspeak.com)
            "tsWriteAPIKey": The Users Write API Key
            "tsChannelID": The Channel ID
        """
        self.tsMQTTHost = optionsDict['tsMQTTHost']
        self.tsAPIKey = optionsDict['tsWriteAPIKey']
        self.tsChannel = optionsDict['tsChannelID']
        self.no_retries = 10
        
    def PublishData(self, dr:HubStatsRecord):
        """
        Publish data in a HubStatsRecord to the ThingSpeak channel
        :param dr: A HubStatsRecord object containing the data to be published
        """
        
        print("Publishing data to ThingSpeakMQTT")
        
        # build the payload string
        Payload = "field1=" + str(dr.Uptime) +\
        "&field2=" + str(dr.DataRate_Upload) +\
        "&field3=" + str(dr.DataRate_Down) +\
        "&field4=" + str(dr.MaxDataRate_Up) +\
        "&field5=" + str(dr.MaxDataRate_Down) +\
        "&field6=" + str(dr.SNR_Up) +\
        "&field7=" + str(dr.SNR_Down)

        print("MQTT Payload string: \""+Payload+"\"")
    
        #### ThingSpeak comms settings (basic configurationf or unsecired websockets)
        tTransport = "websockets"
        tPort = 80
        tTLS = None
        
        # Create the topic string
        topic = "channels/" + self.tsChannel + "/publish/" + self.tsAPIKey
        
        publishsuccess = False
        result = ""
        retrycount = 0
        while (retrycount < self.no_retries) and (publishsuccess ==False):
            # attempt to publish this data to the topic 
            try:
                result = publish.single(topic, payload=Payload, hostname=self.tsMQTTHost, port=tPort, tls=tTLS, transport=tTransport)
                publishsuccess = True
                pass
        
            except (KeyboardInterrupt):
                break
        
            except:
                print ("There was an error while publishing the data at try: "+str(retrycount))
                publishsuccess = False
                retrycount = retrycount+1
                
        print("Publish success was: "+str(publishsuccess) + " (result was \""+ str(result)+"\" after "+str(retrycount)+ " retries)")
                