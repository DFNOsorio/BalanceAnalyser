from datetime import datetime

from processing_code.NOVAOpenSignals import *


def load_open_trial(name_of_file):
    time, date, sampling_rate, labels, data_points, columns = file_scrapper(name_of_file+'.txt')
    date_time = date + "T" + time + "Z"
    utc_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds() - 3600  # TimeZone

    open_time = time_vector_creator(float(sampling_rate), 0, len(data_points))
    EMG, ACC, ECG, EMG_labels, ACC_labels, ECG_labels = data_characterize_all(data_points, labels, columns)

    return EMG, ACC, ECG, EMG_labels, ACC_labels, ECG_labels, open_time, epoch_time


def load_emg_rest(name_of_file):
    time, date, sampling_rate, labels, data_points, columns = file_scrapper(name_of_file+'.txt')
    EMG, EMG_labels, EMG_means = data_characterize_rest(data_points, labels, columns)

    return EMG, EMG_labels, EMG_means
