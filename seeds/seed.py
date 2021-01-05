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
