import json

x = {
    'TestNum': '1045',
    'numDevices': [1, 0, 0],
    'chNames': ['LED Tc', 'DRV', 'HS Top', 'Ple Amb', 'Lab Amb', 'N/A', 'N/A', 'N/A'],
    'chLimits': [85, 80, 150, 150 , 150, 150, 150, 150],
    'timeInterval': 30,
    'runDuration': 600
}

with open('test.json', 'w') as outfile:
    json.dump(x, outfile)