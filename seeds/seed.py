from app.main.model.activity_model import ActivityTypeModel, ActivityParameterModel
import json

def seed_data(db):
    activities = ActivityTypeModel.query.all()
    if len(activities) == 0:
        with open('seeds/activities.json') as json_file:
            data = json.load(json_file)

            for act_type in data:
                new_type = ActivityTypeModel(id=act_type['id'], name=act_type['name'], description=act_type['description'])
                db.session.add(new_type)

        db.session.commit()


    params = ActivityParameterModel.query.all()
    if len(params) == 0:
        with open('seeds/activity_parameters.json') as json_file:
            data = json.load(json_file)

            for param in data:
                act_param = ActivityParameterModel(id=param['id'], name=param['name'])
                db.session.add(act_param)

        db.session.commit()