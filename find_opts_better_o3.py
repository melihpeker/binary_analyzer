import csv
import numpy as np
import matplotlib.pyplot as plt
from generate_opt_sequence import read_optimizations, create_optimization_options
import pandas as pd


def write_labels_to_csv(labels):
    csv_input = pd.read_csv('graph_properties.csv')
    csv_input['label'] = labels
    csv_input.to_csv('graph_properties.csv', index=False)


with open('run_times_o3.csv', 'r', encoding='UTF8') as f:
    reader = csv.DictReader(f)
    dataset_names = []
    for row in reader:
        # if float(row[None][0]) <= correlation_o3_time:
        dataset_names.append(row['name'])

o3_times = {k: 0.0 for k in dataset_names}

with open('run_times_o3.csv', 'r', encoding='UTF8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        o3_times[row['name']] = float(row[None][0])

run_times = {k: [] for k in dataset_names}

# Fixing random state for reproducibility
np.random.seed(19680801)
with open('run_times_all.csv', 'r', encoding='UTF8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # if float(row[None][0]) <= correlation_o3_time:
        # print(row['name'], float(row[None][0]))
        run_times[row['name']].append(float(row[None][0]))
    # write the header


opts = read_optimizations()
all_optimizations = {}
labels = []
for idx, data in enumerate(dataset_names):
    if run_times[data] and o3_times[data]:
        # options = create_optimization_options()
        opts = read_optimizations()
        options = opts
        best_optimizations = []
        sorted_runtimes = sorted(run_times[data])

        keydict = dict(zip(options, run_times[data]))
        options.sort(key=keydict.get)

        min_index = 0
        min_runtime = sorted_runtimes[min_index]
        while min_runtime == 0:
            min_index = min_index + 1
            min_runtime = sorted_runtimes[min_index]

        while sorted_runtimes[min_index] < o3_times[data]:
            best_optimizations.append(options[min_index])
            min_index = min_index + 1

        print("Best optimization for  " + data + " :")
        label = 1
        for idx in range(10):
            best_optimizations.append(options[min_index + idx])
            print(options[min_index + idx])
            if options[min_index + idx] in all_optimizations:
                all_optimizations[options[min_index + idx]] = all_optimizations[options[min_index + idx]] + 1
            else:
                all_optimizations[options[min_index + idx]] = 1

            # if options[min_index + idx] == '-fstack-protector-strong':
            #    label = 1

        if min_runtime < 0.5:
            label = 0
        labels.append(label)
        # min_index = run_times[data].index(min(run_times[data]))
        print("Min run time of " + data + " : " + str(min_runtime))

