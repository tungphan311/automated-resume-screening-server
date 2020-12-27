from app.main import classify_manager as cm
import networkx as nx

class CandidateDataProcessing:
    def __init__(self, experience):
        self.experience = experience

    def get_skills_ontologies(self, experience, domain = "general"):
        generate_skill_link = {}

        prepareText = {'keywords':"data mining, computer science"}
        prepareText['abstract'] = experience

        result = cm.run_classifier(domain, prepareText, explanation=True).get_dict()

        generate_skill_link['union'] = result['union']
        generate_skill_link['explanation'] = result['explanation']

        return generate_skill_link
