# This script will calculate the number of correctly decoded sentences, WER and Levenshtein scores for the subset of grammatically perfect sentences that can contain no vocabulary unknown to kaldiNL.
# The file subset_sentences_compensated contains a column with this subset, in addition to a second column which is modified slightly to accomodate for slight differences due to kaldiNL's decoding.
# KaldiNL will be tested against this compensated column for fairness, since any decoding errors in this regard are not a reflection of the systems performance.

import pandas as pd
from csv import reader
import asr_metrics as metrics
import numpy as np

results_df = pd.read_csv("subset_sentences_compensated.csv")

# Import the relevant results from nifti asr:
nifti_results=pd.read_csv("processed_results_nifti_asr.csv")

# Import the relevant results from kaldi NL:
kaldi_NL_results = pd.read_csv("processed_results_kaldiNL.csv")
# This step is necessary because of empty recognition cases:
kaldi_NL_results = kaldi_NL_results.replace(np.nan, '', regex=True)

# Get speaker IDs:
subject_ids=[]
with open('subjectnames.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    subject_names_ids = list(csv_reader)
    for sublist in subject_names_ids:
        subject_ids.append(sublist[1])

def get_decode_from_nifti(subject, utterance):
    for index, row in nifti_results.iterrows():
        if row['Test utterance'] == utterance:
            return row['{}-decoded'.format(subject)]
    print("ERROR: utterance {0} for speaker {1} not found in Kaldi NL results!".format(utterance, subject))

def get_decode_from_kaldi_NL(subject, utterance):
    for index, row in kaldi_NL_results.iterrows():
        if row['Test utterance'] == utterance:
            return row['{}-decoded'.format(subject)]
    print("ERROR: utterance {0} for speaker {1} not found in nifti results!".format(utterance, subject))


for subject_id in subject_ids:
    print(subject_id)
    #results_df['{0} Nifti ASR'.format(subject_id)] = results_df.apply(lambda row : metrics.wer(row['Test utterance'], row['Grammar reference']), axis = 1) 
    
    # For every speaker, add the nifti asr decoding results:
    results_df['{0} Nifti decode'.format(subject_id)] = results_df.apply(lambda row : get_decode_from_nifti(subject_id, row['Original test utterance']), axis = 1) 
    # Also include WER, Levenshtein:
    results_df['{0} Nifti WER'.format(subject_id)] = results_df.apply(lambda row : metrics.wer(row['Original test utterance'], row['{0} Nifti decode'.format(subject_id)]), axis = 1) 
    #results_df['{0} Nifti Levenshtein'.format(subject_id)] = results_df.apply(lambda row : metrics.levenshtein(row['Original test utterance'], row['{0} Nifti decode'.format(subject_id)]), axis = 1) 

    # Repeat the above steps for the Kaldi NL results:
    results_df['{0} Kaldi NL decode'.format(subject_id)] = results_df.apply(lambda row : get_decode_from_kaldi_NL(subject_id, row['Original test utterance']), axis = 1) 
    # Note: in the case of Kaldi NL we compare the decode output to the compensated reference for fairness (due to vocabulary differences with Kaldi NL)
    results_df['{0} Kaldi NL WER'.format(subject_id)] = results_df.apply(lambda row : metrics.wer(row['Compensated for Kaldi NL'], row['{0} Kaldi NL decode'.format(subject_id)]), axis = 1) 
    #results_df['{0} Kaldi NL Levenshtein'.format(subject_id)] = results_df.apply(lambda row : metrics.levenshtein(row['Compensated for kaldi NL'], row['{0} Kaldi NL decode'.format(subject_id)]), axis = 1) 

# Finally, we export the results to a CSV:
results_df.to_csv(r'processed_results_nifti_vs_kaldi_NL.csv', index = False)