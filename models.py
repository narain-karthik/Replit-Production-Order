from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Association table for many-to-many relationship between WorkCenter and Department
workcenter_department = db.Table('workcenter_department',
    db.Column('workcenter_id', db.Integer, db.ForeignKey('work_center.id'), primary_key=True),
    db.Column('department_id', db.Integer, db.ForeignKey('department.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    excel_access = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class WorkCenter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Many-to-many relationship with departments
    departments = db.relationship('Department', secondary=workcenter_department, back_populates='workcenters')
    
    def __repr__(self):
        return f'<WorkCenter {self.name}>'

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Many-to-many relationship with workcenters
    workcenters = db.relationship('WorkCenter', secondary=workcenter_department, back_populates='departments')
    
    def __repr__(self):
        return f'<Department {self.name}>'

class ProductionOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    production_order = db.Column(db.String(50), nullable=False)
    workcenter_id = db.Column(db.Integer, db.ForeignKey('work_center.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_type = db.Column(db.String(10), nullable=False)  # 'IN' or 'OUT'
    remark = db.Column(db.Text, nullable=True)  # New remark field
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    workcenter = db.relationship('WorkCenter', backref='production_orders')
    user = db.relationship('User', backref='production_orders')
    
    def __repr__(self):
        return f'<ProductionOrder {self.production_order} - {self.order_type}>'
