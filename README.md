Guide to setting up the dedicon environment
===========================================

Pre-requisites
--------------
1. Run linux.
2. Make sure to compile kaldi on your system. Don't copy a precompiled version, it likely won't work. For instructions, go to the official Kaldi website.
3. Update the paths in environment.py. All scripts will rely on this information to run correctly.

Model layers
------------
### Description of layers ###
A Kaldi ASR is composed of several layers that make up a decoding graph from recorded audio to text:

- H: Hidden Markov Model that outputs context-dependent phones.
- C: Takes the input from H, outputs phones.
- L: Lexical layer: it takes phones as input and outputs words from a lexicon.
- G: Grammatical layer. It looks at the sequence of words generated by the L-layer and tries to estimate the closest grammatically correct sequence. Valid grammar is defined in a Finite State Graph (FSG). It is an acceptor: ideally the input and output should be the same, but if for example a word is recognized slightly incorrect by L, G will nudge it back to the correct form based on it's knowledge of acceptible grammar.

For more information about the layers, please refer to the official Kaldi documentation.

### Generating the layers ###
The H and C layer form the Acoustic Model (AM). The code provided here uses a pre-trained AM, it (currently) can't generate an AM on it's own. The L and G layers can be generated manually. Finally, all layers are composed into a HCLG fst file.

All files needed for layer generation are found in model_data/input. The pre-trained acoustic model is contained within the AM directory, files to generate the L and G layer are placed in their respective directories.

Before generating the L-layer, it is possible to change the lexicon in the L-directory. Generation is started by running generate_L.py. This will, amongst others, generate the L.fst file, which will ultimately be composed into the HCLG fst. One of the other files generated is words.txt. The L.fst file is binary and no longer includes the actual word-strings from the lexicon; they are now represented by numbers. If we want to translate the decoder output back to words at the end of all this, we need a word-number translation table. This is provided by words.txt. All generated data is saved in model_data/generated/

Once the L-fst has been generated, the grammar FST should be created. First, create a valid grammar FSG. You can do this manually or use a script that generates a FSG based on a train text. A basic FSG generator script is included. It looks at /model_data/input/G/train_text for the train text, and outputs to model_data/generated/G/fsg.txt. Just run generate_G_fsg.py or its larger number-including sibling.

Once the grammar FSG has been created, we can compile it into a binary G.fst by running generate_binary_G_fst.py. The binary file appears next to the fsg.txt in the G directory.

We can now finally compose the complete HCLG by running compose_HCLG.py. When this finishes without errors, the decoder is now ready to run.

Running the decoder
-------------------
First, make sure to place your (WAV) audio recordings in the decoder/input directory. They should be named according to this example:
> recording_jurriaan_hello-world_1.wav

The decoder script extracts information-fields from the filenames, hence they are important for proper decoding. The fields are separated by "_". The field "jurriaan" identifies the speaker. The field "hello-world" entails the spoken text. Note that words are separate by "-". The spoken text is provided for (optional, currently not fully functional) performance analysis, but you may input anything; it does not have to be the actual text just to decode. The final field "1" just has to be added for some reason ("I'll look into this, maybe later").

To run the decoder, run decode_audio.sh. When all goes well, the output text can be found in decoder/output. The results directory contains more information generated during the decoding, and the scratch directory contains files created and used by the decoder, such as mfcc feature data. 

Cleaning up your work environment
---------------------------------
Most scripts here perform some checks to make sure no previously generated data is overwritten. As a result, you have to make sure to clean previously generated data manually before generating new data. You can simply remove the files and directories in the generated-directory or the output, scratch and results directories for the decoder. If you want to quickly clean up everything, you can run clean_all_generated_data.sh. Make sure to backup your results and any other generated information before doing so!

Credits
-------
This project was created by Jurriaan ten Brinke. Parts of the code were previously written by Emre Yilmaz.
test