"""
Copyright 2022 Netherlands eScience Center and University of Twente
Licensed under the Apache License, version 2.0. See LICENSE for details.

This file defines pipelines for standardised EMG analysis.
"""

from . import preprocessing as pp
from . import ecg_removal as ecg
from . import envelope as evl

def working_pipeline_exp(our_chosen_file):
    """This function is legacy.
    It produces a filtered respiratory EMG signal from a
    3 lead sEMG file. A better
    option is a corresponding function in multi_lead_type
    The inputs are :code:`our_chosen_file` which we
    give the function as a string of filename.  The output is the
    processed EMG signal filtered and seperated from ECG components.
    The algorithm to pick out the EMG here is by having
    more peaks.

    :param our_chosen_file: Poly5 file
    :type our_chosen_file: ~TMSiSDK.file_readers.Poly5Reader

    :returns: final_envelope_a
    :rtype: ~numpy.ndarray
    """
    cut_file_data = pp.bad_end_cutter(
        our_chosen_file,
        percent_to_cut=3,
        tolerance_percent=5,
    )
    bd_filtered_file_data = pp.emg_bandpass_butter_sample(
        cut_file_data,
        5,
        450,
        2048,
        output='sos',
    )
    # end-cutting again to get rid of filtering artifacts
    re_cut_file_data = pp.bad_end_cutter_for_samples(
        bd_filtered_file_data,
        percent_to_cut=3,
        tolerance_percent=5,
    )
    # do ICA
    components = ecg.compute_ICA_two_comp(re_cut_file_data)
    #  pick components with more peak
    emg = ecg.pick_more_peaks_array(components)
    # now process it in final steps
    abs_values = abs(emg)
    final_envelope_d = pp.emg_highpass_butter(abs_values, 150, 2048)
    final_envelope_a = evl.naive_rolling_rms(final_envelope_d, 300)

    return final_envelope_a

def working_pipeline_pre_ml(our_chosen_samples, picker='heart'):
    """
    This is a pipeline to pre-process
    an array of specific fixed dimensions
    i.e. a three lead array into an EMG singal,
    the function is legacy code, and most
    processsing should be done with
    :code:`multi_lead_type.working_pipeline_pre_ml_multi`
    or :code:`multi_lead_type.working_pipeline_pre_ml_multi`

    :param our_chosen_samples: the read EMG file arrays
    :type our_chosen_samples: ~numpy.ndarray
    :param picker: the picking strategy for independent components
    :type picker: str

    :returns: final_envelope_a
    :rtype: ~numpy.ndarray
    """
    cut_file_data = pp.bad_end_cutter_for_samples(
        our_chosen_samples,
        percent_to_cut=3,
        tolerance_percent=5
    )
    bd_filtered_file_data = pp.emg_bandpass_butter_sample(
        cut_file_data,
        5,
        450,
        2048,
        output='sos'
    )
    # step for end-cutting again to get rid of filtering artifacts
    re_cut_file_data = pp.bad_end_cutter_for_samples(
        bd_filtered_file_data,
        percent_to_cut=3,
        tolerance_percent=5
    )
    #  and do step for ICA
    components = ecg.compute_ICA_two_comp(re_cut_file_data)
    #     the picking step!
    if picker == 'peaks':
        emg = ecg.pick_more_peaks_array(components)
    elif picker == 'heart':
        emg = ecg.pick_lowest_correlation_array(components, re_cut_file_data[0])
    else:
        emg = ecg.pick_lowest_correlation_array(components, re_cut_file_data[0])
        print("Please choose an exising picker i.e. peaks or hearts ")
    # now process it in final steps
    abs_values = abs(emg)
    final_envelope_d = pp.emg_highpass_butter(abs_values, 150, 2048)

    return final_envelope_d
