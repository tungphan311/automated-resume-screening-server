import json
import os


class Config:
    """ A simple abstraction layer for the configuration file """

    ONTOLOGY_KEY = "ontology_path"
    MODEL_KEY = "cached_model_path"

    def __init__(self, paper = None):
        """ Initialising the config class """
        self.dir = os.path.dirname(os.path.realpath(__file__))
        self.config_file = os.path.join(self.dir, "config.json")
        self.config_json = json.load(self.config_file)
        self.read_config_file()

    def get_ontology_path(self, domain):
        path = self.config_json[self.ONTOLOGY_KEY][domain]
        return os.path.join(self.dir, path)

    def get_model_path(self, domain):
        path = self.config_json[self.MODEL_KEY][domain]
        return os.path.join(self.dir, path)

    def get_supported_domains(self):
        return [v for (_, v) in self.config_json[self.ONTOLOGY_KEY].items()]
