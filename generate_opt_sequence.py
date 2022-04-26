import itertools


def read_optimizations():
    opts = []
    file1 = open('optimizations_huawei.txt', 'r')
    lines = file1.readlines()
    for opt in lines:
        opts.append(opt.strip())
    return opts


def generate_possible_combinations(opts):
    all_combinations = []
    for r in range(len(opts) + 1):
        combinations_object = itertools.combinations(opts, r)
        combinations_list = list(combinations_object)
        all_combinations += combinations_list

    # print(all_combinations)
    return all_combinations


def generate_table_entry(opts, combination):
    row = []
    for opt in opts:
        if opt in combination:
            row.append('x')
        else:
            row.append(" ")
    return row


def create_optimization_options():
    opts = read_optimizations()
    return generate_possible_combinations(opts)


def create_other_optimization_options(my_opts):
    opts = read_optimizations()
    for my_opt in my_opts:
        opts.remove(my_opt)
    return generate_possible_combinations(opts)