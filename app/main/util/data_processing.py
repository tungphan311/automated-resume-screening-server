from app.main import classify_manager as cm
import networkx as nx
import gmatch4py as gm
from numpy import linalg as LA
import numpy as np


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


def matching_score(post_text, cv_text, domain):
    """
    Return:
    {
        'score': float
        'cv_explanation': dict
        'post_explanation': dict
    }
    
    """
    post_skills = __get_skills_by_classifier(post_text, domain)
    cv_skills = __get_skills_by_classifier(cv_text, domain)

    post_graph = generate_skill_graph(generate_edges(post_skills['explanation']))
    cv_graph = generate_skill_graph(generate_edges(cv_skills['explanation']))

    score = _matching(post_graph, cv_graph)

    if not cv_skills['explanation'] or not post_skills['explanation']:
        score = 0

    DECIMAL_LENGTH = 4
    return {
        "score": np.round(score, DECIMAL_LENGTH),
        "cv_explanation": cv_skills['explanation'],
        "post_explanation": post_skills['explanation'],
        "post_graph": post_graph,
        "cv_graph": cv_graph,
        
        "cv_skills": cv_skills,
        "post_skills": post_skills,
    }
    

def __get_skills_by_classifier(text, domain):
    generate_skill_link = {}
    result = cm.run_classifier(domain, text, explanation=True).get_dict()
    generate_skill_link['union'] = result['union']
    generate_skill_link['explanation'] = result['explanation']
    generate_skill_link['syntactic'] = result['syntactic']
    generate_skill_link['semantic'] = result['semantic']
    return generate_skill_link

def _matching(post_graph, cv_graph):
        # all edit cost are equal to 1
        ged = gm.GraphEditDistance(1, 1, 1, 1)
        result = ged.compare([post_graph, cv_graph], None)
        # description how much score is and why it got matched
        return LA.norm(ged.similarity(result))