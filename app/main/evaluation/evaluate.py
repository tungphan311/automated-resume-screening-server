import sys

from numpy.core.einsumfunc import _einsum_path_dispatcher
sys.path.append("/Users/vinhpham/Desktop/automated-resume-screening-server")
sys.path.append("/Users/vinhpham/Desktop/automated-resume-screening-server/app")
sys.path.append("/Users/vinhpham/Desktop/automated-resume-screening-server/app/main")

from app.main.util.resume_extractor import ResumeExtractor, parse_pdf
from app.main.process_data.classify_wrapper.classify_manager import ClassifyManager
import json
import os


base_dir = os.path.dirname(os.path.realpath(__file__))

class Evaluation:

    def __init__(self):
        self.classifier = ClassifyManager()


    ##################
    # HELPERS
    ##################
    # dict_keys(['syntactic', 'semantic', 'union', 'enhanced', 'explanation'])
    def extract(self, domain, doc):
        domain_result = self.classifier.run_classifier(domain=domain, explanation=True, job_description=doc)
        general_result = self.classifier.run_classifier(domain='general', explanation=True, job_description=doc)
        softskill_result = self.classifier.run_classifier(domain='softskill', explanation=True, job_description=doc)
        return {
            'domain': self.parse_result(domain_result),
            'general': self.parse_result(general_result),
            'softskill': self.parse_result(softskill_result),
        }

    def parse_result(self, result):
        dict_result = result.get_dict()
        all_skills = set(dict_result['union'])
        explicit_skills = set(dict_result['syntactic'])
        related_skills = all_skills.difference(explicit_skills)
        return {
            'explicit_skills': list(explicit_skills),
            'related_skills': list(related_skills),
            'all_skills': list(all_skills),
            'explanation': dict_result['explanation']
        }


####################
# Create resume csv
####################

def parse_cv(local_path):
    "Return text."
    result_dict = parse_pdf(local_path, True)
    return result_dict

PDF_PATH = 'data/{domain}/cv/{domain}/{domain}-{index}/{domain}-{index}.pdf'
DELIMITER = '::delimiter::'

with open(os.path.join(base_dir, 'resumes_3.csv'), 'w') as f:
    f.write(DELIMITER.join(['index', 'domain', 'resume']))
    f.write('\n')
    j = 0
    for domain in ['android', 'fullstack']:
        for i in range(1, 11):
            j += 1
            print('parsing {domain}: {i}, index {j}'.format(domain=domain, i=i, j=j))
            sub_path = PDF_PATH.format(domain=domain, index=i)
            pdf_path = os.path.join(base_dir, sub_path)
            sentences = parse_cv(pdf_path)
            text = '. '.join(sentences).replace('\n', '. ')
            f.write(DELIMITER.join([str(j), domain, text]))
            f.write('\n')

print("Done")
# res = parse_cv(ios_path)
# with open(os.path.join('app/main/evaluation/evaluation_result.json'), 'w') as f:
#     f.write(json.dumps(res, indent=4))