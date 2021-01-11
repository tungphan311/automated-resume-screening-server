from app.main.util.data_processing import generate_edges, generate_skill_graph
from app.main.service.data_processing.job_post import JobDataProcessing
from app.main.model.job_post_model import JobPostModel

class JobPostBusiness:
    def __init__(self, job_id):
        self.job_id = job_id

    def get_job_jost(self, job_id):
        job_post = JobPostModel.query.get(job_id)

        requirement = job_post.requirement_text
        domain = job_post.job_domain.alternative_name

        return requirement, domain

    def get_job_skill_dict(self, requirement, domain):
        job_data_processing = JobDataProcessing(requirement)
        job_skill_dict = job_data_processing.get_skill_ontologies(requirement)
        job_domain_skill_dict = job_data_processing.get_skill_ontologies(requirement, domain=domain)

        return job_skill_dict, job_domain_skill_dict

    
    def get_job_skill_graph(self, job_skill_dict):
        skill_edges = generate_edges(job_skill_dict['explanation'])
        return generate_skill_graph(skill_edges)

    