from app.main import classify_manager as cm
import networkx as nx

class JobDataProcessing:
    def __init__(self, requirement):
        self.requirement = requirement


    def get_skill_ontologies(self, requirement, domain = 'general'):
        generate_skill_link = {}

        prepareText = {'keywords':"data mining, computer science"}
        prepareText['abstract'] = requirement

        result = cm.run_classifier(domain, prepareText, explanation=True).get_dict()

        generate_skill_link['union'] = result['union']
        generate_skill_link['explanation'] = result['explanation']

        return generate_skill_link

