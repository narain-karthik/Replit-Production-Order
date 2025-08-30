# PostgreSQL Setup Guide for Production Order Tracking System

Comprehensive setup guide for PostgreSQL database integration with the Production Order Tracking System, optimized for Replit deployment and local development environments.

## Overview

The Production Order Tracking System uses PostgreSQL as its primary production database with automatic provisioning in Replit environment. This guide covers both Replit deployment and local development setup with detailed configuration options for manufacturing environments.

## Replit Environment (Recommended)

### Automatic PostgreSQL Provisioning

The Replit environment automatically provides:

- **PostgreSQL Database**: Pre-configured and ready to use
- **Environment Variables**: Automatically set connection parameters
- **Connection Pooling**: Optimized for web application performance
- **Backup Management**: Handled by Replit infrastructure
- **SSL Connections**: Secure database connections by default

### Available Environment Variables

```bash
DATABASE_URL=postgresql://username:password@host:port/database
PGHOST=your-postgres-host
PGPORT=5432
PGUSER=your-username
PGPASSWORD=your-password
PGDATABASE=your-database-name
SESSION_SECRET=auto-generated-secure-key
```

### Verification Steps

1. **Check Database Connection Status**:
```python
# In your Replit console
python -c "
import os
print('Database URL:', os.environ.get('DATABASE_URL', 'Not set'))
print('PG Host:', os.environ.get('PGHOST', 'Not set'))
print('PG Database:', os.environ.get('PGDATABASE', 'Not set'))
print('Session Secret:', 'Set' if os.environ.get('SESSION_SECRET') else 'Not set')
"
```

2. **Test Database Connectivity**:
```python
# Run this in Replit shell
python -c "
from app import app, db
with app.app_context():
    try:
        db.create_all()
        print('✅ Database connection successful!')
        print('✅ Tables created successfully!')
        
        # Check if tables exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f'✅ Found {len(tables)} tables: {tables}')
    except Exception as e:
        print(f'❌ Database error: {e}')
"
```

3. **Verify Default Data**:
```python
# Check default admin user and work centers
python -c "
from app import app, db
from models import User, WorkCenter, Department
with app.app_context():
    try:
        admin = User.query.filter_by(username='admin').first()
        wc_count = WorkCenter.query.count()
        dept_count = Department.query.count()
        print(f'✅ Admin user: {\"Found\" if admin else \"Not found\"}')
        print(f'✅ Work centers: {wc_count}')
        print(f'✅ Departments: {dept_count}')
    except Exception as e:
        print(f'❌ Error checking data: {e}')
"
```

## Local Development Setup

### Prerequisites

- **Python 3.11+**: Required for Flask application
- **PostgreSQL 15+**: Database server (PostgreSQL 12+ supported)
- **Administrative Access**: For installation and configuration
- **Git**: For version control (optional)

### Windows Installation

1. **Download PostgreSQL**:
   - Visit: https://www.postgresql.org/download/windows/
   - Download PostgreSQL 15.x or higher
   - Run installer as Administrator

2. **Installation Configuration**:
   ```
   Installation Directory: C:\Program Files\PostgreSQL\15
   Data Directory: C:\Program Files\PostgreSQL\15\data
   Password: [Set strong password for postgres user]
   Port: 5432 (default)
   Locale: Default or your preference
   ```

3. **Verify Installation**:
   ```cmd
   # Open Command Prompt as Administrator
   cd "C:\Program Files\PostgreSQL\15\bin"
   psql -U postgres -h localhost
   # Enter password when prompted
   # You should see: postgres=#
   ```

4. **Add PostgreSQL to PATH** (optional):
   ```cmd
   # Add to system PATH environment variable:
   C:\Program Files\PostgreSQL\15\bin
   ```

### macOS Installation

1. **Using Homebrew** (Recommended):
   ```bash
   # Install Homebrew if not already installed
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # Install PostgreSQL
   brew install postgresql@15
   
   # Start PostgreSQL service
   brew services start postgresql@15
   
   # Create database cluster (if needed)
   initdb /usr/local/var/postgres
   ```

2. **Using PostgreSQL.app**:
   - Download from: https://postgresapp.com/
   - Drag PostgreSQL.app to Applications folder
   - Launch and initialize
   - Add to PATH: `/Applications/Postgres.app/Contents/Versions/15/bin`

3. **Verify Installation**:
   ```bash
   # Test connection
   psql postgres
   # Should connect successfully
   ```

### Linux Installation (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install PostgreSQL and contrib packages
sudo apt install postgresql postgresql-contrib postgresql-client

# Start and enable PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Check service status
sudo systemctl status postgresql

# Switch to postgres user and access database
sudo -u postgres psql

# Set password for postgres user (optional)
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'your_password';"
```

### CentOS/RHEL/Fedora Installation

```bash
# Install PostgreSQL
sudo dnf install postgresql postgresql-server postgresql-contrib

# Initialize database cluster
sudo postgresql-setup --initdb

# Start and enable service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Access database
sudo -u postgres psql
```

## Database Configuration

### Create Production Order Database

```sql
-- Connect as postgres superuser
psql -U postgres

-- Create database
CREATE DATABASE production_order_tracking
    WITH ENCODING='UTF8'
    LC_COLLATE='en_US.UTF-8'
    LC_CTYPE='en_US.UTF-8'
    TEMPLATE=template0;

-- Create dedicated application user
CREATE USER production_app WITH PASSWORD 'production_secure_password_2024';

-- Grant database privileges
GRANT ALL PRIVILEGES ON DATABASE production_order_tracking TO production_app;
GRANT USAGE, CREATE ON SCHEMA public TO production_app;

-- Connect to new database
\c production_order_tracking

-- Grant table privileges (run after table creation)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO production_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO production_app;

-- Grant future privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO production_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO production_app;

-- Create read-only user for reporting
CREATE USER production_readonly WITH PASSWORD 'readonly_password_2024';
GRANT CONNECT ON DATABASE production_order_tracking TO production_readonly;
GRANT USAGE ON SCHEMA public TO production_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO production_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO production_readonly;

-- Exit
\q
```

### Environment Configuration

Create `.env` file in project root:

```env
# Database Configuration
DATABASE_URL=postgresql://production_app:production_secure_password_2024@localhost:5432/production_order_tracking

# Flask Configuration
FLASK_APP=main.py
FLASK_ENV=development
SESSION_SECRET=your_very_long_random_secret_key_here_min_32_chars

# Optional: Email Configuration (for future features)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@domain.com
SMTP_PASSWORD=your-app-password

# Optional: Application Configuration
DEBUG=True
SECRET_KEY=another-secret-key-for-flask-sessions
```

### Advanced Database Configuration

**Edit `postgresql.conf`** for production optimization:

```ini
# Connection Settings
listen_addresses = 'localhost'          # Security: only local connections
port = 5432                             # Standard PostgreSQL port
max_connections = 100                   # Adjust based on application needs

# Memory Settings (adjust based on available RAM)
shared_buffers = 256MB                  # 25% of available RAM
effective_cache_size = 1GB              # 75% of available RAM
work_mem = 8MB                          # Per connection working memory
maintenance_work_mem = 64MB             # Maintenance operations memory

# Performance Settings
random_page_cost = 1.1                  # SSD optimization (default: 4.0)
effective_io_concurrency = 200          # SSD concurrent I/O
checkpoint_completion_target = 0.9      # Checkpoint spreading
wal_buffers = 16MB                      # WAL buffer size

# Logging Configuration
log_destination = 'stderr'              # Log destination
logging_collector = on                  # Enable log collector
log_directory = 'log'                   # Log directory
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_statement = 'none'                  # Log level ('all' for development)
log_duration = on                       # Log query duration
log_min_duration_statement = 1000       # Log slow queries (1 second+)
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h '

# Locale Settings
datestyle = 'iso, mdy'
timezone = 'UTC'                        # Use UTC for consistency
default_text_search_config = 'pg_catalog.english'
```

**Edit `pg_hba.conf`** for authentication:

```conf
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# Local connections
local   all             postgres                                peer
local   all             all                                     md5

# IPv4 local connections
host    all             all             127.0.0.1/32            md5
host    production_order_tracking  production_app  127.0.0.1/32  md5
host    production_order_tracking  production_readonly  127.0.0.1/32  md5

# IPv6 local connections
host    all             all             ::1/128                 md5
```

## Install Python Dependencies

```bash
# Create virtual environment (optional for local development)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate    # Windows

# Install PostgreSQL adapter
pip install psycopg2-binary

# Install all project dependencies (if requirements.txt exists)
pip install -r requirements.txt

# OR install using pyproject.toml
pip install -e .
```

## Database Schema Creation

### Automatic Schema Creation

The application automatically creates all required tables on first run:

```bash
# Run the application - tables created automatically
python main.py

# Tables created:
# - users (authentication and profiles)
# - work_centers (production facilities)
# - departments (organizational structure)
# - production_orders (order tracking)
```

### Manual Schema Creation (Optional)

If you need to create tables manually:

```sql
-- Connect to database
psql -U production_app -d production_order_tracking

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    name VARCHAR(100),
    department VARCHAR(100),
    password_hash VARCHAR(256) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create work_centers table
CREATE TABLE work_centers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create departments table
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create production_orders table
CREATE TABLE production_orders (
    id SERIAL PRIMARY KEY,
    production_order VARCHAR(50) NOT NULL,
    workcenter_id INTEGER REFERENCES work_centers(id) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    order_type VARCHAR(10) NOT NULL CHECK (order_type IN ('IN', 'OUT')),
    user_id INTEGER REFERENCES users(id) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_is_admin ON users(is_admin);
CREATE INDEX idx_users_is_active ON users(is_active);

CREATE INDEX idx_work_centers_is_active ON work_centers(is_active);

CREATE INDEX idx_departments_is_active ON departments(is_active);

CREATE INDEX idx_production_orders_order_type ON production_orders(order_type);
CREATE INDEX idx_production_orders_workcenter_id ON production_orders(workcenter_id);
CREATE INDEX idx_production_orders_user_id ON production_orders(user_id);
CREATE INDEX idx_production_orders_created_at ON production_orders(created_at);

-- Insert default data
INSERT INTO users (username, name, password_hash, is_admin) 
VALUES ('admin', 'System Administrator', 'scrypt:32768:8:1$[HASH]', TRUE);

INSERT INTO work_centers (name) VALUES 
('WC001 - Assembly'),
('WC002 - Machining'),
('WC003 - Welding'),
('WC004 - Painting'),
('WC005 - Quality Control');

INSERT INTO departments (name) VALUES 
('Engineering'),
('Production'),
('Quality Control'),
('Maintenance'),
('Operations'),
('Management');
```

## Performance Optimization

### Application-Level Configuration

```python
# app.py - Enhanced connection pooling
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,                     # Number of connections in pool
    'pool_recycle': 300,                 # Recycle connections every 5 minutes
    'pool_pre_ping': True,               # Test connections before use
    'pool_timeout': 30,                  # Timeout for getting connection
    'max_overflow': 20,                  # Additional connections beyond pool_size
    'echo': False,                       # Set to True for SQL query logging
    'connect_args': {
        'options': '-c timezone=utc'     # Set timezone for session
    }
}
```

### Database Performance Tuning

```sql
-- Analyze table statistics (run regularly)
ANALYZE users;
ANALYZE work_centers;
ANALYZE departments;
ANALYZE production_orders;

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;

-- Monitor table sizes
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(tablename)) as total_size,
    pg_size_pretty(pg_relation_size(tablename)) as table_size,
    pg_size_pretty(pg_total_relation_size(tablename) - pg_relation_size(tablename)) as index_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(tablename) DESC;
```

## Backup and Maintenance

### Automated Backup Scripts

**Linux/macOS Shell Script** (`backup_production_orders.sh`):
```bash
#!/bin/bash

# Configuration
DB_NAME="production_order_tracking"
DB_USER="production_app"
BACKUP_DIR="/home/backups/production_orders"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Set password for automated backup
export PGPASSWORD='production_secure_password_2024'

# Create backup
echo "Starting backup at $(date)"
pg_dump -U "$DB_USER" -h localhost -d "$DB_NAME" \
    --verbose \
    --clean \
    --no-owner \
    --no-privileges \
    > "$BACKUP_DIR/production_orders_$DATE.sql"

# Check backup success
if [ $? -eq 0 ]; then
    echo "✅ Backup completed successfully: $BACKUP_DIR/production_orders_$DATE.sql"
    
    # Compress backup
    gzip "$BACKUP_DIR/production_orders_$DATE.sql"
    echo "✅ Backup compressed: $BACKUP_DIR/production_orders_$DATE.sql.gz"
    
    # Clean old backups
    find "$BACKUP_DIR" -name "production_orders_*.sql.gz" -mtime +$RETENTION_DAYS -delete
    echo "✅ Old backups cleaned (retention: $RETENTION_DAYS days)"
else
    echo "❌ Backup failed!"
    exit 1
fi

# Unset password
unset PGPASSWORD

echo "Backup process completed at $(date)"
```

**Windows Batch File** (`backup_production_orders.bat`):
```batch
@echo off
set DB_NAME=production_order_tracking
set DB_USER=production_app
set PGPASSWORD=production_secure_password_2024
set BACKUP_DIR=C:\Backups\ProductionOrders
set DATE=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set DATE=%DATE: =0%

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

echo Starting backup at %date% %time%
"C:\Program Files\PostgreSQL\15\bin\pg_dump" -U %DB_USER% -h localhost -d %DB_NAME% --verbose --clean --no-owner --no-privileges > "%BACKUP_DIR%\production_orders_%DATE%.sql"

if %ERRORLEVEL% EQU 0 (
    echo ✅ Backup completed: %BACKUP_DIR%\production_orders_%DATE%.sql
) else (
    echo ❌ Backup failed!
    pause
    exit /b 1
)

echo Backup process completed at %date% %time%
pause
```

### Regular Maintenance

**Weekly Maintenance Script** (`maintenance.sql`):
```sql
-- Connect to database
\c production_order_tracking

-- Vacuum and analyze all tables
VACUUM ANALYZE;

-- Check database size
SELECT 
    pg_size_pretty(pg_database_size('production_order_tracking')) AS database_size,
    pg_size_pretty(pg_database_size('production_order_tracking') - 
        (SELECT COALESCE(SUM(pg_relation_size(oid)), 0) FROM pg_class WHERE relkind = 'r')) AS index_size;

-- Table statistics
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes,
    n_live_tup as live_rows,
    n_dead_tup as dead_rows
FROM pg_tables 
JOIN pg_stat_user_tables USING (tablename)
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check for bloated tables (dead tuples)
SELECT 
    tablename,
    n_live_tup,
    n_dead_tup,
    ROUND((n_dead_tup::float / NULLIF(n_live_tup + n_dead_tup, 0)) * 100, 2) as dead_tuple_percent
FROM pg_stat_user_tables
WHERE n_dead_tup > 0
ORDER BY dead_tuple_percent DESC;

-- Connection statistics
SELECT 
    count(*) as total_connections,
    count(*) FILTER (WHERE state = 'active') as active_connections,
    count(*) FILTER (WHERE state = 'idle') as idle_connections
FROM pg_stat_activity
WHERE datname = 'production_order_tracking';
```

## Monitoring and Troubleshooting

### Connection Testing Script

**Python Test Script** (`test_db_connection.py`):
```python
#!/usr/bin/env python3
import os
import sys
import psycopg2
from urllib.parse import urlparse
from datetime import datetime

def test_connection():
    """Test database connection and basic functionality."""
    try:
        # Get database URL from environment
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL not found in environment variables")
            print("   Set DATABASE_URL environment variable:")
            print("   export DATABASE_URL='postgresql://user:password@host:port/database'")
            return False
            
        print(f"🔗 Testing connection to: {database_url.split('@')[1] if '@' in database_url else 'hidden'}")
        
        # Parse URL
        url = urlparse(database_url)
        
        # Test connection
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        
        # Test basic query
        cur = conn.cursor()
        cur.execute('SELECT version();')
        version = cur.fetchone()
        print(f"✅ PostgreSQL version: {version[0].split(',')[0]}")
        
        # Test application database
        cur.execute("SELECT current_database(), current_user;")
        db_info = cur.fetchone()
        print(f"✅ Connected to database: {db_info[0]} as user: {db_info[1]}")
        
        # Check application tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cur.fetchall()
        table_names = [t[0] for t in tables]
        print(f"✅ Found {len(tables)} tables: {table_names}")
        
        # Expected tables for Production Order Tracking System
        expected_tables = ['users', 'work_centers', 'departments', 'production_orders']
        missing_tables = [t for t in expected_tables if t not in table_names]
        
        if missing_tables:
            print(f"⚠️  Missing expected tables: {missing_tables}")
            print("   Run the application to create missing tables automatically")
        else:
            print("✅ All expected tables found")
        
        # Test table content
        for table in expected_tables:
            if table in table_names:
                cur.execute(f"SELECT COUNT(*) FROM {table};")
                count = cur.fetchone()[0]
                print(f"✅ Table '{table}': {count} rows")
        
        # Test foreign key constraints
        cur.execute("""
            SELECT 
                tc.table_name,
                tc.constraint_name,
                tc.constraint_type
            FROM information_schema.table_constraints tc
            WHERE tc.table_schema = 'public' 
            AND tc.constraint_type = 'FOREIGN KEY'
            ORDER BY tc.table_name;
        """)
        fk_constraints = cur.fetchall()
        print(f"✅ Foreign key constraints: {len(fk_constraints)}")
        
        # Close connections
        cur.close()
        conn.close()
        print("✅ Database connection test completed successfully!")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        print("   Common solutions:")
        print("   1. Check if PostgreSQL is running")
        print("   2. Verify connection parameters (host, port, database, user, password)")
        print("   3. Check pg_hba.conf for authentication settings")
        print("   4. Ensure database and user exist")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_environment():
    """Check environment variables."""
    print("🔍 Checking environment variables...")
    
    required_vars = ['DATABASE_URL', 'SESSION_SECRET']
    optional_vars = ['PGHOST', 'PGPORT', 'PGUSER', 'PGPASSWORD', 'PGDATABASE']
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Not set (required)")
    
    for var in optional_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"ℹ️  {var}: Not set (optional)")

if __name__ == "__main__":
    print("🚀 Production Order Tracking System - Database Connection Test")
    print(f"📅 Test started at: {datetime.now()}")
    print("=" * 60)
    
    check_environment()
    print("-" * 60)
    
    if test_connection():
        print("=" * 60)
        print("🎉 All tests passed! Database is ready for Production Order Tracking System.")
        sys.exit(0)
    else:
        print("=" * 60)
        print("💥 Database connection test failed. Please check configuration.")
        sys.exit(1)
```

### Common Issues and Solutions

**Issue: Connection Refused**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list | grep postgresql  # macOS
sc query postgresql-x64-15  # Windows

# Start PostgreSQL if stopped
sudo systemctl start postgresql  # Linux
brew services start postgresql@15  # macOS
net start postgresql-x64-15  # Windows

# Check if service is listening on port 5432
netstat -tlnp | grep 5432  # Linux
lsof -i :5432  # macOS
netstat -an | findstr 5432  # Windows
```

**Issue: Authentication Failed**
```sql
-- Check user exists and has permissions
\du  -- List all users and roles

-- Reset user password if needed
ALTER USER production_app PASSWORD 'new_secure_password';

-- Check pg_hba.conf authentication method
-- Ensure 'md5' or 'scram-sha-256' is used for local connections
```

**Issue: Database Does Not Exist**
```sql
-- List all databases
\l

-- Create database if missing
CREATE DATABASE production_order_tracking;

-- Grant permissions to user
GRANT ALL PRIVILEGES ON DATABASE production_order_tracking TO production_app;
```

**Issue: Permission Denied on Tables**
```sql
-- Connect to target database
\c production_order_tracking

-- Grant table permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO production_app;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO production_app;

-- Grant future permissions
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO production_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO production_app;
```

### Performance Monitoring

**Monitor Database Performance**:
```sql
-- Check slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements
WHERE query LIKE '%production_orders%'
   OR query LIKE '%work_centers%'
   OR query LIKE '%users%'
ORDER BY mean_time DESC
LIMIT 10;

-- Monitor active connections
SELECT 
    pid,
    usename,
    application_name,
    client_addr,
    state,
    query_start,
    LEFT(query, 50) as query_snippet
FROM pg_stat_activity
WHERE datname = 'production_order_tracking'
AND state = 'active';

-- Check cache hit ratio
SELECT 
    'cache hit ratio' as metric,
    ROUND(
        (sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read))) * 100, 
        2
    ) as percentage
FROM pg_statio_user_tables;
```

## Production Deployment Checklist

### Security Configuration

- [ ] **Strong Passwords**: Use complex passwords for all database users
- [ ] **Limited Permissions**: Application user should only have necessary privileges
- [ ] **SSL Connections**: Enable SSL for database connections in production
- [ ] **Firewall Rules**: Restrict database access to application servers only
- [ ] **Regular Updates**: Keep PostgreSQL updated with security patches
- [ ] **Backup Encryption**: Encrypt database backups at rest
- [ ] **Access Logging**: Enable and monitor database access logs

### Performance Configuration

- [ ] **Connection Pooling**: Configure appropriate pool sizes
- [ ] **Memory Settings**: Tune shared_buffers and work_mem for your server
- [ ] **Disk Configuration**: Use SSDs for better I/O performance
- [ ] **Index Monitoring**: Regularly check and optimize indexes
- [ ] **Query Analysis**: Monitor and optimize slow queries
- [ ] **Vacuum Scheduling**: Set up automated VACUUM and ANALYZE

### Monitoring Setup

- [ ] **Health Checks**: Implement database connectivity checks
- [ ] **Performance Metrics**: Monitor query performance and connection counts
- [ ] **Disk Space**: Monitor database size and disk usage
- [ ] **Backup Verification**: Regularly test backup restoration
- [ ] **Alert Configuration**: Set up alerts for critical issues
- [ ] **Log Analysis**: Implement log monitoring and analysis

---

**Setup Guide Version**: 1.0  
**Last Updated**: August 30, 2025  
**PostgreSQL Compatibility**: 12+ (Recommended: 15+)  
**Tested Environments**: Replit, Ubuntu 20.04+, macOS 12+, Windows 10+