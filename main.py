import angr
from angr.analyses.loop_analysis import LoopAnalysis
import os

import csv
import pickle
from graph_writer import save_graph, read_graph
from analyze_bin import analyze_bin, write_edges_to_csv, write_features_to_csv
from compile_binary import compile_binary, compile_binary_generic
from generate_opt_sequence import *


opts = read_optimizations()
options = create_optimization_options()
with open('run_times_o2_opts.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the header
    header = ['name']
    for opt in opts:
        header.append(opt)
    header.append('time')
    writer.writerow(header)


with open('run_times_o2.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the header
    header = ['name', '-O2']
    writer.writerow(header)


with open('graph_edges.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header
        header = ['graph_id', 'src', 'dst']
        writer.writerow(header)


with open('graph_features.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the header
    header = ['graph_id', 'node_id', 'arithmetic', 'arithmetic_FP', 'memory', 'memory_FP',
                'compare', 'jump', 'call', 'ret', 'reg', 'number_of_ins',
                        'number_of_predecessors', 'number_of_successors', 'loop_depth']
    writer.writerow(header)


with open('graph_id_name.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the header
    header = ['graph_id', 'name']
    writer.writerow(header)


with open('graph_properties.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the header
    header = ['graph_id', 'label', 'num_nodes']
    writer.writerow(header)


graph_id = 0
path = os.listdir("dataset/poly_custom/")
print(path)
path = 'codes'
output_path = "bins/" + path
if not os.path.exists(output_path):
    os.mkdir(output_path)
elif not os.path.isdir(output_path):
    os.mkdir(output_path)

if not os.path.exists("graphs/" + path):
    os.mkdir("graphs/" + path)

abs_path = os.path.join("dataset/poly_custom/") + path


for file in os.listdir(abs_path):
    if file.endswith(".c"):
        file = file.split('.')[0]
        for idx, combination in enumerate(options):
            row = [file]
            table_entry = generate_table_entry(opts, combination)
            for entry in table_entry:
                row.append(entry)

            output_file = os.path.join(output_path, file + '_' + str(idx))

            option = ' '.join(options[idx])
            print(option)

            try:
                mean_time = compile_binary(abs_path, os.path.join(abs_path, file + '.c'), output_file, option)
                row.append(str(mean_time))
            except:
                row.append(str(-1))

            try:
                graph_single = analyze_bin(output_file)
                write_edges_to_csv(graph_single, graph_id, 'graph_edges.csv')
                write_features_to_csv(graph_single, graph_id, 'graph_features.csv')

                with open('run_times_o2_opts.csv', 'a', encoding='UTF8') as f:
                    writer = csv.writer(f)
                    # write the header
                    writer.writerow(row)

                with open('graph_properties.csv', 'a', encoding='UTF8') as f:
                    writer = csv.writer(f)
                    # write the header
                    row = [graph_id, 0, len(graph_single.nodes)]
                    writer.writerow(row)

                with open('graph_id_name.csv', 'a', encoding='UTF8') as f:
                    writer = csv.writer(f)
                    # write the header
                    row = [str(graph_id), path]
                    writer.writerow(row)

                graph_id = graph_id + 1

                # save_graph(graph_single, os.path.join('graphs', file, file+str(idx)))
            except:
                print("graph couldn't saved")


print("O2 TIMES FINISHED")
'''
graph_id = 0
paths = os.listdir("dataset/polybench-c-3.2/datamining/")
for path in paths:
    if not path == '.DS_Store':
        print(path)
        output_path = "bins/" + path
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        elif not os.path.isdir(output_path):
            os.mkdir(output_path)

        if not os.path.exists("graphs/" + path):
            os.mkdir("graphs/" + path)

        abs_path = os.path.join("dataset/polybench-c-3.2/datamining/") + path
        for idx, combination in enumerate(options):
            row = [path]
            table_entry = generate_table_entry(opts, combination)
            for entry in table_entry:
                row.append(entry)

            output_file = os.path.join(output_path, path + "_base_" + str(idx))

            # option = ' '.join(options[idx])
            # print(options[idx])
            try:
                mean_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), output_file, options[idx])
                row.append(str(mean_time))
            except:
                row.append(str(-1))
            try:
                graph_single = analyze_bin(output_file)
                write_edges_to_csv(graph_single, graph_id, 'graph_edges.csv')
                write_features_to_csv(graph_single, graph_id, 'graph_features.csv')
                save_graph(graph_single, os.path.join('graphs', path, path+str(idx)))
            except:
                print("graph couldn't saved")

            with open('run_times.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header
                writer.writerow(row)

            with open('graph_properties.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header
                row = [graph_id, 0, len(graph_single.nodes)]
                writer.writerow(row)

            with open('graph_id_name.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header
                row = [str(graph_id), path]
                writer.writerow(row)
            graph_id = graph_id + 1

aths = os.listdir("dataset/polybench-c-3.2/linear-algebra/kernels")
for path in paths:
    if not path in ['.DS_Store']:
        print(path)
        output_path = "bins/" + path
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        elif not os.path.isdir(output_path):
            os.mkdir(output_path)

        if not os.path.exists("graphs/" + path):
            os.mkdir("graphs/" + path)

        abs_path = os.path.join("dataset/polybench-c-3.2/linear-algebra/kernels/") + path
        for idx, combination in enumerate(options):
            row = [path]
            table_entry = generate_table_entry(opts, combination)
            for entry in table_entry:
                row.append(entry)

            output_file = os.path.join(output_path, path + "_" + str(idx))

            # option = ' '.join(options[idx])
            # print(options[idx])
            try:
                mean_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), output_file, options[idx])
                row.append(str(mean_time))
            except:
                row.append(str(-1))

            try:
                graph_single = analyze_bin(output_file)
                write_edges_to_csv(graph_single, graph_id, 'graph_edges.csv')
                graph_id = graph_id + 1
                save_graph(graph_single, os.path.join('graphs', path, path + str(idx)))
            except:
                print("graph couldn't saved")

            with open('graph_properties.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header
                row = [graph_id, 0, len(graph_single.nodes)]
                writer.writerow(row)

            with open('run_times.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header
                writer.writerow(row)


paths = os.listdir("dataset/polybench-c-3.2/linear-algebra/solvers")
for path in paths:
    if not path == '.DS_Store':
        print(path)
        output_path = "bins/" + path
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        elif not os.path.isdir(output_path):
            os.mkdir(output_path)

        if not os.path.exists("graphs/" + path):
            os.mkdir("graphs/" + path)

        abs_path = os.path.join("dataset/polybench-c-3.2/linear-algebra/solvers/") + path
        for idx, combination in enumerate(options):
            row = [path]
            table_entry = generate_table_entry(opts, combination)
            for entry in table_entry:
                row.append(entry)

            output_file = os.path.join(output_path, path + "_" + str(idx))

            option = ' '.join(options[idx])
            print(options[idx])
            try:
                mean_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), output_file, options[idx])
                row.append(str(mean_time))
            except:
                row.append(str(-1))

            try:
                graph_single = analyze_bin(output_file)
                save_graph(graph_single, os.path.join('graphs', path, path + str(idx)))
            except:
                print("graph couldn't saved")

            with open('graph_properties.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header
                row = [graph_id, 0, len(graph_single.nodes)]
                writer.writerow(row)

            with open('run_times.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header
                writer.writerow(row)


paths = os.listdir("dataset/polybench-c-3.2/medley")
for path in paths:
    if not path == '.DS_Store':
        print(path)
        output_path = "bins/" + path
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        elif not os.path.isdir(output_path):
            os.mkdir(output_path)

        if not os.path.exists("graphs/" + path):
            os.mkdir("graphs/" + path)

        abs_path = os.path.join("dataset/polybench-c-3.2/medley/") + path
        for idx, combination in enumerate(options):
            row = [path]
            table_entry = generate_table_entry(opts, combination)
            for entry in table_entry:
                row.append(entry)

            output_file = os.path.join(output_path, path + "_" + str(idx))

            option = ' '.join(options[idx])
            print(options[idx])
            try:
                mean_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), output_file, options[idx])
                row.append(str(mean_time))
            except:
                row.append(str(-1))

            
            try:
                graph_single = analyze_bin(output_file)
                save_graph(graph_single, os.path.join('graphs', path, path + str(idx)))
            except:
                print("graph couldn't saved")
            

            with open('run_times.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header
                writer.writerow(row)

paths = os.listdir("dataset/polybench-c-3.2/stencils")
for path in paths:
    if not path == '.DS_Store':
        print(path)
        output_path = "bins/" + path
        if not os.path.exists(output_path):
            os.mkdir(output_path)
        elif not os.path.isdir(output_path):
            os.mkdir(output_path)

        if not os.path.exists("graphs/" + path):
            os.mkdir("graphs/" + path)

        abs_path = os.path.join("dataset/polybench-c-3.2/stencils/") + path
        for idx, combination in enumerate(options):
            row = [path]
            table_entry = generate_table_entry(opts, combination)
            for entry in table_entry:
                row.append(entry)

            output_file = os.path.join(output_path, path + "_" + str(idx))

            option = ' '.join(options[idx])
            print(options[idx])
            try:
                mean_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), output_file, options[idx])
                row.append(str(mean_time))
            except:
                row.append(str(-1))

            
            try:
                graph_single = analyze_bin(output_file)
                save_graph(graph_single, os.path.join('graphs', path, path + str(idx)))
            except:
                print("graph couldn't saved")
            
            with open('run_times.csv', 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header
                writer.writerow(row)
'''
'''
name = 'main_single'
for idx, combination in enumerate(options):
    row = [name]
    table_entry = generate_table_entry(opts, combination)
    for entry in table_entry:
        row.append(entry)
    if idx < 10:
        option = ''.join(options[idx])
        print(option)
        mean_time = compile_binary_generic("work/main_single.c", name, option, idx)

        row.append(str(mean_time))

        with open('run_times.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(row)


graph_single = analyze_bin('bins/main_single')
# save_graph(graph_single, 'graphs/main_single')
graph_single_read = read_graph('graphs/main_single')

graph_bin = analyze_bin('bins/main_bin')
# save_graph(graph_bin, 'graphs/main_bin')
graph_bin_read = read_graph('graphs/main_bin')


with open('run_times.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    # write the header
    row = ['name', 'base', 'O1', 'O2', 'O3']
    writer.writerow(row)

# name = compile_binary('a', 'a', 'a', 'a')
paths = os.listdir("dataset/polybench-c-3.2/datamining/")
for path in paths:
    if not path == '.DS_Store':
        print(path)
        abs_path = os.path.join("dataset/polybench-c-3.2/datamining/") + path
        base_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_base', [])
        o1_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_o1', ['-O1'])
        o2_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_o2', ['-O2'])
        o3_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_o3', ['-O3'])
        row = [path, base_time, o1_time, o2_time, o3_time]

        with open('run_times.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(row)


paths = os.listdir("dataset/polybench-c-3.2/linear-algebra/kernels")
for path in paths:
    if not path == '.DS_Store':
        print(path)
        abs_path = os.path.join("dataset/polybench-c-3.2/linear-algebra/kernels/") + path
        base_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_base', [])
        o1_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_o1', ['-O1'])
        o2_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_o2', ['-O2'])
        o3_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_o3', ['-O3'])
        row = [path, base_time, o1_time, o2_time, o3_time]

        with open('run_times.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(row)

paths = os.listdir("dataset/polybench-c-3.2/linear-algebra/solvers")
for path in paths:
    if not path == '.DS_Store':
        print(path)
        abs_path = os.path.join("dataset/polybench-c-3.2/linear-algebra/solvers/") + path
        base_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_base', [])
        o1_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_o1', ['-O1'])
        o2_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_o2', ['-O2'])
        o3_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_o3', ['-O3'])
        row = [path, base_time, o1_time, o2_time, o3_time]

        with open('run_times.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(row)

paths = os.listdir("dataset/polybench-c-3.2/medley")
for path in paths:
    if not path == '.DS_Store':
        print(path)
        abs_path = os.path.join("dataset/polybench-c-3.2/medley/") + path
        base_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_base', [])
        o1_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_o1', ['-O1'])
        o2_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_o2', ['-O2'])
        o3_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_o3', ['-O3'])
        row = [path, base_time, o1_time, o2_time, o3_time]

        with open('run_times.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(row)

paths = os.listdir("dataset/polybench-c-3.2/stencils")
for path in paths:
    if not path == '.DS_Store':
        print(path)
        abs_path = os.path.join("dataset/polybench-c-3.2/stencils/") + path
        base_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_base', [])
        o1_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_o1', ['-O1'])
        o2_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_o2', ['-O2'])
        o3_time = compile_binary(abs_path, os.path.join(abs_path, path + '.c'), path + '_o3', ['-O3'])
        row = [path, base_time, o1_time, o2_time, o3_time]

        with open('run_times.csv', 'a', encoding='UTF8') as f:
            writer = csv.writer(f)
            # write the header
            writer.writerow(row)
'''



