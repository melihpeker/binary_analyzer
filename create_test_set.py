import csv
import numpy as np
import matplotlib.pyplot as plt
from generate_opt_sequence import *
import pandas as pd
from itertools import combinations


all_opts = read_optimizations()


def filter_edges(index, name):
    csv_input = pd.read_csv('graph_edges_cbench.csv')
    csv_input = csv_input[csv_input['graph_id'] == index]
    csv_input['graph_id'] = 0
    csv_input.to_csv('graph_edges_cbench_test_' + name + '.csv', index=False)


def filter_features(index, name):
    csv_input = pd.read_csv('graph_features_cbench.csv')
    csv_input = csv_input[csv_input['graph_id'] == index]
    csv_input['graph_id'] = 0
    csv_input.to_csv('graph_features_cbench_test_' + name + '.csv', index=False)


def filter_properties(index, name):
    csv_input = pd.read_csv('graph_properties_cbench.csv')
    csv_input = csv_input[csv_input['graph_id'] == index]
    csv_input['graph_id'] = 0
    csv_input.to_csv('graph_properties_cbench_test_' + name + '.csv', index=False)


# create_graph_properties()
# combine_sets()

with open('run_times_cbench_o2_opts.csv', 'r', encoding='UTF8') as f:
    reader = csv.DictReader(f)
    dataset_names = []
    for row in reader:
        if not row['name'] in dataset_names:
            # if float(row[None][0]) <= correlation_o3_time:
            dataset_names.append(row['name'])


o2_times = {k: 0.0 for k in dataset_names}

with open('run_times_cbench_o2_opts.csv', 'r', encoding='UTF8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if o2_times[row['name']] == 0.0:
            o2_times[row['name']] = float(row['time'])

run_times = {k: [] for k in dataset_names}
sequences = {k: [] for k in dataset_names}

with open('run_times_cbench_o2_opts.csv', 'r', encoding='UTF8') as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader):
        # if float(row[None][0]) <= correlation_o3_time:
        # print(row['name'], float(row[None][0]))
        run_times[row['name']].append(float(row['time']))
        my_row = []
        for opt in all_opts:
            my_row.append(row[opt])
        sequences[row['name']].append((my_row, float(row['time']), idx))

number_of_all_graphs = idx + 1

labels = []

for idx, data in enumerate(dataset_names):
    before = False
    after = False
    row = generate_table_entry(all_opts, [])
    for lists in sequences[data]:
        if row == lists[0]:
            before_runtime = lists[1]
            before_idx = lists[2]
            print(before_idx)
            before = True
    filter_edges(before_idx, data)
    filter_features(before_idx, data)
    filter_properties(before_idx, data)



