# Ultra-Low Latency User-Plane Cyberattack Detection in SDN-based Smart Grids

 This repository contains the public version of the code for our work on cyberattack detection in SDN-based smart grids at line rate leveraging user-plane inference.

The paper is currently under review.

## Organization of the repository  
There are two folders:  
- _User_Plane_Inference_ : P4 code compiled and tested on an Intel Tofino switch, and the model table entries file.
- _Data_Analysis_ : scripts and instructions for processing the data, the jupyter notebooks for training the machine learning models, the python scripts for generating the M/A table entries from the saved trained models, and the control plane code for the benchmark solutions.

## Use case
The use case considered in the paper is a DNP3 attack detection and classification use case based on the publicly available <a href="https://ieee-dataport.org/documents/dnp3-intrusion-detection-dataset">DNP3 Intrusion Detection Dataset</a>. <br>The challenge is to classify traffic into one of 7 classes of which 1 is benign and 6 are malicious.

If you need any additional information, send us an email at _aristide.akem_ at _imdea.org_.