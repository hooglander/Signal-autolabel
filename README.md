# Signal-autolabel
A script to autolabel events start time and duration from raw analog signals. The raw dataset must be in 'csv' format, and the output will be in 'csv' format.

# Running Script
To bring up help run:
```
python autolable.py -h 
```
Two example raw data files in csv (and thus can be opened with any text editor) are provided: 'action_1_signal_raw.data' and 'action_2_signal_raw.data'. Each row represents the values gathered from 19 sources for that timestamp starting from t=0. The script works with any number of sources and takes the mean.