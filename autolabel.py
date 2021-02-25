import pandas as pd
import numpy as np
import argparse

def main(file_name):
    file_name = file_name
    signal_raw = pd.read_csv(file_name, header=0, parse_dates=[0], index_col=0, squeeze=True)
    signal_mean = signal_raw.copy()
    signal_mean['f0'] = signal_mean.mean(axis=1)
    signal_mean = signal_mean.loc[:, signal_mean.columns.intersection(['f0'])]

    signal_digital = convert_signal(signal_mean, 40, 4.5, 400)
    produce_labels(signal_digital, file_name)

def convert_signal(signal_mean, lag, threshold, y_threshold):
    x = signal_mean.index.values
    y = np.asarray(signal_mean["f0"]).astype(int)
    signals = np.zeros(len(y)).astype(int)
    filtered_y = np.array(y)
    avg_filter = [0]*len(y)
    std_filter = [0]*len(y)
    avg_filter[lag - 1] = np.mean(y[0:lag])
    std_filter[lag - 1] = np.std(y[0:lag])
    for i in range(lag, len(y)):
        if y[i] - avg_filter[i-1] > threshold * std_filter [i-1] and y[i] > y_threshold:
            signals[i] = 1
            filtered_y[i] = filtered_y[i-1]
            avg_filter[i] = np.mean(filtered_y[(i-lag+1):i+1])
            std_filter[i] = np.std(filtered_y[(i-lag+1):i+1])
        else:
            signals[i] = 0
            filtered_y[i] = y[i]
            avg_filter[i] = np.mean(filtered_y[(i-lag+1):i+1])
            std_filter[i] = np.std(filtered_y[(i-lag+1):i+1])
            
        if signals[i] == 1 and signals[i-2] == 1 and signals[i-1] == 0:
            signals[i-1] = 1
                
        if signals[i] == 1 and signals[i-3] == 1 and signals[i-1] == 0:
            signals[i-1] = 1
            signals[i-2] = 1
        
        if signals[i] == 1 and signals[i-4] == 1 and signals[i-1] == 0:
            signals[i-1] = 1
            signals[i-2] = 1
            signals[i-3] = 1
                    
        if signals[i] == 0 and signals[i-1] == 1 and signals[i-2] == 0:
            signals[i-1] = 0

    return dict(timestamps = x,
                signals = np.asarray(signals),
                #avg_filter = np.asarray(avg_filter),
                #std_filter = np.asarray(std_filter)
               )

def produce_labels(signal_digital, file_name):
    timestamps = signal_digital["timestamps"]
    signal_values = signal_digital["signals"]
    label = file_name.split('_')[0]+'_'+file_name.split('_')[1]
    action_toggle = False
    start_time = 0
    end_time = 0
    output = []
    
    for i in range(1, len(timestamps)):
        if signal_values[i] == 1:
            if action_toggle == False:
                start_time = timestamps[i]
            action_toggle = True
            
        if signal_values[i] == 0 and action_toggle == True:
            end_time = timestamps[i-1]
            output.append([start_time,end_time - start_time,label])
            action_toggle = False
            
        pd.DataFrame(output, columns=['Time(Seconds)','Length(Seconds)','Label(string)']).to_csv(label+"_labels_output.label", index= False)

parser=argparse.ArgumentParser()
required = parser.add_argument_group('required arguments')
required.add_argument('-f', '--filename', type=str, metavar='', help='raw data file name', required=True)
args=parser.parse_args()

if __name__=='__main__':
    main(args.filename)