import networkx as nx
import os


def render_graph(graph, output_dir):
    name = graph.name
    draw_graphviz_image(graph, name, output_dir)


def create_graph_with_all_dsos(dso_map, name):
    graph = nx.DiGraph(name=name)
    for dso_relation in dso_map.get_all_relations():
        num_symbols = len(dso_relation.symbols)
        if num_symbols:
            graph.add_edge(dso_relation.from_dso,
                           dso_relation.to_dso,
                           label=num_symbols,
                           weight=num_symbols)
    return graph


def render_graph_for_every_dso(relationships, output_dir):
    for dso, relations in relationships.get_relations_for_every_single_dso().items():

        nxgraph = create_graph_for_dso(dso, relations)

        draw_graphviz_image(nxgraph, dso, output_dir)


def create_graph_for_dso(dso, relations):
    nxgraph = nx.DiGraph(name=dso)
    relations = list(relations)
    relations.sort()
    for relation in relations:
        num_symbols = len(relation.symbols)
        if num_symbols > 0:
            nxgraph.add_edge(relation.from_dso,
                             relation.to_dso,
                             weight=num_symbols,
                             label=num_symbols)
    return nxgraph


def draw_graphviz_image(nxgraph, name, output_dir):
    engine = "neato"
    agraph = nx.drawing.nx_agraph.to_agraph(nxgraph)
    agraph.graph_attr.update(fontsize=100, nodesep=1, overlap="scale", rankdir="tb", ranksep=2, splines=True)
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    base_file_name = os.path.join(output_dir, f'dsos.{name}.{engine}')
    agraph.write(f"{base_file_name}.gv")
    agraph.draw(f"{base_file_name}.svg", prog=engine)


def create_relationship_graphs(relationships, output_dir):
    graph = create_graph_with_all_dsos(relationships, "all")
    render_graph(graph, output_dir)
    render_graph_for_every_dso(relationships, output_dir)
