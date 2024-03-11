import pandas as pd
import numpy as np
import sys

input_file = sys.argv[1] # file to be labelled
output_file = sys.argv[2] # name of output file - these two are catered for in the bash scripts

# label file
Labels = pd.read_csv("./Data_Analysis_DNP3_labs_unique.csv")

packet_data = pd.DataFrame()

packet_data = pd.read_csv(input_file, sep = ',', header=None)

packet_data.columns = ["frame.time_relative","ip.src","ip.dst","tcp.srcport","tcp.dstport","ip.len",
                   "tcp.flags.syn","tcp.flags.ack","tcp.flags.push","tcp.flags.fin",
                   "tcp.flags.reset","tcp.flags.ece","ip.proto","udp.srcport","udp.dstport",
                   "eth.src","eth.dst", "ip.hdr_len", "ip.tos", "ip.ttl", "tcp.window_size_value", 
                   "tcp.hdr_len", "udp.length"]

packet_data = packet_data[(packet_data["ip.proto"] != "1,17") & (packet_data["ip.proto"] != "1,6")].reset_index(drop=True)
packet_data = packet_data.dropna(subset=['ip.proto'])
packet_data["ip.src"] = packet_data["ip.src"].astype(str)
packet_data["ip.dst"] = packet_data["ip.dst"].astype(str)
packet_data["ip.len"] = packet_data["ip.len"].astype("int")
packet_data["ip.proto"] = packet_data["ip.proto"].astype("int")
##the new features from either tcp or udp might have some NA which we set to 0
packet_data["tcp.window_size_value"] = packet_data["tcp.window_size_value"].astype('Int64').fillna(0)
packet_data["tcp.hdr_len"] = packet_data["tcp.hdr_len"].astype('Int64').fillna(0)
packet_data["udp.length"] = packet_data["udp.length"].astype('Int64').fillna(0)
##
packet_data["tcp.srcport"] = packet_data["tcp.srcport"].astype('Int64').fillna(0)
packet_data["tcp.dstport"] = packet_data["tcp.dstport"].astype('Int64').fillna(0)
packet_data["udp.srcport"] = packet_data["udp.srcport"].astype('Int64').fillna(0)
packet_data["udp.dstport"] = packet_data["udp.dstport"].astype('Int64').fillna(0)
packet_data["srcport"] = np.where(packet_data["ip.proto"] == 6, packet_data["tcp.srcport"], packet_data["udp.srcport"])
packet_data["dstport"] = np.where(packet_data["ip.proto"] == 6, packet_data["tcp.dstport"], packet_data["udp.dstport"])
##
packet_data["srcport"] = packet_data["srcport"].astype('Int64')
packet_data["dstport"] = packet_data["dstport"].astype('Int64')

## CREATE THE FLOW IDs AND DROP UNWANTED COLUMNS
packet_data = packet_data.drop(["tcp.srcport","tcp.dstport","udp.srcport","udp.dstport"],axis=1)

packet_data = packet_data.reset_index(drop=True)

packet_data["flow.id"] = packet_data["ip.src"].astype(str) + " " + packet_data["ip.dst"].astype(str) + " " + packet_data["srcport"].astype(str) + " " + packet_data["dstport"].astype(str) + " " + packet_data["ip.proto"].astype(str)
packet_data["flow.id_rev"] = packet_data["ip.dst"].astype(str) + " " + packet_data["ip.src"].astype(str) + " " + packet_data["dstport"].astype(str) + " " + packet_data["srcport"].astype(str) + " " + packet_data["ip.proto"].astype(str)

# Labeling
flow_label_dict = Labels.set_index("Flow ID")["Label"].to_dict()
packet_data["label"] = packet_data["flow.id"].map(flow_label_dict)
packet_data["label2"] = packet_data["flow.id_rev"].map(flow_label_dict)

packet_data["label"] = packet_data["label"].fillna(packet_data["label2"])

# drop unwanted columns
packet_data = packet_data.drop(["label2","flow.id_rev","ip.tos"],axis=1)

packet_data = packet_data.reset_index(drop=True)

# save final data to csv
packet_data.to_csv(output_file,index=False)
