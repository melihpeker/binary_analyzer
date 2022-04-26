import csv
import numpy as np
import matplotlib.pyplot as plt
from generate_opt_sequence import *
import pandas as pd
from tqdm import tqdm


properties = pd.read_csv('graph_properties-funsafe-math-optimizations.csv')
all_labels = properties['label'].to_list()

features = pd.read_csv('graph_features-funsafe-math-optimizations.csv')


prev_id = 0
keys = ['graph_id', 'arithmetic', 'arithmetic_FP', 'memory', 'memory_FP',
                'compare', 'jump', 'call', 'ret', 'reg', 'number_of_ins',
                        'number_of_predecessors', 'number_of_successors', 'number_of_loops1', 'number_of_loops2',  'number_of_loops3']
graph = {k: 0 for k in keys}
graphs = []
for index, row in tqdm(features.iterrows()):
    if row['graph_id'] == prev_id:
        for key in keys:
            if not (key == 'graph_id' or key == 'loop_depth' or key =='number_of_loops3' or key == 'number_of_loops2' or key == 'number_of_loops1'):
                graph[key] += row[key]
        key = 'loop_depth'
        if row[key] == 1:
            graph['number_of_loops1'] += 1
        if row[key] == 2:
            graph['number_of_loops2'] += 1
        if row[key] == 3:
            graph['number_of_loops3'] += 1
    else:
        graphs.append(graph)
        graph = {k: 0 for k in keys}
        graph['graph_id'] = row['graph_id']
        prev_id = row['graph_id']

graphs.append(graph)


csv_file = 'flat_graphs.csv'
with open(csv_file, 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the header
    header = ['graph_id', 'arithmetic', 'arithmetic_FP', 'memory', 'memory_FP',
                'compare', 'jump', 'call', 'ret', 'reg', 'number_of_ins',
                        'number_of_predecessors', 'number_of_successors', 'number_of_loops1', 'number_of_loops2',  'number_of_loops3']

    writer.writerow(header)

with open(csv_file, 'a', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the header
    for row in graphs:
        writer.writerow(list(row.values()))


csv_file = 'flat_labels.csv'
with open(csv_file, 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(['label'])
    for row in all_labels:
        writer.writerow([row])