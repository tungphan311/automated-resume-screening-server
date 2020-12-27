import gmatch4py as gm
from numpy import linalg as LA

class Matcher:
    def __init__(self, G_candidate = None, G_job_post = None):
        self.G_candidate = G_candidate
        self.G_job_post = G_job_post

    def one2one_skill_match(self, G_candidate, G_job_post):
        # all edit cost are equal to 1
        ged = gm.GraphEditDistance(1, 1, 1, 1)
        result = ged.compare([G_candidate, G_job_post], None)

        # description how much score is and why it got matched
        return LA.norm(ged.similarity(result))


    def one2one_domain_skill_match(self, G_candidate_domain, G_job_post_domain):
        # all edit cost are equal to 1
        ged = gm.GraphEditDistance(1, 1, 1, 1)
        result = ged.compare([G_candidate_domain, G_job_post_domain], None)

        # description how much score is and why it got matched
        return LA.norm(ged.similarity(result))

