
import json
from app.main.process_data.classifier.model import Model


class DomainCachedModel(Model):
    """
    A simple subclass of Model.
    This class helps load and store cached model associated with the specified ontology.
    """

    def __init__(self, domain_model_pickle_path, domain_name):
        super().__init__(load_model=False)
        self.domain_model_pickle_path = domain_model_pickle_path
        self.domain_name = domain_name
        self.load_cached_domain_model()


    def load_cached_domain_model(self):
        """Function that loads the cached Word2vec model for the according ontology.
        The ontology file has been serialised with Pickle. 
        The cached model is a json file (dictionary) containing all words in the corpus vocabulary with the corresponding CSO topics.
        The latter has been created to speed up the process of retrieving CSO topics given a token in the metadata
        """
        with open(self.domain_model_pickle_path) as f:
           self.model = json.load(f)
        print("Model {name} has bene loaded.".format(name=self.domain_name))



