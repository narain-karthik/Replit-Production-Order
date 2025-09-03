# PostgreSQL Setup Guide for Production Order Tracking System

Simple setup guide for PostgreSQL database integration with the Production Order Tracking System, optimized for Replit environment with basic local development setup.

## Overview

The Production Order Tracking System uses PostgreSQL as its primary database with automatic provisioning in Replit environment. For Replit users, **no manual database setup is required** - everything is automatically configured.

## Replit Environment (Recommended)

### Automatic PostgreSQL Provisioning

The Replit environment automatically provides:

- **PostgreSQL Database**: Pre-configured and ready to use
- **Environment Variables**: Automatically set connection parameters
- **Connection Pooling**: Optimized for web application performance
- **Backup Management**: Handled by Replit infrastructure
- **SSL Connections**: Secure database connections by default

### Available Environment Variables

These are automatically set in Replit:

```bash
DATABASE_URL=postgresql://username:password@host:port/database
PGHOST=your-postgres-host
PGPORT=5432
PGUSER=your-username
PGPASSWORD=your-password
PGDATABASE=your-database-name
SESSION_SECRET=auto-generated-secure-key
```

### Quick Verification

To verify your Replit database is working:

1. **Check Application**: Simply run your application - if it starts without database errors, everything is working!

2. **Default Login**: Use the default credentials:
   - Username: `admin`
   - Password: `admin123`

3. **Test Features**: Try creating a production order to verify database functionality.

If you encounter any issues, restart your Replit environment and try again.

### Default Data Created Automatically

On first run, the application automatically creates:

- **Default Admin User**: username `admin`, password `admin123`
- **Default Work Centers**: WC001-Assembly, WC002-Machining, WC003-Welding, WC004-Painting, WC005-Quality Control
- **Default Departments**: Engineering, Production, Quality Control, Maintenance, Operations, Management
- **Work Center-Department Relationships**: Initial mappings for department-based access

## Database Tables

The system uses 5 tables with automatic creation:

1. **user** - User authentication and profiles
2. **work_center** - Production facilities
3. **department** - Organizational structure
4. **production_order** - Order tracking with IN/OUT types
5. **workcenter_department** - Many-to-many relationships for department-based access

All timestamps are stored in UTC and displayed in Indian Standard Time (IST) for user convenience.

## Local Development Setup (Optional)

### Prerequisites

- **Python 3.11+**: Required for Flask application
- **PostgreSQL 15+**: Database server
- **Administrative Access**: For installation and configuration

### Quick Installation

#### Windows
1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Run installer and use default settings
3. Remember the password you set for the postgres user

#### macOS
```bash
# Using Homebrew (recommended)
brew install postgresql@15
brew services start postgresql@15
```

#### Linux (Ubuntu/Debian)
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Create Database for Local Development

```sql
-- Connect as postgres user
psql -U postgres

-- Create database
CREATE DATABASE production_order_tracking;

-- Create application user
CREATE USER production_app WITH PASSWORD 'secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE production_order_tracking TO production_app;

-- Exit
\q
```

### Environment Configuration

Create `.env` file in project root:

```env
# Database Configuration
DATABASE_URL=postgresql://production_app:secure_password@localhost:5432/production_order_tracking

# Flask Configuration
SESSION_SECRET=your_random_secret_key_here
FLASK_ENV=development
```

### Install Python Dependencies

```bash
# Install required packages
pip install flask flask-sqlalchemy psycopg2-binary werkzeug openpyxl gunicorn

# Or if you have the project files:
pip install -e .
```

### Automatic Schema Creation

The application automatically creates all required tables on first run:

```bash
# Run the application - tables created automatically
python main.py

# Tables created:
# - user (authentication and profiles)
# - work_center (production facilities)
# - department (organizational structure)
# - production_order (order tracking)
# - workcenter_department (relationships)
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**: Ensure your Replit environment has restarted properly
2. **Tables Not Found**: Run the application once to create tables automatically
3. **Login Issues**: Use default credentials: admin/admin123
4. **Data Not Saving**: Check console for any database constraint errors

### Getting Help

- Check application logs in Replit console
- Verify database connection by running the application
- Restart your Replit environment if issues persist
- Use the default admin account to test functionality

## Features Supported

- **User Management**: Admin and regular user roles
- **Work Center Management**: Production facility tracking
- **Department-Based Access**: Users see only assigned work centers
- **Production Order Tracking**: IN/OUT order types with balance calculations
- **Balance Reporting**: Real-time balance calculations with IST timestamps
- **Excel Export**: Professional reporting with formatted exports
- **Search and Filtering**: Advanced search across production data

---

**Last Updated**: September 3, 2025  
**Environment**: Replit Optimized (Local development optional)  
**Database**: PostgreSQL Compatible with IST timezone display  
**Default Login**: admin/admin123