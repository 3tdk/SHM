# coding=utf-8
"""
Provides data capture instructions for different modems / routers / OEM hubs based on screen scraping using Selenium.

HubStatsRecord - Provides a structure to report data captured from a HubStatsCollector
HubStatsCollector - a virtual class acting as a template for specific hubs
BTSmartHub2 - Concrete implementation of HubStatsCollector which overrides the CaptureStats function to collect data
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import re

class HubStatsRecord:
    """
    Structure to report data captured from a HubStatsCollector.
    """
    
    def __init__(self):
        self.Uptime=0
        self.DataRate_Upload=0
        self.DataRate_Down=0
        self.MaxDataRate_Up=0
        self.MaxDataRate_Down=0
        self.SNR_Up=0
        self.SNR_Down=0

class HubStatsCollector:
    """
    Virtual class for generic hub. Concrete implementations provide CaptureStats method.

    """
    
    def __init__(self, optionsDict: dict):
        """
        VIRTUAL. Capture stats from a hub and return a HubStatsRecord.
        
        :param optionsDict: A dictionary containing the options required by the specific implementation
        """
        raise NotImplementedError("")
          
    def CaptureStats(self, driver: webdriver) -> HubStatsRecord:
        """
        VIRTUAL. Capture stats from a hub and return a HubStatsRecord.
        :param driver: A configured Selenium webdriver object
        """
        raise NotImplementedError("")
        
class BTSmartHub2(HubStatsCollector):
    """
    Implements the CaptureStats method for capturing data from a BT Smart Hub 2.

    """

    def __init__(self, optionsDict: dict):
        """
        Create a BTSmartHub2 HubStatsCollector
        :param optionsDict: A dictionary which must contain the following entries:
        sh2URI : the URI of the Smart Hub
        sh2AdminPassword : the admin password
        """
        self.URI = optionsDict['sh2URI']
        self.AdminPassword = optionsDict['sh2AdminPassword']

    def CaptureStats(self, driver: webdriver)->HubStatsRecord:
        """
        Capture stats from a BT Smart Hub 2 and return a populated HubStatsRecord
        :param driver: A configured Selenium webdriver object
        """
        print("Capturing modem stats from BT Smart Hub 2 at "+ self.URI+"\n")
        # Capture the data from the Smart Hub
        # Start the web session
        driver.get(self.URI)
        # Select "Advanced Settings" screen
        WebDriverWait(driver,30).until(expected_conditions.element_to_be_clickable((By.ID,'gotoA'))).click()
        # Select "Helpdesk"
        WebDriverWait(driver,30).until(expected_conditions.element_to_be_clickable((By.ID,'advHelpdesk'))).click()
        #Put the password int he dialog"
        WebDriverWait(driver,30).until(expected_conditions.visibility_of_element_located((By.ID,'login_password_input_noshow'))).send_keys(self.AdminPassword)
        #Click the "OK" buttin
        WebDriverWait(driver,30).until(expected_conditions.element_to_be_clickable((By.ID,'ok_button'))).click()
        #Grab the infobox
        DataTableWebElement = WebDriverWait(driver,10).until(expected_conditions.element_to_be_clickable((By.ID,'Infobox')))
        
        # Process uptime
        UptimeStrings = re.findall(r"[-+]?\d*\.\d+|\d+",DataTableWebElement.find_element_by_id('DSLuptime').text) 
        Uptime = int(UptimeStrings[0])*24 + int(UptimeStrings[1])*1 + int(UptimeStrings[2])/60 + int(UptimeStrings[3])/3600
        
        # Process Data rate
        DatarateStrings = re.findall(r"[-+]?\d*\.\d+|\d+",DataTableWebElement.find_element_by_id('Datarate').text) 
        DatarateValues = [float(i) for i in DatarateStrings]
        
        # Process Max data rate
        MDatarateStrings = re.findall(r"[-+]?\d*\.\d+|\d+",DataTableWebElement.find_element_by_id('MDatarate').text) 
        MDatarateValues = [float(i) for i in MDatarateStrings]
        
        # Process noise margin
        NoiseMarginStrings = re.findall(r"[-+]?\d*\.\d+|\d+",DataTableWebElement.find_element_by_id('noise_margin').text) 
        NoiseMarginValues = [float(i) for i in NoiseMarginStrings]
        
        # Close Web browser
        driver.quit()

        # Populate the return data structure
        d = HubStatsRecord()
        d.Uptime = Uptime
        d.DataRate_Upload = DatarateValues[0]
        d.DataRate_Down = DatarateValues[1]
        d.MaxDataRate_Up = MDatarateValues[0]
        d.MaxDataRate_Down = MDatarateValues[1]
        d.SNR_Up = NoiseMarginValues[0]
        d.SNR_Down = NoiseMarginValues[1]
        
        return d