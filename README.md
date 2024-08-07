# binary_analyzer

This repo is for analyzing binaries and creating a GNN models for chosing better optimization flags. The main pipeline is as follows:

1. Compile the benchmark programs given in `dataset` folder.
2. For each executable, we analyze the binary file and create a graph representation with node features for each binary file.
3. These representations are saved as CSV files and then these CSV files are used for GNN training that is given in the Google Colab link.

## Instructions

* Download the Polybench dataset from here: https://sourceforge.net/projects/polybench/
* Move the dataset folder to the folder that is named as `dataset` under the main directory.
* Install the requirements in a Python 3.9 (or higher) environment:
  `pip install -r requirements.txt`
* After arranging the directories, call main.py for generating datasets.
* For using other benchmark sets, you need to modify the `gcc` compile command given in `complie_binary.py` script as for each benchmark set we need to include some additional libraries. Currently this command is arranged for compiling polybench as follows:
```
command = "gcc -O2 " + options + " -I dataset/polybench-c-3.2/utilities -I " + \
              path + " dataset/polybench-c-3.2/utilities/polybench.c " +\
              name + " -DPOLYBENCH_TIME -o " + output_path
```
* For specific versions of `gcc` change the `gcc` from the compilation command.
* There will be 3 outputs form the main.py:
     - graph_edges.csv
     - graph_properties.csv
     - graph_features.csv
* These files represents the graph version of each compiled program.
* After generating datasets, run `label_graphs.py` script for generating the training GT data by labeling graphs as 1-0 (whether this program will benefit from this particular optimization or not).
* This scirpt will generate training data for each optimization option as follows:
     - graph_edges_funroll-loops.csv
     - graph_properties_funroll-loops.csv
     - graph_features_funroll-loops.csv
     - graph_edges_funsafe-math-optimizations.csv
     - graph_properties_funsafe-math-optimizations.csv
     - graph_features_funsafe-math-optimizations.csv
* These three files for each optimization flag should be uploaded to the following colab script for GNN training:
https://colab.research.google.com/drive/1orbq_2Vz0vZ-x5QatKnT4FPDS3OJ33ad?usp=sharing
* This scirpt can be used for training a GNN graph classification model for each flag. At the end, we will have a model for each optimizaiton option that will tell us whether the input program may benefit from this optimization.
