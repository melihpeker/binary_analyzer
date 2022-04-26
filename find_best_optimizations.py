import csv
import numpy as np
import matplotlib.pyplot as plt
from generate_opt_sequence import read_optimizations, create_optimization_options
import pandas as pd


def write_labels_to_csv(labels):
    csv_input = pd.read_csv('graph_properties.csv')
    csv_input['label'] = labels
    csv_input.to_csv('graph_properties.csv', index=False)


with open('run_times_o2_opts.csv', 'r', encoding='UTF8') as f:
    reader = csv.DictReader(f)
    dataset_names = []
    for row in reader:
        if not row['name'] in dataset_names:
            # if float(row[None][0]) <= correlation_o3_time:
            dataset_names.append(row['name'])

o2_times = {k: 0.0 for k in dataset_names}

with open('run_times_o2_opts.csv', 'r', encoding='UTF8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if o2_times[row['name']] == 0.0:
            o2_times[row['name']] = float(row['time'])


run_times = {k: [] for k in dataset_names}

# Fixing random state for reproducibility
np.random.seed(19680801)

'''
with open('run_times_part1.csv', 'r', encoding='UTF8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # if float(row[None][0]) <= correlation_o3_time:
        print(row['name'], float(row[None][0]))
        run_times[row['name']].append(float(row[None][0]))
    # write the header
'''

with open('run_times_o2_opts.csv', 'r', encoding='UTF8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # if float(row[None][0]) <= correlation_o3_time:
        # print(row['name'], float(row[None][0]))
        run_times[row['name']].append(float(row['time']))
    # write the header

''' For this occasion only - DELETE
run_times = {k: [] for k in dataset_names}
with open('run_times.csv', 'r', encoding='UTF8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # if float(row[None][0]) <= correlation_o3_time:
        # print(row['name'], float(row[None][0]))
        run_times[row['name']].append(float(row[None][0]))
    # write the header

labels = []
for idx, data in enumerate(dataset_names):
    if run_times[data]:
        # options = create_optimization_options()
        sorted_runtimes = sorted(run_times[data])

        label = 1
        if sorted_runtimes[0] < 0.5:
            label = 0
        labels.append(label)
            # min_index = run_times[data].index(min(run_times[data]))

write_labels_to_csv(labels)
For this occasion only - DELETE'''

labels = []
for idx, data in enumerate(dataset_names):
    for time in run_times[data]:
        if time < 0.5:
            labels.append(0)
        else:
            labels.append(1)

'''
opts = read_optimizations()
all_optimizations = {}
labels = []
for idx, data in enumerate(dataset_names):
    if run_times[data]:
        opts = read_optimizations()
        options = create_optimization_options()

        best_optimizations = []
        sorted_runtimes = sorted(run_times[data])

        keydict = dict(zip(options, run_times[data]))
        options.sort(key=keydict.get)

        min_index = 0
        min_runtime = sorted_runtimes[min_index]
        while min_runtime == 0:
            min_index = min_index + 1
            min_runtime = sorted_runtimes[min_index]

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

'''
write_labels_to_csv(labels)
fs = 9  # fontsize

pos = [0]
fig, axs = plt.subplots(4,7, figsize=(15, 10), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .5, wspace=.5)
axs = axs.ravel()

index = 0
for idx, data in enumerate(dataset_names):
    if run_times[data]:
        run_times[data] = [i for i in run_times[data] if i != 0]
        axs[index].violinplot(run_times[data], pos, points=235, widths=0.5,
                             showmeans=True, showextrema=True, showmedians=False)
        axs[index].hlines(o2_times[data], axs[index].get_xlim()[0], axs[index].get_xlim()[1], color='red', linestyle='-', lw=2, label='O2  Time')
        axs[index].set_title(data, fontsize=fs)
        axs[index].get_xaxis().set_visible(False)
        index = index + 1

handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right')

fig.suptitle("Different Optimization Run Times with O2 Baseline")
fig.subplots_adjust(hspace=0.4)
# plt.show()
plt.savefig('plots/o2vsOpts.png', dpi=600)