The files in this folder are used for analysing the decoder results.


The process_results_nifti_asr.py script will read the testutt_and_ref.txt file. This comma-separated file contains the spoken test utterances along with their grammatical reference (ie, the grammar path it should adhere to).
The process will output a new comma-separated file that adds several new columns.
The process will first calculate the Word Error Rate (WER) between the spoken utterance and the grammar reference, which is used as a difficulty metric for the decoder. Similarly, the levenshtein distances between the spoken utterances and grammar references are calculated. 
The subsequent columns contain the decodings for each of the test speakers (which are retrieved from the decoders output directory)

The process_results_kaldi_nl.py does a similar task for the decoding results of the Kaldi NL system. The raw decoder results are stored in results_kaldiNL.csv (may not be available due to privacy). In this case, a subset of the sentences is processed because kaldiNL is not theoretically able to detect all words correctly due to its models. Also, the subset of sentences that Kaldi NL's output is compared to has been slightly compensated for small differences such as split words (because it's unfair to penalize Kaldi NL for such model-differences).

Finally, nifti_vs_kaldiNL_performance.py compares the performane of the Nifti ASR and Kaldi NL for the subset of sentences that Kaldi NL can theoretically encode (as explained earlier).
