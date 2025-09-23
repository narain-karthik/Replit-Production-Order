import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def get_database_uri():
    """Get database URI - PostgreSQL primary, with SQL Server and MySQL support"""

    # PostgreSQL (primary database)
    postgres_url = os.environ.get("DATABASE_URL")
    if postgres_url:
        return postgres_url

    # Fallback to SQLite for development if no DATABASE_URL is set
    return "sqlite:///production_order_tracking.db"

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET" , "1010")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models and routes
    import models
    import routes
    
    # Create all tables
    db.create_all()
    
    # Create default admin user if not exists
    from models import User, WorkCenter, Department
    from werkzeug.security import generate_password_hash
    
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User()
        admin_user.username = 'admin'
        admin_user.password_hash = generate_password_hash('admin123')
        admin_user.is_admin = True
        db.session.add(admin_user)
    
    # Create default workcenters if not exist
    if WorkCenter.query.count() == 0:
        default_workcenters = ['WC001 - Assembly', 'WC002 - Machining', 'WC003 - Welding', 'WC004 - Painting', 'WC005 - Quality Control']
        for wc_name in default_workcenters:
            workcenter = WorkCenter()
            workcenter.name = wc_name
            db.session.add(workcenter)
    
    # Create default departments if not exist
    if Department.query.count() == 0:
        default_departments = ['Engineering', 'Production', 'Quality Control', 'Maintenance', 'Operations', 'Management']
        for dept_name in default_departments:
            department = Department()
            department.name = dept_name
            db.session.add(department)
    
    db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
