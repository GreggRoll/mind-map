import pydot
import os
import json

os.environ["PATH"] += os.pathsep + "C:\\Program Files\\Graphviz\\bin"

def lighten_color(base_color, amount):
    """
    Lighten the given color by the specified amount.
    """
    r = int(base_color[1:3], 16)
    g = int(base_color[3:5], 16)
    b = int(base_color[5:7], 16)
    
    r = min(255, r + amount)
    g = min(255, g + amount)
    b = min(255, b + amount)
    
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def add_nodes(graph, parent_name, child_dict, depth):
    """
    Recursively add nodes to the graph based on the JSON structure.
    """
    color = lighten_color("#6a7aa8", depth * 30)  # Start with a lighter blue (half blue, half white)
    for child_name, grandchild_dict in child_dict.items():
        child_node = pydot.Node(child_name, style="filled", fillcolor=color)
        graph.add_node(child_node)
        edge = pydot.Edge(parent_name, child_name)
        graph.add_edge(edge)
        
        add_nodes(graph, child_name, grandchild_dict, depth + 1)

def create_mind_map(data):
    graph = pydot.Dot(graph_type="graph", rankdir="TB", bgcolor="white", ranksep=2)
    
    graph.set_node_defaults(shape='ellipse', fontsize='12', height='0.5', width='0.75')
    graph.set_edge_defaults(len='3')
    
    root_name = list(data.keys())[0]
    root_node = pydot.Node(root_name, style="filled", fillcolor="#6a7aa8")  # Lighter shade of blue
    graph.add_node(root_node)
    
    add_nodes(graph, root_name, data[root_name], 1)  # Start with a depth of 1 for child nodes
    
    graph.write_png("mind_map.png", prog='twopi')
    os.startfile("mind_map.png")

with open("StartAGarden.json", "r") as file:
    data = json.load(file)
    
create_mind_map(data)