from graph_writer import read_graph
import networkx as nx
from analyze_bin import *

class Loop:
    def __init__(self, name, info, depth):
        self.name = name
        self.info = info
        self.depth = depth


class Bin:
    def __init__(self, name, functions):
        self.name = name
        self.functions = functions
        self.number_of_blocks = 0
        self.number_of_loops = 0
        self.number_of_branching_blocks = 0
        self.number_of_join_blocks = 0
        keys = ['arithmetic', 'arithmetic_FP', 'memory', 'memory_FP',
                'compare', 'jump', 'call', 'ret', 'reg']
        self.instruction_types = {k: 0 for k in keys}
        self.operations = {'nop':0}

    def populate_features(self):
        for function in self.functions:
            self.number_of_blocks += len(function.blocks)
            for block in function.blocks:
                # print(block.loop_depth)
                # print(block.instruction_mnemonics)
                for key in block.instruction_types:
                    self.instruction_types[key] += block.instruction_types[key] #  * 10 ** block.loop_depth
                if block.number_of_successors > 1:
                    self.number_of_branching_blocks += 1
                if block.number_of_predecessors > 1:
                    self.number_of_join_blocks += 1
            for op in function.operations:
                if op not in self.operations:
                    self.operations[op] = 1
                else:
                    self.operations[op] += 1


class Function:
    def __init__(self, name, addr):
        self.name = name
        self.addr = addr
        self.blocks = []
        self.operations = []


class Block:
    def __init__(self, addr):
        self.addr = addr
        self.number_of_ins = 0
        self.instruction_mnemonics = []
        self.instruction_str = []
        keys = ['arithmetic', 'arithmetic_FP', 'memory', 'memory_FP',
                'compare', 'jump', 'call', 'ret', 'reg']
        self.instruction_types = {k: 0 for k in keys}
        self.looping_times = 0
        self.number_of_predecessors = 0
        self.number_of_successors = 0
        self.loop_depth = 0

    def classify_instructions(self):
        for ins in self.instruction_mnemonics:
            if ins in arithmetic_and_logic_op:
                self.instruction_types['arithmetic'] += 1
            if ins in memory_op:
                self.instruction_types['memory'] += 1
            if ins in arithmetic_and_logic_op_FP:
                self.instruction_types['arithmetic_FP'] += 1
            if ins in memory_op_FP:
                self.instruction_types['memory_FP'] += 1
            if ins in call_op:
                self.instruction_types['call'] += 1
            if ins in compare_op:
                self.instruction_types['compare'] += 1
            if ins in jmp_op:
                self.instruction_types['jump'] += 1
            if ins in ret_op:
                self.instruction_types['ret'] += 1

        for ins in self.instruction_str:
            for reg_values in x86_64_regs:
                if reg_values in ins:
                    self.instruction_types['reg'] += 1
                    break


graph_single = analyze_bin('bins/correlation/correlation_1023')
nx.write_gpickle(graph_single, "test.gpickle", 4)

g_new = nx.read_gpickle("test.gpickle")

for node in g_new.nodes:
    print(node)

