import csv
import numpy as np
import matplotlib.pyplot as plt
from generate_opt_sequence import *
import pandas as pd
from itertools import combinations

all_opts = read_optimizations()


def combine_sets():
    csv_input_1 = pd.read_csv('graph_properties_cbench.csv')
    csv_input_2 = pd.read_csv('graph_properties.csv')
    last_id = csv_input_1.iloc[-1]['graph_id'] + 1
    csv_input_2['graph_id'] = csv_input_2['graph_id'] + last_id

    result = csv_input_1.append(csv_input_2, ignore_index=True)

    result.to_csv('graph_properties_ALL.csv', index=False)

    csv_input_1 = pd.read_csv('graph_edges_cbench.csv')
    csv_input_2 = pd.read_csv('graph_edges.csv')
    last_id = csv_input_1.iloc[-1]['graph_id'] + 1
    csv_input_2['graph_id'] = csv_input_2['graph_id'] + last_id

    result = csv_input_1.append(csv_input_2, ignore_index=True)

    result.to_csv('graph_edges_ALL.csv', index=False)

    csv_input_1 = pd.read_csv('graph_features_cbench.csv')
    csv_input_2 = pd.read_csv('graph_features.csv')
    last_id = csv_input_1.iloc[-1]['graph_id'] + 1
    csv_input_2['graph_id'] = csv_input_2['graph_id'] + last_id

    result = csv_input_1.append(csv_input_2, ignore_index=True)

    result.to_csv('graph_features_ALL.csv', index=False)

    csv_input_1 = pd.read_csv('run_times_cbench_o2_opts.csv')
    csv_input_2 = pd.read_csv('run_times_o2_opts.csv')

    result = csv_input_1.append(csv_input_2, ignore_index=True)

    result.to_csv('run_times_o2_opts_ALL.csv', index=False)


def create_graph_properties():
    csv_input = pd.read_csv('graph_features_cbench.csv')
    graph_id = 0
    num_of_edges = 0
    graphs = []
    for index, line in csv_input.iterrows():
        if line['graph_id'] == graph_id:
            num_of_edges = num_of_edges + 1
        else:
            graphs.append((graph_id, 0, num_of_edges))
            graph_id = line['graph_id']
            num_of_edges = 1
            print(graph_id)

    graphs.append((graph_id, 0, num_of_edges))
    df = pd.DataFrame(graphs, columns=['graph_id', 'label', 'num_nodes'])

    df.to_csv('graph_properties_cbench.csv', index=False)


def write_labels_to_csv(labels, opt):
    csv_input = pd.read_csv('graph_properties_ALL.csv')
    csv_input['label'] = labels
    csv_input.to_csv('graph_properties_ALL' + opt + '.csv', index=False)


def filter_edges(indexes, opt):
    csv_input = pd.read_csv('graph_edges_ALL.csv')

    opt_indexes = []
    for idx, label in enumerate(indexes):
        if not label == -1:
            opt_indexes.append(idx)

    csv_input = csv_input[csv_input['graph_id'].isin(opt_indexes)]

    for idx, old_id in enumerate(opt_indexes):
        csv_input.loc[csv_input.graph_id == old_id, 'graph_id'] = idx
    csv_input.to_csv('graph_edges_ALL' + opt + '.csv', index=False)


def filter_features(indexes, opt):
    csv_input = pd.read_csv('graph_features_ALL.csv')

    opt_indexes = []
    for idx, label in enumerate(indexes):
        if not label == -1:
            opt_indexes.append(idx)

    csv_input = csv_input[csv_input['graph_id'].isin(opt_indexes)]

    for idx, old_id in enumerate(opt_indexes):
        csv_input.loc[csv_input.graph_id == old_id, 'graph_id'] = idx
    csv_input.to_csv('graph_features_ALL' + opt + '.csv', index=False)


def filter_properties(indexes, opt):
    csv_input = pd.read_csv('graph_properties_ALL' + opt + '.csv')

    opt_indexes = []
    for idx, label in enumerate(indexes):
        if not label == -1:
            opt_indexes.append(idx)

    csv_input = csv_input[csv_input['graph_id'].isin(opt_indexes)]

    for idx, old_id in enumerate(opt_indexes):
        csv_input.loc[csv_input.graph_id == old_id, 'graph_id'] = idx
    csv_input.to_csv('graph_properties_ALL' + opt + '.csv', index=False)


# create_graph_properties()
# combine_sets()

with open('run_times_o2_opts_ALL.csv', 'r', encoding='UTF8') as f:
    reader = csv.DictReader(f)
    dataset_names = []
    for row in reader:
        if not row['name'] in dataset_names:
            # if float(row[None][0]) <= correlation_o3_time:
            dataset_names.append(row['name'])


o2_times = {k: 0.0 for k in dataset_names}

with open('run_times_o2_opts_ALL.csv', 'r', encoding='UTF8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if o2_times[row['name']] == 0.0:
            o2_times[row['name']] = float(row['time'])

run_times = {k: [] for k in dataset_names}
sequences = {k: [] for k in dataset_names}

with open('run_times_o2_opts_ALL.csv', 'r', encoding='UTF8') as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader):
        # if float(row[None][0]) <= correlation_o3_time:
        # print(row['name'], float(row[None][0]))
        run_times[row['name']].append(float(row['time']))
        my_row = []
        for opt in all_opts:
            my_row.append(row[opt])
        sequences[row['name']].append((my_row, float(row['time']), idx))


# write the header
# run_times = {k: [] for k in dataset_names}

# Fixing random state for reproducibility
np.random.seed(19680801)

number_of_all_graphs = idx + 1
all_optimizations = {}

opts_combinations = list(combinations(all_opts, 2))
for opts_of_two in all_opts:
    print(opts_of_two)
    labels = [-1] * number_of_all_graphs
    options_without_opt = create_other_optimization_options(opts_of_two)
    index_1 = all_opts.index(opts_of_two)
    # index_2 = all_opts.index(opts_of_two[1])
    for idx, data in enumerate(dataset_names):
        for options in options_without_opt:
            runtimes = []
            before = False
            after = False
            row = generate_table_entry(all_opts, options)
            for lists in sequences[data]:
                if row == lists[0]:
                    before_runtime = lists[1]
                    before_idx = lists[2]
                    before = True
                    runtimes.append(before_runtime)

            row[index_1] = 'x'
            for lists in sequences[data]:
                if row == lists[0]:
                    runtimes.append(lists[1])
                    after_idx = lists[2]
                    after = True
            '''
            row = generate_table_entry(all_opts, options)
            row[index_2] = 'x'
            for lists in sequences[data]:
                if row == lists[0]:
                    runtimes.append(lists[1])
                    after_idx = lists[2]
                    after = True

            row = generate_table_entry(all_opts, options)
            row[index_1] = 'x'
            row[index_2] = 'x'
            for lists in sequences[data]:
                if row == lists[0]:
                    runtimes.append(lists[1])
                    after_idx = lists[2]
                    after = True
            '''
            try:
                min_runtime = np.argmin(runtimes)
                if runtimes[0] - runtimes[min_runtime] > (runtimes[0] * 0.10):
                    labels[before_idx] = min_runtime
                else:
                    labels[before_idx] = 0
            except:
                labels[before_idx] = -1

        name = ''.join(map(str, opts_of_two))
        write_labels_to_csv(labels, name)
    filter_edges(labels, name)
    filter_features(labels, name)
    filter_properties(labels, name)
    count_a = labels.count(0)
    print(f'{count_a=}')
    count_a = labels.count(1)
    print(f'{count_a=}')
    count_a = labels.count(2)
    print(f'{count_a=}')
    count_a = labels.count(3)
    print(f'{count_a=}')

'''
for idx_opt, opt in enumerate(all_opts):
    labels = [-1] * number_of_all_graphs
    options_without_opt = create_other_optimization_options(opt)
    print(opt)
    for idx, data in enumerate(dataset_names):
        for options in options_without_opt:
            before = False
            after = False
            row = generate_table_entry(all_opts, options)
            for lists in sequences[data]:
                if row == lists[0]:
                    before_runtime = lists[1]
                    before_idx = lists[2]
                    before = True

            row[idx_opt] = 'x'
            for lists in sequences[data]:
                if row == lists[0]:
                    after_runtime = lists[1]
                    after_idx = lists[2]
                    after = True

            if before and after:
                if before_runtime - after_runtime > (before_runtime * 0.10):
                    labels[before_idx] = 1
                else:
                   labels[before_idx] = 0
        write_labels_to_csv(labels, opt)
    filter_edges(labels, opt)
    filter_features(labels, opt)
    filter_properties(labels, opt)
'''





