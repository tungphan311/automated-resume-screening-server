import sys

from networkx.algorithms import matching

sys.path.append("/Users/vinhpham/Desktop/automated-resume-screening-server")
sys.path.append("/Users/vinhpham/Desktop/automated-resume-screening-server/app")
sys.path.append("/Users/vinhpham/Desktop/automated-resume-screening-server/app/main")

from app.main.util.resume_extractor import ResumeExtractor, parse_pdf
from app.main.util.data_processing import tree_matching_score
from app.main.evaluation.prepare_data_evaluatation import parse_result
# from app.main.process_data.classify_wrapper.classify_manager import ClassifyManager
import json
import os
import pandas as pd

base_dir = os.path.dirname(os.path.realpath(__file__))
resumes_path = os.path.join(base_dir, 'data/resumes.csv')

def posts_path(domain):
    sub_path = "data/{domain}/{domain}_posts.csv".format(domain=domain)
    return os.path.join(base_dir, sub_path)

class Evaluation:
    def __init__(self, domain, domain_w, general_w, soft_w):
        self.domain = domain
        self.resumes = self.get_domain_resume_texts()
        self.posts = self.get_domain_job_posts()

        self.domain_w = domain_w
        self.general_w = general_w
        self.soft_w = soft_w

        self.results = {}

    def get_domain_resume_texts(self):
        df = pd.read_csv(resumes_path, delimiter="::delimiter::")
        df = df[df.domain == self.domain]
        return list(df['resume'])

    def get_domain_job_posts(self):
        df = pd.read_csv(posts_path(self.domain), delimiter="::delimiter::")
        df = df[0:5]
        return list(df['post'])

    def print_result(self):
        print("\n\n=Result for domain {domain}".format(domain=self.domain))
        print()
        for i in range(0, len(self.posts)):

            # TODO
            if i != 1: continue

            label_post = "JD-{i}: ".format(i=i)
            print("== List CV's score for {p} ==".format(p=label_post))

            infos = []
            for j in range(0, len(self.resumes)):

                # TODO
                # if j != 2 and j != 5: continue
                if j != 2: continue

                label_cv = "CV-{j}".format(j=j)
                p_text = self.posts[i]
                cv_text = self.resumes[j]

                domain_res = tree_matching_score(post_text=p_text, cv_text=cv_text, domain=self.domain)
                soft_res = tree_matching_score(post_text=p_text, cv_text=cv_text, domain='softskill')
                # general_res = tree_matching_score(post_text=p_text, cv_text=cv_text, domain='general')

                overall = domain_res['score'] * self.domain_w \
                    + soft_res['score'] * self.soft_w \
                    # + general_res['score'] * self.general_w

                print("\t" + label_cv + ":")
                print("\tDomain_matching_score: {score:.4f}".format(score=domain_res['score']))
                print("\tSoft_matching_score: {score:.4f}".format(score=soft_res['score']))
                # print("\tGeneral_matching_score: {score:.4f}".format(score=general_res['score']))
                print("\tOverall_matching_score: {score:.4f}".format(score=overall))
                print()

                cv_domain_res = parse_result(domain_res['cv_skills'])
                post_domain_res = parse_result(domain_res['post_skills'])
                # cv_general_res = parse_result(general_res['cv_skills'])
                # post_general_res = parse_result(general_res['post_skills'])
                cv_soft_res = parse_result(soft_res['cv_skills'])
                post_soft_res = parse_result(soft_res['post_skills'])

                res_dict = {
                    "domain": self.domain,
                    "post_index": i,
                    "cv_index": j,
                    "post_text": p_text,
                    "cv_text": cv_text,

                    "domain_w": self.domain_w,
                    "general_w": self.general_w,
                    "soft_w": self.soft_w, 
                    "overall_score": overall,

                    "domain_score": float(domain_res['score']),
                    "soft_score": float(soft_res['score']),
                    # "general_score": float(general_res['score']),

                    # "cv_domain_skills": cv_domain_res['all_skills'],
                    # "cv_soft_skills": cv_soft_res['all_skills'],
                    # "cv_general_skills": cv_general_res['all_skills'],

                    # "post_domain_skills": post_domain_res['all_skills'],
                    # "post_soft_skills": post_soft_res['all_skills'],
                    # "post_general_skills": post_general_res['all_skills'],
                    # "post_soft_explanation_skills": post_soft_res['explanation'],
                    # "cv_soft_explanation_skills": cv_soft_res['explanation'],
                }

                infos.append(res_dict)
            
            self.results[label_post] = infos

    def sort(self):
        for k, v in self.results.items():
            v.sort(key=lambda x: x.get('overall_score'), reverse=True)
            self.results[k] = v


# for lb in ['backend', 'frontend', 'android', 'ios', 'fullstack']:
for lb in ['frontend']:
    evaluation = Evaluation(lb, 3, 3, 1)
    evaluation.print_result()
    evaluation.sort()

    with open(os.path.join(base_dir, '{domain}_evaluation_result.json'.format(domain=lb)), 'w') as f:
        f.write(json.dumps(evaluation.results, indent=4))
