from pydub import AudioSegment
from pydub.silence import split_on_silence
import os 
import sys

'''
This script can be used to automatically split a recording into sentences, provided that there is some silence in between sentences. By specifying a text file containing the sentences, the split recordings can be automatically labeled. This script assumes that the audio recordings have been amplified so that the peaks are at 0dB (maximum without distortion). It may not be able to properly split when used with low-volume recordings. Audio splitting parameters may be changed if need be.

@author Jurriaan ten Brinke
'''


RECORDINGS_DIR="recordings"
SENTENCES_FILE="sentences.txt"

def resample(infile, outfile):
    compose_cmd='sox {0} -e signed-integer -r 16000 -b 16 {1}'.format(infile, outfile)
    os.system(compose_cmd)

def processFile(f):
    print("Now processing file: ",f)
    simple_name = os.path.splitext(os.path.basename(f))[0]
    os.mkdir(RECORDINGS_DIR+"/"+simple_name)
    outputdir=RECORDINGS_DIR+"/"+simple_name+"/"
    resampled_fname = outputdir+simple_name+"_resampled.wav"
    resample(RECORDINGS_DIR+"/"+f,resampled_fname)
    inputdata = AudioSegment.from_wav(resampled_fname) # Load audio.
    audio_chunks = split_audio(inputdata)
    chunk_names=getChunkNames(SENTENCES_FILE, simple_name)
    export_chunks(audio_chunks,outputdir,chunk_names)
    os.remove(resampled_fname) # Clean up resampled file.

def getChunkNames(textfile, chunk_base_name):
    '''
    Generate chunk output names based on input text file
    '''
    filedata = open(textfile, 'r')
    inlines = filedata.readlines()
    outlines = []
    for line in inlines:
        outlines.append("recording_"+chunk_base_name+"_"+line.replace(" ", "-")+"_1")
    return outlines
    
def split_audio(inputdata):
    # Split audio data where the silence is 500 milliseconds or more and get chunks using the imported function.
    print("Now splitting audio, please wait...")
    chunks = split_on_silence (
        # Use the loaded audio.
        inputdata, 
        # Specify that a silent chunk must be at least 0.5 seconds or 500 ms long.
        min_silence_len = 800,
        # Consider a chunk silent if it's quieter than -16 dBFS.
        # (You may want to adjust this parameter.)
        silence_thresh = -39,
        # How much of the silence to keep at begin and ending (so this amount is doubled in total). Set to prevent cutting into the audio too soon, ms.
        keep_silence=400
    )
    print("Found {} chunks.".format(len(chunks)))
    return chunks

def export_chunks(chunks, outputdir, chunk_names):
    if(len(chunks) != len(chunk_names)):
        print("FAIL: number of detected chunks does not match number of chunk names. ({} vs {}). Maybe change the audio split parameters?".format(len(chunks), len(chunk_names)))
        sys.exit() #Disable this line if you still want to export these files.
    # Export split chunks
    for i, chunk in enumerate(chunks):
        # Export the audio chunk.
        chunk.export(
            outputdir+chunk_names[i]+".wav".format(i),
            format = "wav"
        ) 

for f in os.listdir(RECORDINGS_DIR): 
     # check the files which are end with specific extention 
    if f.endswith(".wav"): 
        processFile(f) 
