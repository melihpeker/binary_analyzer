import angr
from angr.analyses.loop_analysis import LoopAnalysis
import csv
from angrutils import *
import numpy as np
from anytree import Node, RenderTree


arithmetic_and_logic_op = {'add', 'sub', 'mul', 'inc', 'dec', 'imul', 'idiv', 'and', 'or', 'xor', 'not', 'neg', 'shl',
                        'shr'}

arithmetic_and_logic_op_FP = {'addss', 'subss', 'mulss', 'incss', 'decss', 'imulss', 'idivss'}

compare_op = {'cmp'}

memory_op = {'mov', 'push', 'pop', 'lea'}

memory_op_FP = {'movss', 'pushss', 'popss', 'leass'}


jmp_op = {
    ' ', 'ja', 'jae', 'jb', 'jbe', 'jc', 'jcxz', 'jecxz', 'jrcxz', 'je', 'jg', 'jge', 'jl', 'jle', 'jna',
    'jnae', 'jnb', 'jnbe', 'jnc', 'jne', 'jng', 'jnge', 'jnl', 'jnle', 'jno', 'jnp', 'jns', 'jnz', 'jo', 'jp',
    'jpe', 'jpo', 'js', 'jz'
}

call_op = {
    'call'
}

ret_op = {
    'ret'
}

x86_64_regs = {
    'al', 'ah', 'bl', 'bh', 'cl', 'ch', 'dl', 'dh', 'spl', 'bpl', 'sil', 'dil',
    'ax', 'bx', 'cx', 'dx', 'sp', 'bp', 'si', 'di',
    'eax', 'ebx', 'ecx', 'edx', 'esp', 'ebp', 'esi', 'edi',
    'rax', 'rdx', 'rcx', 'rdx', 'rsp', 'rbp', 'rsi', 'rdi',
    'r8b', 'r9b', 'r10b', 'r11b', 'r12b', 'r13b', 'r14b', 'r15b',
    'r8w', 'r9w', 'r10w', 'r11w', 'r12w', 'r13w', 'r14w', 'r15w',
    'r8d', 'r9d', 'r10d', 'r11d', 'r12d', 'r13d', 'r14d', 'r15d',
    'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15',
    'cs', 'ss', 'ds', 'es', 'fs', 'gs',
    'ecs', 'ess', 'eds', 'ees', 'efs', 'egs',
    'rcs', 'rss', 'rds', 'res', 'rfs', 'rgs'
}


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
    def __init__(self, id, addr):
        self.id = id
        self.addr = addr
        self.number_of_ins = 0
        self.instruction_mnemonics = []
        self.instruction_str = []
        self.keys = ['arithmetic', 'arithmetic_FP', 'memory', 'memory_FP',
                'compare', 'jump', 'call', 'ret', 'reg']
        self.instruction_types = {k: 0 for k in self.keys}
        self.looping_times = 0
        self.number_of_predecessors = 0
        self.number_of_successors = 0
        self.loop_depth = 0
        feature_keys = ['arithmetic', 'arithmetic_FP', 'memory', 'memory_FP',
                'compare', 'jump', 'call', 'ret', 'reg', 'number_of_ins',
                        'number_of_predecessors', 'number_of_successors', 'loop_depth']
        self.features = {k: 0 for k in feature_keys}

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

    def create_feature_dict(self):
        for key in self.keys:
            self.features[key] = self.instruction_types[key]
        self.features['number_of_ins'] = self.number_of_ins
        self.features['number_of_predecessors'] = self.number_of_predecessors
        self.features['number_of_successors'] = self.number_of_successors
        # self.features['looping_times'] = self.looping_times
        self.features['loop_depth'] = self.loop_depth


class Loop:
    def __init__(self, name, info, depth):
        self.name = name
        self.info = info
        self.depth = depth


def find_subloop(loops, loop, node, depth):
    for sub_loop in loop.subloops:
        depth = depth + 1
        #  print("Loop name " + str(sub_loop))
        curr_loop = Loop(sub_loop.entry.addr, sub_loop, depth)
        loops.append(curr_loop)
        current_node = Node(sub_loop.entry.addr, parent=node)
        find_subloop(loops, sub_loop, current_node, depth)


def extract_operations(function_obj, function):
    try:
        instructions = function.operations
        for ins in instructions:
            function_obj.operations.append(ins)
    except angr.errors.SimTranslationError:
        print('Unable to translate bytecode for function ' + str(function))


def extract_function_instructions(block_id, function):
    all_blocks = []
    new_function = Function(function.name, function.addr)
    for block in function.blocks:
        all_blocks.append(block)

    for block in all_blocks:
        new_block = Block(block_id, block.addr)
        block_id = block_id + 1
        try:
            new_block.number_of_ins = block.instructions
            for ins in block.disassembly.insns:
                new_block.instruction_mnemonics.append(ins.mnemonic)
                new_block.instruction_str.append(ins.op_str)
        except angr.errors.SimTranslationError:
            print("Unable to translate bytecode for block " + str(block.addr))
        new_block.classify_instructions()
        new_function.blocks.append(new_block)

    return new_function


def extract_pred_succ_info(cfg, function):
    for block in function.blocks:
        node = cfg.get_any_node(block.addr)
        if node:
            block.looping_times = node.looping_times
            block.number_of_predecessors = len(node.predecessors)
            block.number_of_successors = len(node.successors)

    return True


def extract_looping_info(loops, function):
    for block in function.blocks:
        for loop in loops:
            for node in loop.info.body_nodes:
                if block.addr == node.addr:
                    block.loop_depth = loop.depth

    return True


def analyze_bin(name):
    # name = "atax_base"
    proj = angr.Project(name, load_options={'auto_load_libs': False})
    cfg = proj.analyses.CFGEmulated(fail_fast=True)
    # cfg_fast = proj.analyses.CFGFast()

    proj.analyses.Disassembly()

    # Loop analysis
    lf = proj.analyses.LoopFinder()
    # print(lf.loops_hierarchy)

    sub_loops = []
    loops = []
    main = Node("main")

    for loop in lf.loops:
        nested_loop = False
        for my_loop in loops:
            if loop.entry.addr == my_loop.name:
                nested_loop = True
                break
        if not nested_loop:
            # print("Loop name " + str(loop))
            curr_loop = Loop(loop.entry.addr, loop, 1)
            current_node = Node(loop.entry.addr, parent=main)
            loops.append(curr_loop)
            find_subloop(loops, loop, current_node, 1)

    # for pre, fill, node in RenderTree(main):
    #     print("%s%s" % (pre, node.name))

    # for loop in loops:
        # print("Loop entry address: " + str(loop.name) + " Depth: " + str(loop.depth))
        #print("\tNumber of blocks inside: " + str(len(loop.info.body_nodes)))
        # for block_node in loop.info.body_nodes:
        #     block = proj.factory.block(block_node.addr)
        #     print(block.pp())


    ######################### Block analysis #########################
    functions = []
    function_block_lens = []
    cfg.kb.functions.values()
    block_id = 0
    for function in cfg.kb.functions.values():
        try:
            function_obj = extract_function_instructions(block_id, function)
            extract_pred_succ_info(cfg, function_obj)
            extract_looping_info(loops, function_obj)
            extract_operations(function_obj, function)
            functions.append(function_obj)
            function_block_lens.append(len(function.block_addrs))
        except:
            print("Skipping function..")

    file = Bin(name, functions)
    file.number_of_loops = len(loops)
    file.populate_features()

    for function in functions:
        # print("----------------------")
        for block in function.blocks:
            # print(block.loop_depth)
            # print(block.instruction_mnemonics)
            for key in block.instruction_types:
                # block.instruction_types[key] *= 10**block.loop_depth
                block.create_feature_dict()
            # print(block.instruction_types)

    G = cfg.graph
    cfg_nodes = []
    cfg_edges = []
    all_blocks = []
    new_edges = []
    for node in G.nodes:
        cfg_nodes.append(node)
    for edge in G.edges:
        cfg_edges.append(edge)

    for function in file.functions:
        for block in function.blocks:
            all_blocks.append(block)

    index = 0
    attrs = {block.addr: {} for block in all_blocks}
    for edge in G.edges:
        new_edge = []
        for block in all_blocks:
            if block.addr == edge[0].addr:
                new_edge.append(block.addr)
                attrs[block.addr] = block.features
                break
        for block in all_blocks:
            if block.addr == edge[1].addr:
                new_edge.append(block.addr)
                attrs[block.addr] = block.features
                break
        if len(new_edge) == 2:
            new_edges.append(new_edge)

    G_new = nx.DiGraph()
    G_new.add_edges_from(new_edges)
    nx.set_node_attributes(G_new, attrs)

    # index_max = np.argmax(np.asarray(function_block_lens))
    # biggest_function = functions[index_max]

    # start_state = proj.factory.blank_state(addr=proj.entry)
    # plot_cfg(cfg, name, asminst=True, remove_imports=True, remove_path_terminator=True)

    return G_new


def write_edges_to_csv(G, id, csv_file):
    node_ids = {}
    node_index = 0
    for node in G.nodes:
        node_ids[node] = node_index
        node_index = node_index + 1

    rows = []
    for edge in G.edges:
        row = [id]
        row.append(node_ids[edge[0]])
        row.append(node_ids[edge[1]])
        rows.append(row)

    with open(csv_file, 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header
        for row in rows:
            writer.writerow(row)


def write_features_to_csv(G, id, csv_file):
    node_ids = {}
    node_index = 0
    for node in G.nodes:
        node_ids[node] = node_index
        node_index = node_index + 1

    rows = []
    for node in G.nodes:
        row = [id, node_ids[node]]
        for key in G.nodes._nodes[node]:
            row.append(G.nodes._nodes[node][key])
        rows.append(row)

    with open(csv_file, 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header
        for row in rows:
            writer.writerow(row)
