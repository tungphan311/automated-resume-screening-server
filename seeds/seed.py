from app.main.model.major_model import MajorModel
from app.main.model.job_domain_model import JobDomainModel
import json

def seed_data(db):
    domains = JobDomainModel.query.all()
    if (len(domains)) == 0:
        with open('seeds/domains.json') as json_file:
            data = json.load(json_file)

            for domain in data:
                d = JobDomainModel(id=domain['id'], name=domain['name'], alternative_name=domain['alternative_name'])
                db.session.add(d)

        db.session.commit()

    majors = MajorModel.query.all()
    if (len(majors)) == 0:
        with open('seeds/majors.json', encoding="utf-8") as json_file:
            data = json.load(json_file)

            for domain in data:
                d = MajorModel(name=domain['name'])
                db.session.add(d)

        db.session.commit()