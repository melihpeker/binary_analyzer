import os
from generate_opt_sequence import *
import subprocess
import time
import csv
import pickle
from graph_writer import save_graph, read_graph
from analyze_bin import analyze_bin, write_edges_to_csv, write_features_to_csv
from compile_binary import compile_binary, compile_binary_generic


main_path = "/Users/melihpeker/Documents/Master/dataset/cBench_V1.1_test"
all_datasets = os.listdir("/Users/melihpeker/Documents/Master/dataset/cBench_V1.1_test")

with open("skipped.txt", 'w') as f:
    f.write("Skipped:")

def change_gcc_version():
    for dataset in all_datasets:
        try:
            makefile_path = os.path.join(main_path, dataset, "src", "Makefile.gcc")
            file = open(makefile_path, 'r')

            Lines = file.readlines()
            for idx, line in enumerate(Lines):
                if "gcc" in line:
                    print(line + " replaced with ")
                    line = line.replace("gcc", "gcc-11")
                    print(line)
                    Lines[idx] = line
                    print(" ")

            file.close()

            file = open(makefile_path, 'w')
            file.writelines(Lines)
            file.close()

        except:
            print("NO MAKEFILE")


def change_optimization(dataset, option):
    makefile_path = os.path.join(main_path, dataset, "src", "Makefile.gcc")
    file = open(makefile_path, 'r')

    Lines = file.readlines()
    for idx, line in enumerate(Lines):
        if "CCC_OPTS =" in line:
            line = "CCC_OPTS =" + option + "\n"
            """
            if line[-1] == "\n":
                line = line[:-1] + option
            else:
                line = line + option
            """
            Lines[idx] = line
        elif "CCC_OPTS_ADD =" in line:
            line = "CCC_OPTS_ADD =" + option + "\n"
            Lines[idx] = line

    file.close()

    file = open(makefile_path, 'w')
    file.writelines(Lines)
    file.close()


def run_times(dataset, row):
    os.chdir(os.path.join(main_path, dataset, "src"))
    env = os.environ.copy()
    subprocess.call("./__compile gcc", shell=True, stdout=subprocess.PIPE, env=env)
    timeStarted = time.time()  # Save start time.
    subprocess.call("./__run 1", shell=True, stdout=subprocess.PIPE, env=env)
    timeDelta = time.time() - timeStarted
    row.append(str(timeDelta))
    os.chdir("/Users/melihpeker/Documents/Master/")


opts = read_optimizations()
options = create_optimization_options()

os.chdir("/Users/melihpeker/Documents/Master/")

with open('run_times_cbench_o2_opts_TEST.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the header
    header = ['name']
    for opt in opts:
        header.append(opt)
    header.append('time')
    writer.writerow(header)

with open('graph_edges_cbench_TEST.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the header
    header = ['graph_id', 'src', 'dst']
    writer.writerow(header)

with open('graph_features_cbench_TEST.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the header
    header = ['graph_id', 'node_id', 'arithmetic', 'arithmetic_FP', 'memory', 'memory_FP',
              'compare', 'jump', 'call', 'ret', 'reg', 'number_of_ins',
              'number_of_predecessors', 'number_of_successors', 'loop_depth']
    writer.writerow(header)


graph_id = 0
for dataset in all_datasets:
    for idx, combination in enumerate(options):
        row = [dataset]
        table_entry = generate_table_entry(opts, combination)
        for entry in table_entry:
            row.append(entry)

        option = "-O2 " + ' '.join(options[idx])
        print(dataset + " " + option)
        try:
            change_optimization(dataset, option)
            run_times(dataset, row)
            output_file = os.path.join(main_path, dataset, "src", "a.out")

            graph_single = analyze_bin(output_file)
            write_edges_to_csv(graph_single, graph_id, 'graph_edges_cbench_TEST.csv')
            write_features_to_csv(graph_single, graph_id, 'graph_features_cbench_TEST.csv')

            with open('run_times_cbench_o2_opts_TEST.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header
                writer.writerow(row)

            graph_id += 1

        except:
            with open("skipped.txt", 'a') as f:
                f.write(dataset + " " + option)
            print(dataset + " " + option + " SKIPPED!")



