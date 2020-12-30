dedicon_home=$PWD
inputdir="$dedicon_home/decoder/input"
outputdir="$dedicon_home/decoder/output"
resultdir="$dedicon_home/decoder/results"
scratchdir="$dedicon_home/decoder/scratch"
#datadir="$scratchdir/data"
model_data_dir="$dedicon_home/model_data"

# Get Kaldi home directory from environment configuration.
# TODO: This is an ugly way to read these variables but I have not found a neat way that works for python and bash.
kaldi_dir=$(. $PWD/environment.py; echo $kaldi_dir)
nj=1
scoring=false #Does not fully work because of the block at the bottom (awk things)



#[ -f ./path.sh ] && . ./path.sh; # source the path.

s5_dir=$kaldi_dir/egs/wsj/s5

if [[ -d $resultdir/AM ]];then
  echo "$resultdir is not clean, please ensure clean result directory!"
  exit
fi
mkdir -p $resultdir/AM
cp -r $model_data_dir/input/AM $resultdir
echo "Adjusting Acoustic Model configuration paths in config files..."
sed -i "s|DECODER_RESULTS_DIR|$resultdir|g" $resultdir/AM/conf/online.conf # Overwrite path in config file
sed -i "s|DECODER_RESULTS_DIR|$resultdir|g" $resultdir/AM/conf/ivector_extractor.conf # Overwrite path in config file

if [[ -d $outputdir ]];then
  echo "$outputdir is not clean, please ensure clean output directory!"
  exit
fi
mkdir -p $outputdir

echo "Cleaning scratch directory prior to processing..."
rm $scratchdir -fr
mkdir $scratchdir
#mkdir $datadir

echo "Now decoding audio recordings."
for inputfile in $inputdir/*.wav; do
  file_id=$(basename "$inputfile" .wav)
  sox $inputfile -e signed-integer -r 16000 -b 16 $scratchdir/${file_id}_conv.wav # Audio conversion
  IFS="_" read -ra fields <<< $file_id
  spoken_text="${fields[2]}"
  text=${spoken_text//-/ }
  speaker="${fields[1]}"
  targetdir=$scratchdir/${file_id}_$(date +"%y_%m_%d_%H_%m_%S")
  datadir=$targetdir/data
  mkdir -p $datadir


  echo "$file_id $scratchdir/${file_id}_conv.wav" > $datadir/wav.scp
  echo "$file_id $speaker" > $datadir/utt2spk
  echo "$speaker $file_id" > $datadir/spk2utt
  echo "$file_id $text" > $datadir/text

  cd $kaldi_dir/egs/wsj/s5
  steps/make_mfcc.sh --nj $nj --mfcc-config $model_data_dir/input/AM/conf/mfcc.conf $datadir $targetdir/log $targetdir/mfcc
  steps/compute_cmvn_stats.sh $datadir $targetdir/log $targetdir/mfcc
  cd $s5_dir # Necessary because otherwise decode.sh does not know where score.sh is.
  if [ "$scoring" == true ]; then
  steps/online/nnet3/decode.sh --nj $nj --acwt 1.2 --post-decode-acwt 10.0 $model_data_dir/generated/HCLG/graph $datadir $resultdir/AM/decode_${file_id}
  grep 'WER' $resultdir/AM/decode_${file_id}/scoring_kaldi/best_wer >> $resultdir/recacc_per_utt
  cat $resultdir/AM/decode_${file_id}/scoring_kaldi/wer_details/per_utt >> $resultdir/detail_per_utt
  else
  steps/online/nnet3/decode.sh --nj $nj --acwt 1.2 --post-decode-acwt 10.0 --skip-scoring true $model_data_dir/generated/HCLG/graph $datadir $resultdir/AM/decode_${file_id}
  fi
  grep "^${file_id}" $resultdir/AM/decode_${file_id}/log/decode.1.log | cut -d' ' -f2- > $outputdir/${file_id}.txt
done

echo "Finished decoding audio."
# The following block doesn't quite work because of awk issues that I don't understand....
if [ "$scoring" == true ]; then
  echo "Now processing results."
  error=$(cut -d' ' -f 4 $resultdir/recacc_per_utt | awk '{ sum += $1 } END { print sum }')
  total=$(cut -d' ' -f 6 $resultdir/recacc_per_utt | sed 's/,//g' | awk '{ sum += $1 } END { print sum #}')
  ins=$(cut -d' ' -f 7 $resultdir/recacc_per_utt | awk '{ sum += $1 } END { print sum }')
  del=$(cut -d' ' -f 9 $resultdir/recacc_per_utt | awk '{ sum += $1 } END { print sum }')
  sub=$(cut -d' ' -f 11 $resultdir/recacc_per_utt | awk '{ sum += $1 } END { print sum }')
  wer=$(bc -l <<<"scale=2; $error / $total * 100")
  echo "%WER $wer [ $error / $total, $ins ins, $del del, $sub sub ] $dedicondir/offline_recognizer/#resources/AM/decode_*" > $resultdir/final_res
  echo "%WER $wer [ $error / $total, $ins ins, $del del, $sub sub ] $resultdir/AM/decode_*" > $resultdir/final_res
fi