import networkx as nx


def save_graph(G, name):
    nx.write_gexf(G, name + ".gexf")


def read_graph(name):
    return nx.read_gexf(name + ".gexf")

    # pickle.dump(G, open('graphs/' + name, 'w'))

    # g = cfg.graph
    # nx.draw(g)
