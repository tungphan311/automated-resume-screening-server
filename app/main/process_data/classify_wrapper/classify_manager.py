from app.main.process_data.classify_wrapper.domain_cached_model import DomainCachedModel
from app.main.process_data.classify_wrapper.domain_ontology import DomainOntology
from app.main.process_data.classifier.ontology import Ontology
from app.main.process_data.config import Config
from app.main.process_data.classifier.paper import Paper
from app.main.process_data.classifier.result import Result
from app.main.process_data.classifier.semanticmodule import Semantic as SemanticModule
from app.main.process_data.classifier.syntacticmodule import Syntactic as SyntacticModule


class ClassifyManager:
    """ 
    A simple manager for all different ontology-domains classifier. 

    The class name and method names was taken based on the origin CSO Classifier to respect their work.
    CSO Classifier Url: https://github.com/angelosalatino/cso-classifier
    """

    def __init__(self):
        # A dictionary for classifier.
        self.model_dict = dict()
        self.config = Config()
        self.supported_domains = self.config.get_supported_domains()

        # Todo: need optimize 
        for d in self.supported_domains:
            o_path = self.config.get_ontology_path(d)
            m_path = self.config.get_model_path(d)
            o = DomainOntology(o_path, d)
            m = DomainCachedModel(m_path, d)
            self.model_dict[d] = (o, m)


    def get_domain_model(self, domain):
        # free to crash for debugging.
        return self.model_dict[domain]


    def run_classifier(self, domain, job_description, modules='both', enhancement="first", explanation=False):
        """ Run the CSO Classifier.

            It takes as input the text from abstract, title, and keywords of a research paper and outputs a list of relevant
            concepts from CSO.

            This function requires the paper (please note, one single paper, no batch mode) and few flags: 
                (i) modules, determines whether to run only the syntactic module, or the semantic module, or both;
                (ii) enhancement, controls whether the classifier should infer super-topics, i.e., their first direct
                super-topics or the whole set of topics up until root.

            Args:
                domain (string): the domain name which is used for get matched the according ontology and model.

                job_description (string): contain raw text of job description.

                modules (string): either "syntactic", "semantic" or "both" to determine which modules to use when
                classifying. "syntactic" enables only the syntactic module. "semantic" enables only the semantic module.
                Finally, with "both" the classifier takes advantage of both the syntactic and semantic modules. Default =
                "both".

                enhancement (string): either "first", "all" or "no". With "first" the CSO classifier returns only the topics
                one level above. With "all" it returns all topics above the resulting topics. With "no" the CSO Classifier
                does not provide any enhancement.
                explanation (boolean): if true it returns the chunks of text that allowed to infer a particular topic. This feature
                of the classifier is useful as it allows users to asses the result

            Returns:
                class_res (dictionary): containing the result of each classification
        """

        if modules not in ["syntactic", "semantic", "both"]:
            raise ValueError("Error: Field modules must be 'syntactic', 'semantic' or 'both'")

        if enhancement not in ["first", "all", "no"]:
            raise ValueError("Error: Field enhances must be 'first', 'all' or 'no'")
        
        if type(explanation) != bool:
            raise ValueError("Error: Explanation must be set to either True or False")


        # Loading ontology and model
        (ontology, cached_model) = self.get_domain_model(domain)
        t_paper = Paper(job_description, modules)
        result = Result(explanation)


        # Passing parameters to the two classes (synt and sema) and actioning classifiers

        if modules == 'syntactic' or modules == 'both':
            synt_module = SyntacticModule(ontology, t_paper)
            result.set_syntactic(synt_module.classify_syntactic())
            if explanation: result.dump_temporary_explanation(synt_module.get_explanation())

        if modules == 'semantic' or modules == 'both':
            sema_module = SemanticModule(cached_model, ontology, t_paper)
            result.set_semantic(sema_module.classify_semantic())
            if explanation: result.dump_temporary_explanation(sema_module.get_explanation())

        result.set_enhanced(ontology.climb_ontology(getattr(result, "union"), enhancement))

        return result