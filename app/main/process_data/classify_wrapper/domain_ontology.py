import pickle
from app.main.process_data.classifier.ontology import Ontology


class DomainOntology(Ontology):
    """ 
    A simple subclass of Ontology.
    This class helps create the specified ontology from the existent path.
    """

    def __init__(self, domain_ontology_pickle_path, domain_name):
        super().__init__(load_ontology=False)
        self.domain_ontology_pickle_path = domain_ontology_pickle_path
        self.domain_name = domain_name
        self.load_domain_ontology()

    
    def load_domain_ontology(self):
        """ Function that loads the domain ontology from the pickle file. 
        This file has been serialised using Pickle allowing to be loaded quickly.
        """
        ontology = pickle.load(open(self.domain_ontology_pickle_path, 'rb'))
        self.from_cso_to_single_items(ontology)
        # print("{domain_name} ontology has been loaded.".format(domain_name=self.domain_name))