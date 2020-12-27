from app.main.util.data_processing import generate_edges, generate_skill_graph
from app.main.service.data_processing.candidate import CandidateDataProcessing
from app.main.model.resume_model import ResumeModel
import re


class CandidateBusiness:
    def __init__(self, resume_id):
        self.resume_id = resume_id

    def get_resume(self, resume_id):
        resume = ResumeModel.query.get(resume_id)

        experience = resume.experiences
        skills = resume.technical_skills
        skills = re.sub(r"|", ", ", skills)

        domain = resume.job_domain.alternative_name

        return experience + " " + skills, domain

    def get_unique_skill(self, resume_id):
        resume = ResumeModel.query.get(resume_id)
        skills = resume.technical_skills
        skills = skills.split("|")

        return skills

    def get_candidate_skill_dict(self, experience, domain):
        candidate_data_processing = CandidateDataProcessing(experience)

        candidate_skill_dict = candidate_data_processing.get_skills_ontologies(experience)
        candidate_domain_skill_dict = candidate_data_processing.get_skills_ontologies(experience, domain=domain)

        return candidate_skill_dict, candidate_domain_skill_dict

    def get_candidate_skill_graph(self, candidate_skill_dict):
        skill_edges = generate_edges(candidate_skill_dict['explanation'])

        return generate_skill_graph(skill_edges)

        