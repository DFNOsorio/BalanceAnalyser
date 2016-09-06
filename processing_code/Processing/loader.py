from processing_code.SyncingCode import *
from processing_code.Processing import *
from processing_code.NOVAOpenSignals import *
from processing_code.NOVAWiiBoard import *
from flask import Flask
from flask import jsonify

global ls1
global ls2
global ls3
global ls4

global l_filter_frequency
global l_emg_smoother_window

def process_patient(folder_name, patient, multiple=False, pre_filter = False, filtering=True,
                    filter_frequency=(30, 400), pdf=True, norm=False, emg_smoother_window=500):

    if multiple:

        output = sync_files_multiple(folder_name, patient, ["_1", "_4"], [[0, 1, 2], [3]], number_of_files=2,
                                     plot=False,
                                     high=True)

        [s1, s2, s3] = segmented_signal(output, input_index=0, number_of_segments=3)

        [s4] = segmented_signal(output, input_index=1, number_of_segments=1)

    else:
        output = sync_files(folder_name, patient, plot=False, high=True)

        [s1, s2, s3, s4] = segmented_signal([output])

    if pre_filter:
        total = 8+5
        total = '"total": '+str(total)
    else:
        total = 8
        total = '"total": '+str(total)
    ## Processing

    yield "data: " + '{"data" : "Removing duplicates", "counter": 1, ' + total +' }' + "\n\n"

    [s1, s2, s3, s4] = remove_duplicates_batch([s1, s2, s3, s4])

    yield "data:" + '{"data" : "Adding COPs", "counter": 2, ' + total +' }' + "\n\n"

    [s1, s2, s3, s4] = add_COPs([s1, s2, s3, s4], interval_COPs([s1, s2, s3, s4]))

    yield "data:" + '{"data" : "Zeroing out data", "counter": 3, ' + total +' }' + "\n\n"

    EMG_zero, EMG_l_zero, EMG_means_zero = load_emg_rest(folder_name+patient+'/Base')

    [s1, s2, s3, s4] = zero_out_EMG([s1, s2, s3, s4], EMG_means_zero)
    counter  = 3
    if pre_filter:

        yield "data:" + '{"data" : "Spectrogram of each emg, for each interval", "counter": 4, ' + total +' }' + "\n\n"

        [s1, s2, s3, s4] = add_spec([s1, s2, s3, s4])

        yield "data:" + '{"data" : "Psd, for each interval", "counter": 5, ' + total +' }' + "\n\n"

        [s1, s2, s3, s4] = add_psd([s1, s2, s3, s4])

        yield "data:" + '{"data" : "Psd and spec integral, for each interval", "counter": 6, ' + total +' }' + "\n\n"

        [s1, s2, s3, s4] = integrate_spec_psd([s1, s2, s3, s4])

        yield "data:" + '{"data" : "RMS, for each interval", "counter": 7, ' + total +' }' + "\n\n"

        [s1, s2, s3, s4] = add_EMG_RMS([s1, s2, s3, s4], window_size=1000)
        yield "data:" + '{"data" : "Smoothing", "counter": 8, ' + total +' }' + "\n\n"
        [s1, s2, s3, s4] = smooth_intervals([s1, s2, s3, s4], window=emg_smoother_window)

        counter = 8

    if filtering:

        yield "data:" + '{"data" : "Filtering signal", "counter": '+str(counter + 1)+', ' + total +' }' + "\n\n"

        [s1, s2, s3, s4] = add_filtered_signal([s1, s2, s3, s4], frequencies=filter_frequency, order=4)

        yield "data:" + '{"data" : "Making spectrograms", "counter": '+str(counter + 2)+', ' + total +' }' + "\n\n"

        [s1, s2, s3, s4] = add_spec([s1, s2, s3, s4], data_var="open_signals_data_filtered", new_var="spec_data_filtered")

        yield "data:" + '{"data" : "Calculating the PSD", "counter": '+str(counter + 3)+', ' + total +' }' + "\n\n"

        [s1, s2, s3, s4] = add_psd([s1, s2, s3, s4], data_var="open_signals_data_filtered", new_var="psd_data_filtered")

        yield "data:" + '{"data" : "Integrating the spectrogram and the PSD", "counter": '+str(counter + 4)+', ' + total +' }' + "\n\n"

        [s1, s2, s3, s4] = integrate_spec_psd([s1, s2, s3, s4], data_var_psd="psd_data_filtered",
                                              data_var_spec="spec_data_filtered", new_var="spec_psd_integrated_filtered")

        yield "data:" + '{"data" : "Smoothing the EMG (window size = ' + str(emg_smoother_window) +')", "counter": '+str(counter + 5)+', ' + total +' }' + "\n\n"
        [s1, s2, s3, s4] = smooth_intervals([s1, s2, s3, s4], data_var="open_signals_data_filtered",
                                            new_var="smoothed_data_filtered", window=emg_smoother_window)
    yield "data:" + "End" + "\n\n"

    set_val([s1, s2, s3, s4], filter_frequency, emg_smoother_window)

    yield "data:" + "Close" + "\n\n"

# TODO
#
#

def set_val(data, filter_frequency, emg_smoother_window):

    global ls1
    global ls2
    global ls3
    global ls4

    global l_emg_smoother_window
    global l_filter_frequency

    [ls1, ls2, ls3, ls4] = data
    l_emg_smoother_window = emg_smoother_window
    l_filter_frequency = filter_frequency

def get_val():
    global ls1
    global ls2
    global ls3
    global ls4

    global l_emg_smoother_window
    global l_filter_frequency

    return [ls1, ls2, ls3, ls4], l_filter_frequency, l_emg_smoother_window


