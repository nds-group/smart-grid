import os
import shutil
from scapy.all import *

# Point the location containing your split pcap files.
parent_folder = "./"

train_folder = os.path.join(parent_folder, "Train")
test_folder = os.path.join(parent_folder, "Test")
os.makedirs(train_folder, exist_ok=True)
os.makedirs(test_folder, exist_ok=True)

# we go through each of the folders in the main folder
for folder_name in os.listdir(parent_folder):
    folder_path = os.path.join(parent_folder, folder_name)

    if os.path.isdir(folder_path):

        # Traverse through each pcap file in the folder
        for pcap_file in os.listdir(folder_path):

            pcap_file_path = os.path.join(folder_path, pcap_file)

            if pcap_file.endswith(".pcap"):

                # Load the pcap file with Scapy and split it into train and test sets using 75-25 split ratio
                packets = rdpcap(pcap_file_path)
                total_packets = len(packets)
                
                train_packets = packets[:int(0.75 * total_packets)]
                test_packets = packets[int(0.75 * total_packets):]

                # Add a suffix to the two new files to specify whehter they are train or test
                train_pcap_file = os.path.join(folder_path, os.path.splitext(pcap_file)[0] + "_train.pcap")
                test_pcap_file = os.path.join(folder_path, os.path.splitext(pcap_file)[0] + "_test.pcap")

                wrpcap(train_pcap_file, train_packets)
                wrpcap(test_pcap_file, test_packets)

                # Move files to Train or Test folder based on suffix
                if "_train" in train_pcap_file:
                    shutil.move(train_pcap_file, os.path.join(train_folder, os.path.basename(train_pcap_file)))
                if "_test" in test_pcap_file:
                    shutil.move(test_pcap_file, os.path.join(test_folder, os.path.basename(test_pcap_file)))

print("Files split and saved in test and train folders.")
