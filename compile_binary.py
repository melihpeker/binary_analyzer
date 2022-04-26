import os
import subprocess


def compile_binary_generic(path, name, options, index):
    output_path = "bins/" + name
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    elif not os.path.isdir(output_path):
        os.mkdir(output_path)
    output = os.path.join(output_path, name + "_" + str(index))
    command = "gcc-8 " + options + " " + path + " -o " + output
    # command = "gcc-8 -I dataset/polybench-c-3.2/utilities -I dataset/polybench-c-3.2/linear-algebra/kernels/atax dataset/polybench-c-3.2/utilities/polybench.c dataset/polybench-c-3.2/linear-algebra/kernels/atax/atax.c -DPOLYBENCH_TIME -o atax_base"
    # os.system(command)
    # command = "gcc -v"
    env = os.environ.copy()
    getVersion = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, env=env).stdout
    version = getVersion.read()
    print(version)
    run_times = []
    for i in range(5):
        command = "./" + output
        get_runtime = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, env=env).stdout
        time = get_runtime.read()
        run_times.append(float(time.decode()))
    print("Mean run time ", sum(run_times)/5)
    return sum(run_times)/5


def compile_binary(path, name, output_path, options):
    command = "gcc-8 -O2 " + options + " -I dataset/polybench-c-3.2/utilities -I " + \
              path + " dataset/polybench-c-3.2/utilities/polybench.c " +\
              name + " -DPOLYBENCH_TIME -o " + output_path
    # command = "gcc-8 -I dataset/polybench-c-3.2/utilities -I dataset/polybench-c-3.2/linear-algebra/kernels/atax dataset/polybench-c-3.2/utilities/polybench.c dataset/polybench-c-3.2/linear-algebra/kernels/atax/atax.c -DPOLYBENCH_TIME -o atax_base"
    # os.system(command)
    # command = "gcc -v"
    env = os.environ.copy()
    getVersion = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, env=env).stdout
    version = getVersion.read()
    run_times = []
    for i in range(5):
        command = "./" + output_path
        get_runtime = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, env=env).stdout
        time = get_runtime.read()
        run_times.append(float(time.decode()))
    print("Mean run time ", sum(run_times)/5)
    return sum(run_times)/5

