# binary_analyzer
 
* After arranging the directories, call main.py for generating datasets.
* For specific versions of `gcc` change the `gcc-8` from the compilation command in the `compile_binary.py` script.
* After generating datasets, run `label_graphs.py` script for labeling graphs as 1-0. 
* There will be 3 outputs form the main.py:
     - graph_edges.csv
     - graph_properties.csv
     - graph_features.csv
* These files represents the graph version of each compiled program. 
* These three files should be uploaded to the following colab script for GNN training:
https://colab.research.google.com/drive/1orbq_2Vz0vZ-x5QatKnT4FPDS3OJ33ad?usp=sharing