import pandas as pd
import asr_metrics as metrics # Custom levenshtein library
import os
import numpy as np
from csv import reader


DECODER_OUTPUT_DIR="../decoder/output/"

# For anonymisation we translate the subject names according to a predefined table:
with open('subjectnames.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    subject_names_ids = list(csv_reader)

def get_subject_id(subject_name):
    for name_with_id in subject_names_ids:
        if name_with_id[0] == subject_name:
            return name_with_id[1]
    print("ERROR: subject name {0} not found!".format(subject_name))

# First we read the test sentences and their grammatical reference paths into a DataFrame:
results_df = pd.read_csv("testset_and_gramref.csv")

# We add the Word Difference Rate for every utterance (compared to grammar reference) (which is the same as WER):
results_df['WDR (utterance vs reference)'] = results_df.apply(lambda row : metrics.wer(row['Grammar reference'], row['Test utterance']), axis = 1) 

# We add the word-level Levenshtein distance:
#results_df['Word-level Levenshtein distance'] = results_df.apply(lambda row : metrics.word_levenshtein(row['Test utterance'], row['Grammar reference']), axis = 1) 

# Let's also add the character-level Levenshtein distances by comparing the first two columns:
#results_df['Levenshtein distance'] = results_df.apply(lambda row : metrics.levenshtein(row['Test utterance'], row['Grammar reference']), axis = 1) 



# Now we are going to read all of the decoder output:
speakers=[]
test_utts=[]
decoded_sentences=[]
for f in os.listdir(DECODER_OUTPUT_DIR): 
     # check the files which start with the correct prefix:

    if f.startswith("recording_"):
        speaker=f.split('_')[1]
        test_utt=f.split('_')[2].replace("-"," ")
        filedata = open(DECODER_OUTPUT_DIR+f, 'r')
        decoded_sentence=filedata.readlines()[0].strip()
        speakers.append(speaker)
        test_utts.append(test_utt)
        decoded_sentences.append(decoded_sentence)

# Function to quickly retrieve a particular speaker's decoded version of a test utterance:
def get_decoded_output(speaker, test_utt):
    for i in range(len(speakers)):
        if(speakers[i]==speaker):
            if(test_utts[i]==test_utt):
                return decoded_sentences[i]
    print("ERROR: test utterance {0} for speaker {1} not found!".format(test_utt, speaker))

# # Custom function for coloring a particular DataFrame cell:
# def color_cell(indf,row_idx,col_idx):
#     color = 'background-color: yellow; color: black'
#     df_colored = pd.DataFrame('', index=indf.index, columns=indf.columns)
#     df_colored.iloc[row_idx, col_idx] = color
#     return df_colored

# Consolidate this data into the DataFrame:
for speaker in list(set(speakers)):
    speaker_id=get_subject_id(speaker)
    results_df[speaker_id+'-decoded']=results_df.apply(lambda row : get_decoded_output(speaker,row['Test utterance']), axis = 1)
    results_df['{0} WER'.format(speaker_id)] = results_df.apply(lambda row : metrics.wer(row['Grammar reference'], row['{0}-decoded'.format(speaker_id)]), axis = 1) 
    results_df['{0} CER'.format(speaker_id)] = results_df.apply(lambda row : metrics.wer(row['Grammar reference'], row['{0}-decoded'.format(speaker_id)]), axis = 1) 



# Finally, we export the results to a CSV:
results_df.to_csv(r'processed_results_nifti_asr.csv', index = False)