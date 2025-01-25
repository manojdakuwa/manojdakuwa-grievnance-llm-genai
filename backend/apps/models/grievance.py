from backend.apps.utils.db import db

class Grievance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('grievance.id'), nullable=True)
    assignments = db.relationship('Assignment', backref='grievance', lazy=True)

class GRO(db.Model):
    gro_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)

class Assignment(db.Model):
    assignment_id = db.Column(db.Integer, primary_key=True)
    grievance_id = db.Column(db.Integer, db.ForeignKey('grievance.id'), nullable=False)
    gro_id = db.Column(db.Integer, db.ForeignKey('gro.gro_id'), nullable=False)
