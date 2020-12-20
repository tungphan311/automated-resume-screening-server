from sqlalchemy.orm import backref
from .. import db
from datetime import datetime


class ActivityTypeModel(db.Model):
    __tablename__ = "activity_types"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    activities = db.relationship('ActivityModel', backref='activity_type', lazy=True)


class ActivityParameterModel(db.Model):
    __tablename__ = "activity_parameters"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    action_details = db.relationship('ActivityDetailModel', backref='activity_parameter', lazy=True)


class ActivityModel(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    activity_type_id = db.Column(db.Integer, db.ForeignKey(ActivityTypeModel.id), nullable=False)

    activity_detail = db.relationship('ActivityDetailModel', uselist=False, backref='activity')


class ActivityDetailModel(db.Model):
    __tablename__ = "activity_details"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_id = db.Column(db.Integer, db.ForeignKey(ActivityModel.id), nullable=False)
    
    activity_parameter_id = db.Column(db.Integer, db.ForeignKey(ActivityParameterModel.id), nullable=False)
    value = db.Column(db.Integer, nullable=False)
