from backend.apps.utils.db import init_db
from flask import Flask
from flask_cors import CORS 
from backend.apps.routes.grievance_routes import grievance_bp
from backend.apps.routes.users_routes import user_bp

app = Flask(__name__)
CORS(app) 
# Initialize database
init_db(app)
app.register_blueprint(grievance_bp, url_prefix='/api/grievances')
app.register_blueprint(user_bp, url_prefix='/api/users')

if __name__ == '__main__':
    app.run(debug=True)
