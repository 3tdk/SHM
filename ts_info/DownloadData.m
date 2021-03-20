% Template MATLAB code for visualizing data from a channel as a 2D line
% plot using PLOT function.

% Prior to running this MATLAB code template, assign the channel variables.
% Set 'readChannelID' to the channel ID of the channel to read from. 
% Also, assign the read field ID to 'fieldID1'. 

% TODO - Replace the [] with channel ID to read data from:
readChannelID = [];
% TODO - Replace the [] with the Field ID to read data from:
fieldID1 = 3; %DOWN data rate
fieldID2 = 5; %DOWN MaxDataRate
fieldID3 = 7; %DOWN SNR

% Channel Read API Key 
% If your channel is private, then enter the read API
% Key between the '' below: 
readAPIKey = '';

numDatapoints = 4000 %ThingSpeak max. is 8000, but 4,000 gives 2 weeks data and is manageable

%% Read Data %%

[speeddata, timestamps] = thingSpeakRead(readChannelID, 'Field', [fieldID1, fieldID2], 'NumPoints', numDatapoints, 'ReadKey', readAPIKey);
[SNRdata, timestamps] = thingSpeakRead(readChannelID, 'Field', [fieldID3], 'NumPoints', numDatapoints, 'ReadKey', readAPIKey);

%% Visualize Data %%

plot(timestamps, speeddata);
title("Sync and Max sync with SNR");
ylim([30,50]);
ylabel("Sync speed Mbps");
yyaxis right;
plot(timestamps, SNRdata);
ylim([3,9]);
yline(6,'--','color','#EDB120');
ylabel("SNR dB");
xlabel("Date and time");
legend({"Sync rate","Max sync rate","SNR"},"location","Northwest");