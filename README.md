# Production Order Tracking System

Comprehensive Flask-based web application for tracking production orders in manufacturing environments, optimized for PostgreSQL with role-based access control and advanced Excel export capabilities.

## Overview

The Production Order Tracking System uses a modern relational database architecture with **4 core tables** supporting user management, work center definitions, department organization, and comprehensive production order lifecycle tracking. Designed for PostgreSQL primary deployment with IST timezone display and optimized for Replit environment.

**Database Tables:**
1. **user** - User authentication, profile management, and Excel access permissions
2. **work_center** - Production facility definitions and work center management
3. **department** - Organizational unit definitions and structure
4. **production_order** - Core production order lifecycle with IN/OUT tracking and balance calculations
5. **workcenter_department** - Many-to-many relationship table linking work centers to departments

## Features

### **Core Functionality**
- **Production Order Management**: Record and track incoming (IN) and outgoing (OUT) production orders with balance calculations
- **Work Center Integration**: Multi-work center support with department-based filtering and dedicated tracking per facility
- **Role-Based Access Control**: Three-tier system (Regular User, Excel Access User, and Administrator)
- **Department-Based Access**: Users only see work centers assigned to their department, reducing interface complexity
- **Balance Reporting**: Real-time balance calculations showing IN/OUT quantities and current balance per work center
- **Real-time Reporting**: Generate comprehensive reports with filtering and export capabilities
- **Excel Export with Permissions**: Professional Excel export with granular access control and department-based filtering
- **Search and Filtering**: Advanced search capabilities across all production data

### **Excel Access Management**
- **Granular Permissions**: Admin can grant/revoke Excel export access per user
- **Department Filtering**: Users with Excel access see only their department's data (unless admin)
- **Professional Formatting**: Excel exports include headers, styling, and proper data formatting
- **Multiple Worksheets**: Production Orders and Balance Report in separate sheets
- **Access Indicators**: Visual badges showing Excel access status in user management

### **User Management**
- **Authentication**: Secure session-based login with password hashing
- **User Profiles**: Department assignment, role management, and Excel access control
- **Department-Based Access**: Users see only work centers assigned to their department
- **Admin Functions**: User management, work center configuration, department assignment, Excel access control, and system administration
- **Auto-provisioning**: Default admin user, work center, and department creation on first startup

### **Responsive Design**
- **Bootstrap 5**: Professional dark theme interface
- **Mobile Optimized**: Responsive design that works on all devices
- **Font Awesome Icons**: Consistent iconography throughout the application
- **Modern UI/UX**: Clean, intuitive interface designed for manufacturing environments
- **Conditional UI**: Excel download buttons appear only for users with appropriate permissions

## Quick Start

### **Replit Environment (Recommended)**

1. **Automatic Setup**: Database and dependencies are automatically configured
2. **Default Login**: 
   - **Username**: admin
   - **Password**: admin123
3. **Access Application**: Click the "Run" button and open the web preview
4. **Excel Access**: Admin users automatically have Excel export access

### **Local Development**

1. **Prerequisites**: Python 3.11+, PostgreSQL 15+
2. **Database Setup**: See [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) for detailed setup
3. **Environment Variables**:
   ```bash
   DATABASE_URL=postgresql://username:password@localhost:5432/production_orders
   SESSION_SECRET=your-secure-random-key-here
   ```
4. **Installation**: Dependencies managed through `pyproject.toml`
5. **Run Application**: `python main.py` or `gunicorn app:app`

## System Architecture

### **Backend Architecture**
- **Web Framework**: Flask with modular structure separating routes, models, and configuration
- **Database ORM**: SQLAlchemy with declarative base for robust database operations
- **Authentication**: Session-based authentication with Werkzeug password hashing
- **File Structure**: 
  - `app.py`: Application factory and configuration
  - `models.py`: Database models and relationships
  - `routes.py`: URL routing and request handling
  - `main.py`: Application entry point

### **Frontend Architecture**
- **Template Engine**: Jinja2 templates with Flask for server-side rendering
- **UI Framework**: Bootstrap 5 with professional dark theme
- **Icons**: Font Awesome 6.4.0 for consistent iconography
- **Client-side**: Vanilla JavaScript for form validation and UI interactions

### **Data Storage**
- **Database**: SQLAlchemy ORM with PostgreSQL backend (configurable via DATABASE_URL)
- **Connection Management**: Connection pooling with automatic reconnection and health checks
- **Data Integrity**: Foreign key constraints and comprehensive validation
- **Performance**: Strategic indexing and query optimization
- **Timezone**: All timestamps displayed in Indian Standard Time (IST) for user convenience

## Database Schema

### **Core Models**

#### **Users (`user`)**
- User authentication and role management
- Department assignment and profile information
- Admin privileges and Excel export access control
- Account status and creation tracking

#### **Work Centers (`work_center`)**
- Production facility definitions
- Active/inactive status management
- Creation and modification tracking

#### **Departments (`department`)**
- Organizational structure definitions
- Department-based user organization
- Administrative configuration

#### **Production Orders (`production_order`)**
- Core order tracking with IN/OUT types
- Work center assignment and user attribution
- Quantity tracking and timestamp management (displayed in IST)
- Complete audit trail with relationships

For detailed database schema, see [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)

## Default Configuration

### **Default Admin User**
- **Username**: admin
- **Password**: admin123
- **Role**: Administrator
- **Excel Access**: Enabled by default
- **Access**: Full system administration

*⚠️ Important: Change default password after first login*

### **Default Work Centers**
- WC001 - Assembly
- WC002 - Machining  
- WC003 - Welding
- WC004 - Painting
- WC005 - Quality Control

### **Default Departments**
- Engineering
- Production
- Quality Control
- Maintenance
- Operations
- Management

## Technology Stack

### **Backend Technologies**
- **Flask 3.1.2**: Modern web framework with excellent performance
- **SQLAlchemy 2.0.43**: Advanced ORM with relationship management
- **PostgreSQL**: Enterprise-grade relational database
- **Werkzeug 3.1.3**: Security utilities and password hashing
- **Gunicorn 23.0.0**: Production WSGI server

### **Frontend Technologies**
- **Bootstrap 5**: Responsive UI framework with dark theme
- **Font Awesome**: Professional icon library
- **Jinja2**: Powerful template engine
- **Vanilla JavaScript**: Client-side functionality without framework overhead

### **Additional Libraries**
- **OpenPyXL 3.1.5**: Excel file generation and formatting
- **Email-Validator 2.3.0**: Email validation utilities
- **psycopg2-binary 2.9.10**: PostgreSQL database adapter

## Key Features

### **Production Order Management**
```python
# Example: Creating a production order
production_order = ProductionOrder()
production_order.production_order = "PO-2024-001"
production_order.workcenter_id = 1
production_order.quantity = 100
production_order.order_type = "IN"  # or "OUT"
production_order.user_id = current_user.id
# Timestamp automatically set to current time (displayed in IST)
```

### **Excel Access Control**
```python
# Example: Checking Excel access
current_user = User.query.get(session['user_id'])
has_excel_access = current_user and (current_user.excel_access or current_user.is_admin)

# Excel export with department filtering
if not current_user.is_admin and user_department:
    query = query.filter(User.department == user_department)
```

### **Reporting and Analytics**
- **Search Functionality**: Filter orders by production order number
- **Balance Reporting**: Real-time IN/OUT balance calculations with user name, department, and IST timestamps
- **Export Capabilities**: Professional Excel export with access control
- **Date Range Filtering**: Filter orders by creation date (displayed in IST)
- **Work Center Analysis**: View orders by specific work centers
- **Department-Based Filtering**: Users see only relevant data based on their department

### **Excel Export Features**
- **Access Control**: Only users with Excel permissions can download reports
- **Professional Formatting**: Headers, colors, and alignment
- **Multiple Worksheets**: Production Orders and Balance Reports
- **Department Filtering**: Non-admin users see only their department's data
- **Data Validation**: Comprehensive data integrity checks
- **Automated Generation**: One-click export functionality

## Security Features

### **Authentication Security**
- **Password Hashing**: Werkzeug-based secure password storage
- **Session Management**: Secure session-based authentication
- **Role Validation**: Route-level permission checking
- **Excel Access Control**: Granular permissions for data export
- **Auto-logout**: Session timeout and security measures

### **Data Security**
- **Foreign Key Constraints**: Database-level data integrity
- **Input Validation**: Comprehensive form validation
- **SQL Injection Protection**: SQLAlchemy ORM protection
- **XSS Prevention**: Template-based output escaping
- **Department Isolation**: Users can only access their department's data

### **Access Control**
- **Role-Based Permissions**: Admin vs. User vs. Excel Access levels
- **Route Protection**: Login required for all operational routes
- **Session Validation**: Continuous session state checking
- **Export Permissions**: Excel download access control

## User Interface Enhancements

### **Admin Interface**
- **User Management**: Create, edit, and manage user accounts
- **Excel Access Control**: Grant/revoke Excel export permissions per user
- **Visual Indicators**: Excel access status shown with icons and badges
- **Department Management**: Assign users to departments
- **Work Center Configuration**: Set up and manage production facilities

### **User Experience**
- **Conditional Navigation**: UI elements appear based on user permissions
- **Excel Download Buttons**: Visible only to users with appropriate access
- **Professional Styling**: Consistent design with proper spacing and alignment
- **Responsive Layout**: Optimized column layouts for form fields

## Development Guidelines

### **Code Structure**
```
├── app.py              # Flask application setup and configuration
├── main.py             # Application entry point
├── models.py           # Database models and relationships (with excel_access field)
├── routes.py           # URL routing and request handling (with Excel access routes)
├── static/             # Static files (CSS, JS, images, favicon)
├── templates/          # HTML templates with Jinja2 (updated with Excel access UI)
├── pyproject.toml      # Python dependencies and project config
└── replit.md           # Project documentation and preferences
```

### **Database Design Patterns**
- **Relationship Management**: Proper foreign key relationships
- **Timestamp Tracking**: Creation timestamps on all entities
- **Soft Deletes**: Active/inactive flags instead of hard deletes
- **Audit Trails**: User attribution for all data modifications
- **Permission Fields**: Boolean flags for feature access control

### **Performance Considerations**
- **Connection Pooling**: Optimized database connection management
- **Query Optimization**: Efficient joins and filtering with department-based access
- **Lazy Loading**: Strategic relationship loading
- **Index Usage**: Proper database indexing for performance

## Production Deployment

### **Environment Configuration**
```bash
# Required Environment Variables
DATABASE_URL=postgresql://user:password@host:port/database
SESSION_SECRET=your-secure-random-session-key

# Optional Configuration
FLASK_ENV=production
GUNICORN_WORKERS=4
GUNICORN_TIMEOUT=30
```

### **Security Checklist**
- [ ] Change default admin password
- [ ] Use strong session secrets
- [ ] Configure database with restricted user permissions
- [ ] Enable SSL/HTTPS in production
- [ ] Set up regular database backups
- [ ] Configure firewall and network security
- [ ] Enable application logging and monitoring
- [ ] Review Excel access permissions for all users

### **Performance Optimization**
- [ ] Configure database connection pooling
- [ ] Set up database indexing (including excel_access field)
- [ ] Enable query caching
- [ ] Configure static file serving
- [ ] Set up CDN for static assets
- [ ] Monitor application performance
- [ ] Configure log rotation

## Monitoring and Maintenance

### **Health Checks**
- Database connectivity testing
- Application response time monitoring
- User session validation
- Excel export functionality testing
- File system space monitoring

### **Backup Strategy**
- Daily automated database backups (including user permissions)
- Configuration file backups
- Static file preservation
- Version control integration

### **Logging**
- Application error logging
- User activity tracking (including Excel exports)
- Database query monitoring
- Performance metric collection

## Support and Documentation

### **Documentation Files**
- **README.md**: This comprehensive overview
- **DATABASE_SCHEMA.md**: Detailed database schema and setup
- **DATABASE_POSTGRESQL_SETUP.md**: PostgreSQL configuration guide
- **README_IIS_Deployment.md**: Windows IIS deployment instructions
- **replit.md**: Project preferences and architecture notes

### **Getting Help**
- Check application logs for error details
- Verify database connection and configuration
- Review environment variable settings
- Validate user permissions and roles
- Test Excel access permissions

### **Common Issues**
- **Login Problems**: Check user credentials and database connectivity
- **Data Not Saving**: Verify database permissions and constraints
- **Performance Issues**: Check database connections and query performance
- **Export Failures**: Validate Excel access permissions and data integrity
- **Permission Issues**: Verify user department assignments and Excel access flags

## Recent Updates

### **Version 2.0 Features**
- **Excel Access Control**: Granular permissions for Excel export functionality
- **Enhanced User Management**: Visual indicators for Excel access in admin interface
- **Department-Based Filtering**: Excel exports respect user department restrictions
- **UI Improvements**: Better field alignment and responsive layouts
- **Security Enhancements**: Additional permission layers for data export

### **Migration Notes**
- Added `excel_access` boolean field to user table
- Updated admin interface to manage Excel permissions
- Enhanced templates with conditional Excel download buttons
- Improved form layouts for better alignment

---

**Last Updated**: December 5, 2024  
**Version**: 2.0  
**Environment**: Replit Optimized  
**Database**: PostgreSQL Compatible  
**Current Features**: Excel access control, department-based filtering, enhanced user management, improved UI alignment