import pandas as pd
import os
import numpy as np
from csv import reader

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

# Now we read the results from the Kaldi NL decoder:
with open('results_kaldiNL.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    decoder_output = list(csv_reader)

with open('subset_sentences.txt', 'r') as read_obj:
    csv_reader = reader(read_obj)
    subset_sentences = [item for subl in list(csv_reader) for item in subl]

# Now we are going to read all of the decoder output:
speakers=[]
test_utts=[]
decoded_sentences=[]

# for i in range(len(results_df)):
#      f = results_df.loc[i,]
#      print("Total income in "+ df.loc[i,"Date"]+ " is:"+str(df.loc[i,"Income_1"]+df.loc[i,"Income_2"]))

for sublist in decoder_output: 
    f = sublist[0]
     # check the files which start with the correct prefix:
    if f.startswith("recording_"):
        speaker=f.split('_')[1]
        test_utt=f.split('_')[2].replace("-"," ")
        #decoded_sentence=filedata.readlines()[0].strip()
        decoded_sentence=sublist[1]
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

# # # Custom function for coloring a particular DataFrame cell:
# # def color_cell(indf,row_idx,col_idx):
# #     color = 'background-color: yellow; color: black'
# #     df_colored = pd.DataFrame('', index=indf.index, columns=indf.columns)
# #     df_colored.iloc[row_idx, col_idx] = color
# #     return df_colored

# Consolidate this data into the DataFrame:
for speaker in list(set(speakers)):
    speaker_id=get_subject_id(speaker)
    results_df[speaker_id+'-decoded']=results_df.apply(lambda row : get_decoded_output(speaker,row['Test utterance']), axis = 1)

# Now we just filter out the rows that are not in the sentence subset:
results_df = results_df[results_df['Test utterance'].isin(subset_sentences)]
# Finally, we export the results to a CSV:
results_df.to_csv(r'processed_results_kaldiNL.csv', index = False) 
