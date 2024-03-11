#!/bin/bash

# base folder where all the folders with pcaps of each attack type are located
# same one used in get_pkt_data.sh
root_dir="./"

# loop through each folder
for folder in "$root_dir"/*; do
    if [ -d "$folder" ]; then
        # create a folder to store the labeled packet files  
        labeled_pkt_folder="$folder/Labeled_Pkt_Files"
        mkdir -p "$labeled_pkt_folder"
        pkt_files_folder="$folder/Pkt_Files"

        # Go through the Pkt Files folders and label the packets using the labal info
        if [ -d "$pkt_files_folder" ]; then
            # Traverse through each CSV file in the Pkt Files folder
            for csv_file in "$pkt_files_folder"/*.csv; do
                if [ -f "$csv_file" ]; then
                    echo "Processing CSV file: $(basename "$csv_file")"
                    python3 clean_and_label.py "$csv_file" "$labeled_pkt_folder/$(basename "$csv_file" .csv)_labeled.csv"
                fi
            done
        fi
    fi
done
# merge all the csv files into one final csv in each case
# use load_and_merge.py to merge the csv files
# run these scripts for both the train and test data