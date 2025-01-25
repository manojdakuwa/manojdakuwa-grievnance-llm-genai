from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy()
migrate = Migrate()
def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grievances.db'
    db.init_app(app)
    migrate.init_app(app, db)
    # Import models here to ensure they are registered with SQLAlchemy
    from backend.apps.models.grievance import Grievance, GRO, Assignment
    from backend.apps.models.users import User
    with app.app_context():
        db.create_all()
