
from app.main.business.matching import Matcher
from app.main.business.job_post import JobPostBusiness
from app.main.business.candidate import CandidateBusiness


def candidatePipeline(resume_id):
    candidate_business = CandidateBusiness(resume_id)
    experience, domain = candidate_business.get_resume(resume_id)

    candidate_skill_dict, candidate_domain_skill_dict = candidate_business.get_candidate_skill_dict(experience, domain=domain)

    skill_graph = candidate_business.get_candidate_skill_graph(candidate_skill_dict)
    domain_skill_graph = candidate_business.get_candidate_skill_graph(candidate_domain_skill_dict)

    unique_skill = candidate_business.get_unique_skill(resume_id)

    return skill_graph, domain_skill_graph, unique_skill


def jobPipeline(job_id):
    job_post_business = JobPostBusiness(job_id)

    requirement, domain = job_post_business.get_job_jost(job_id)

    job_skill_dict, job_domain_skill_dict = job_post_business.get_job_skill_dict(requirement, domain)

    job_skill_graph = job_post_business.get_job_skill_graph(job_skill_dict)
    job_domain_skill_graph = job_post_business.get_job_skill_graph(job_domain_skill_dict)

    return job_skill_graph, job_domain_skill_graph
    

def OnetoOneMatching(resume_id, job_id):
    candidate_skill_graph, candidate_domain_skill_graph, candidate_unique_skill = candidatePipeline(resume_id)
    job_skill_graph, job_domain_skill_graph = jobPipeline(job_id)

    matching = Matcher(candidate_skill_graph, job_skill_graph)

    skill_match = matching.one2one_skill_match(candidate_skill_graph, job_skill_graph)
    domain_skill_match = matching.one2one_domain_skill_match(candidate_domain_skill_graph, job_domain_skill_graph) 

    return {
        "skill_match": skill_match,
        "domain_skill_match": domain_skill_match
    }

