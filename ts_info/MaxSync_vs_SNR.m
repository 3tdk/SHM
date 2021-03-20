% Template MATLAB code for visualizing correlated data using the
% SCATTER function.

% Prior to running this MATLAB code template, assign the channel variables.
% Set 'readChannelID' to the channel ID of the channel to read from. 
% Also, assign the read field IDs to the variables 'fieldID1', and 'fieldID2'. 

% TODO - Replace the [] with channel ID to read data from:
readChannelID = [];
% TODO - Replace the [] with the Field ID to read data from:
fieldID1 = 7;
% TODO - Replace the [] with the Field ID to read data from:
fieldID2 = 5;

% Channel Read API Key 
% If your channel is private, then enter the read API
% Key between the '' below: 
readAPIKey = '';

numDatapoints = 4000;%ThingSpeak max. is 8000, but 4,000 gives 2 weeks data and is manageable


%% Read Data %%

% Read first data variable
data1 = thingSpeakRead(readChannelID, 'Field', fieldID1, 'NumPoints', numDatapoints, 'ReadKey', readAPIKey);

% Read second data variable
data2 = thingSpeakRead(readChannelID, 'Field', fieldID2, 'NumPoints', numDatapoints, 'ReadKey', readAPIKey);

%% Visualize Data %%
for i=1:length(data1)
    data_age(i)=(length(data1)-i)/length(data1);
end;

pointsize=15;

s = scatter(data1, data2, pointsize,data_age,"filled");
colormap summer
%s.AlphaData = data_age;
%s.MarkerFaceAlpha = 'flat';