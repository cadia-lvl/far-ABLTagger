#!/bin/bash

# ex. usage: scripts/split_and_process_other.sh corpora/tagged_corpus_sosialurin/fo.revised.txt sosialurin_revised
# corpora/MIM-GOLD.20.05/13_categories/fbl.txt
if [[ $# -eq 0 ]] ; then
    echo 'Usage: '$0' path/to/corpus.txt version_name'
    exit 0
fi

IN_FILE=$1
VERSION=$2
PROCESSED_FOLDER="$(dirname "$IN_FILE")"/processed

# make output in tagger directory

if [ -d ./utils/ABLTagger/data/$VERSION ]
then
  rm -r ./utils/ABLTagger/data/$VERSION
  mkdir -p ./utils/ABLTagger/data/$VERSION
else
  mkdir -p ./utils/ABLTagger/data/$VERSION
fi


echo "Processing file for tagger..."

python3 ./utils/ABLTagger/preprocess/generate_coarse_training_set.py -i ./$IN_FILE -o ./utils/ABLTagger/data/$VERSION/${VERSION}.coarse
python3 ./utils/ABLTagger/preprocess/generate_fine_training_set.py -i ./$IN_FILE -o ./utils/ABLTagger/data/$VERSION/${VERSION}.fine

echo "File processed"

echo "Uploading output folder to dropbox..."
./utils/Dropbox-Uploader/dropbox_uploader.sh delete far/$VERSION
./utils/Dropbox-Uploader/dropbox_uploader.sh upload ./utils/ABLTagger/data/$VERSION far/

echo "All done!"
