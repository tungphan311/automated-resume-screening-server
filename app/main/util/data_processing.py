from app.main import classify_manager as cm
import networkx as nx


def get_technical_skills(domain, text):
    """
    Use classify_manager to extract skill from text.
    Return: 
        (skills, explanation)
        skills: array.
        explanation: dictionary.
    """

    if domain not in cm.supported_domains:
        print("Request to extract the unsupported domain.")
        raise ValueError("Unsupported domain.")
    
    prepare_text = {'keywords':"data mining, computer science"}
    prepare_text['abstract'] = text
    
    result_dict = cm.run_classifier(domain, prepare_text, explanation=True).get_dict()
    skills = result_dict['union']
    explanation = result_dict['explanation']

    # Convert to string
    skills = [str(s) for s in skills]

    return (skills, explanation)

def generate_edges(graph):
    edges = [] 
    # for each node in graph 
    for node in graph: 
        # for each neighbour node of a single node 
        for neighbour in graph[node]: 
            # if edge exists then append 
            edges.append((node, neighbour)) 
    return edges

def generate_skill_graph(edges):
    G2 = nx.Graph()
    G2.add_edges_from(edges)
    return G2