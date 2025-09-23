# Production Order Tracking System - IIS Deployment Guide

## Overview
This guide will help you deploy the Flask-based Production Order Tracking System on Windows IIS with Python 3.11+. This version includes Excel export access control and enhanced user management features.

## Prerequisites

### System Requirements
- **Windows Server 2016+** or **Windows 10/11**
- **IIS 10.0+** with required features
- **Python 3.13.7** (Latest stable version recommended)
- **PostgreSQL 15+** or **SQL Server** (for production database)

### Required IIS Features
Enable these IIS features via "Turn Windows features on/off" or Server Manager:

**Basic IIS Features:**
- Internet Information Services
- Web Management Tools → IIS Management Console
- World Wide Web Services → Common HTTP Features (all)
- World Wide Web Services → Application Development Features:
  - CGI ✓
  - ISAPI Extensions ✓
  - ISAPI Filters ✓

**Additional Features for Python:**
- IIS → CGI
- Application Development → CGI

## Step 1: Install Python 3.13.7

### Download and Install Python
1. Download Python 3.13.7 from https://www.python.org/downloads/
2. **Important:** Check "Add Python to PATH" during installation
3. Select "Install for all users"
4. Choose "Add Python to environment variables"

### Verify Installation
```cmd
python --version
pip --version
```

## Step 2: Install Required Python Libraries

### Create Project Directory
```cmd
mkdir C:\inetpub\wwwroot\production-tracking
cd C:\inetpub\wwwroot\production-tracking
```

### Copy Project Files
Copy all your project files to `C:\inetpub\wwwroot\production-tracking\`

### Install Dependencies
```cmd
# Navigate to project directory
cd C:\inetpub\wwwroot\production-tracking

# Install required libraries
pip install flask==3.1.2
pip install flask-sqlalchemy==3.1.1
pip install gunicorn==23.0.0
pip install psycopg2-binary==2.9.10
pip install sqlalchemy==2.0.43
pip install werkzeug==3.1.3
pip install openpyxl==3.1.5
pip install email-validator==2.3.0
pip install flask-login==0.6.3

# Or install from requirements file
pip install -r requirements.txt
```

### Create requirements.txt (if not exists)
```txt
flask==3.1.2
flask-sqlalchemy==3.1.1
gunicorn==23.0.0
psycopg2-binary==2.9.10
sqlalchemy==2.0.43
werkzeug==3.1.3
openpyxl==3.1.5
email-validator==2.3.0
flask-login==0.6.3
```

## Step 3: Install IIS-Python Integration

### Option A: Using wfastcgi (Recommended)
```cmd
# Install wfastcgi
pip install wfastcgi

# Enable wfastcgi in IIS
wfastcgi-enable
```

### Option B: Using HttpPlatformHandler
1. Download and install HttpPlatformHandler from Microsoft
2. This allows IIS to proxy requests to Python processes

## Step 4: Configure Database

### PostgreSQL Setup (Recommended)
1. Install PostgreSQL 15+
2. Create database and user:
```sql
CREATE DATABASE production_order_tracking;
CREATE USER production_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE production_order_tracking TO production_user;
```

### SQL Server Setup (Alternative)
1. Install SQL Server 2019+
2. Create database and configure connection string

## Step 5: Environment Configuration

### Create Environment Variables File
Create `.env` file in project root:
```env
# Database Configuration
DATABASE_URL=postgresql://production_user:your_secure_password@localhost:5432/production_order_tracking

# Session Security
SESSION_SECRET=your-very-secure-secret-key-here-min-32-chars

# Application Settings
FLASK_ENV=production
FLASK_DEBUG=False
```

### Windows Environment Variables
Set system environment variables:
```cmd
setx DATABASE_URL "postgresql://production_user:your_secure_password@localhost:5432/production_order_tracking" /M
setx SESSION_SECRET "your-very-secure-secret-key-here-min-32-chars" /M
```

## Step 6: Configure IIS

### Create IIS Application
1. Open **IIS Manager**
2. Right-click **Default Web Site** → **Add Application**
3. **Alias:** `production-tracking`
4. **Physical Path:** `C:\inetpub\wwwroot\production-tracking`
5. **Application Pool:** Create new pool (see below)

### Create Application Pool
1. In IIS Manager → **Application Pools** → **Add Application Pool**
2. **Name:** `ProductionTrackingPool`
3. **.NET CLR Version:** `No Managed Code`
4. **Managed Pipeline Mode:** `Integrated`
5. **Process Identity:** `ApplicationPoolIdentity`

### Configure Application Pool
1. Select **ProductionTrackingPool** → **Advanced Settings**
2. **Process Model** → **Idle Timeout:** `0` (or 20 minutes)
3. **Recycling** → **Regular Time Interval:** `1740` (29 hours)

## Step 7: Web.config Configuration

### Create web.config in project root:
```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="PythonHandler" 
           path="*" 
           verb="*" 
           modules="FastCgiModule"
           scriptProcessor="C:\Python313\python.exe|C:\Python313\Lib\site-packages\wfastcgi.py"
           resourceType="Unspecified" 
           requireAccess="Script" />
    </handlers>
    <defaultDocument>
      <files>
        <add value="main.py" />
      </files>
    </defaultDocument>
  </system.webServer>
  
  <appSettings>
    <add key="WSGI_HANDLER" value="main.app" />
    <add key="PYTHONPATH" value="C:\inetpub\wwwroot\production-tracking" />
    <add key="WSGI_LOG" value="C:\inetpub\logs\wfastcgi.log" />
  </appSettings>
</configuration>
```

### Alternative web.config for HttpPlatformHandler:
```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="PythonHandler" 
           path="*" 
           verb="*" 
           modules="httpPlatformHandler" 
           resourceType="Unspecified"/>
    </handlers>
    <httpPlatform processPath="C:\Python313\python.exe"
                  arguments="main.py"
                  stdoutLogEnabled="true"
                  stdoutLogFile=".\logs\stdout.log"
                  startupTimeLimit="60"
                  requestTimeout="00:04:00">
      <environmentVariables>
        <environmentVariable name="PORT" value="%HTTP_PLATFORM_PORT%" />
      </environmentVariables>
    </httpPlatform>
  </system.webServer>
</configuration>
```

## Step 8: Create Startup Script

### Create startup.py (for HttpPlatformHandler)
```python
import os
import sys
from main import app

if __name__ == '__main__':
    # Get port from IIS
    port = int(os.environ.get('PORT', 5000))
    
    # Run the application
    app.run(host='0.0.0.0', port=port, debug=False)
```

## Step 9: Set Permissions

### Configure Folder Permissions
1. Right-click project folder → **Properties** → **Security**
2. Add **IIS_IUSRS** with **Full Control**
3. Add **Application Pool Identity** (`IIS AppPool\ProductionTrackingPool`) with **Full Control**

### Set Python Permissions
```cmd
# Give IIS access to Python
icacls C:\Python313 /grant "IIS_IUSRS:(OI)(CI)F"
icacls C:\inetpub\wwwroot\production-tracking /grant "IIS_IUSRS:(OI)(CI)F"
```

## Step 10: Initialize Database

### Run Database Setup
```cmd
cd C:\inetpub\wwwroot\production-tracking
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized with Excel access control')"
```

### Add Excel Access Column (if migrating from older version)
```cmd
# If upgrading from version without Excel access
python -c "
from app import app, db; 
app.app_context().push(); 
db.engine.execute('ALTER TABLE user ADD COLUMN excel_access BOOLEAN DEFAULT FALSE NOT NULL'); 
print('Excel access column added')
"
```

## Step 11: Test Deployment

### Test Local Access
1. Open browser: `http://localhost/production-tracking`
2. Login with: **Username:** `admin`, **Password:** `admin123`
3. Navigate to User Management to configure Excel access permissions

### Test Excel Access Control
1. Login as admin
2. Go to **Admin Dashboard** → **User Management**
3. Create a new user and grant Excel access
4. Login as the new user and verify Excel download buttons appear in Reports section

### Test from Network
1. Open Windows Firewall
2. Allow HTTP (port 80) traffic
3. Test from another machine: `http://your-server-ip/production-tracking`

## New Features in Version 2.0

### Excel Access Management
- **Granular Control**: Admin can grant/revoke Excel export access per user
- **Visual Indicators**: Excel access status shown with badges in user management
- **Department Filtering**: Non-admin users with Excel access see only their department's data

### Enhanced User Interface
- **Improved Forms**: Better field alignment and responsive layouts
- **Conditional UI**: Excel download buttons appear only for authorized users
- **Professional Styling**: Updated templates with consistent design

### Security Enhancements
- **Permission Layers**: Additional access control for sensitive data export
- **Audit Trail**: User activity tracking includes Excel export attempts
- **Department Isolation**: Users can only export data from their assigned department

## Troubleshooting

### Common Issues

#### 1. Excel Export Not Working
**Error:** `Access denied. Excel export permission required.`
**Solution:** 
- Login as admin → User Management
- Edit user and check "Excel Access" checkbox
- Verify user has proper department assignment

#### 2. Python Not Found
**Error:** `The FastCGI process exited unexpectedly`
**Solution:** 
- Verify Python path in web.config
- Check Python installation: `python --version`

#### 3. Module Import Errors
**Error:** `ModuleNotFoundError`
**Solution:**
```cmd
# Install missing modules including new dependencies
pip install flask flask-sqlalchemy gunicorn psycopg2-binary openpyxl
```

#### 4. Database Migration Issues
**Error:** `Column 'excel_access' does not exist`
**Solution:**
```cmd
# Add the new column to existing database
python -c "
from app import db; 
db.engine.execute('ALTER TABLE user ADD COLUMN excel_access BOOLEAN DEFAULT FALSE NOT NULL')
"
```

#### 5. Permission Denied
**Error:** `Access denied` or `500 Internal Server Error`
**Solution:**
```cmd
# Fix permissions
icacls C:\inetpub\wwwroot\production-tracking /grant "IIS_IUSRS:(OI)(CI)F"
icacls C:\Python313 /grant "IIS_IUSRS:(OI)(CI)F"
```

#### 6. Application Pool Crashes
**Solution:**
1. Check **Event Viewer** → **Windows Logs** → **Application**
2. Review IIS logs in `C:\inetpub\logs\LogFiles\W3SVC1\`
3. Restart Application Pool

### Enable Detailed Error Messages
Add to web.config for debugging:
```xml
<system.web>
  <customErrors mode="Off"/>
</system.web>
```

### Log Files Locations
- **IIS Logs:** `C:\inetpub\logs\LogFiles\W3SVC1\`
- **Application Logs:** `C:\inetpub\logs\` (create this folder)
- **Event Viewer:** Windows Logs → Application

## Security Recommendations

### Production Security
1. **Change Default Credentials:**
   ```python
   # Update admin password in app.py
   admin_user.password_hash = generate_password_hash('NewSecurePassword123!')
   ```

2. **Configure Excel Access:**
   ```python
   # Grant Excel access to specific users only
   # Review permissions regularly
   # Monitor Excel export activity
   ```

3. **Secure Database:**
   - Use strong passwords
   - Enable SSL/TLS for database connections
   - Restrict database access to application server only

4. **IIS Security:**
   - Remove unused IIS features
   - Configure SSL certificates
   - Enable request filtering
   - Set up IP restrictions if needed

5. **Environment Variables:**
   - Never commit `.env` files to source control
   - Use strong SESSION_SECRET (32+ characters)

## Performance Optimization

### IIS Optimization
1. **Enable Output Caching**
2. **Configure Compression**
3. **Set up Load Balancing** (if multiple servers)

### Application Pool Settings
- **Maximum Worker Processes:** 1-4 (based on CPU cores)
- **Recycling Conditions:** Memory limit 500MB
- **Idle Timeout:** 20 minutes

### Excel Export Optimization
- **File Size Management**: Monitor Excel file sizes
- **Memory Usage**: Track memory during Excel generation
- **Concurrent Exports**: Limit simultaneous Excel exports

## Backup and Maintenance

### Regular Backups
1. **Database Backup:**
   ```cmd
   pg_dump -h localhost -U production_user production_order_tracking > backup.sql
   ```

2. **Application Backup:**
   - Copy entire application folder
   - Export IIS configuration
   - Backup user permissions and Excel access settings

### Updates
1. **Python Dependencies:**
   ```cmd
   pip install --upgrade flask flask-sqlalchemy openpyxl
   ```

2. **Application Updates:**
   - Stop IIS Application Pool
   - Deploy new code
   - Run database migrations if needed
   - Restart Application Pool

### Database Maintenance
1. **User Permissions Audit:**
   ```sql
   SELECT username, is_admin, excel_access, department FROM "user";
   ```

2. **Excel Export Activity:**
   ```sql
   -- Monitor Excel export usage
   -- Check user activity logs
   ```

## Support

### Default Login Credentials
- **Username:** `admin`
- **Password:** `admin123`
- **Excel Access:** Enabled by default
- **Change immediately after first login**

### Application Features (Version 2.0)
- **User Management with Excel Access Control**
- **Work Center Management**  
- **Production Order Tracking (IN/OUT)**
- **Balance Reports with Export Control**
- **Excel Export with Department Filtering**
- **Enhanced Role-based Access Control**

### Technical Support
- Check Event Viewer for system errors
- Review IIS logs for request issues
- Monitor application performance in Task Manager
- Validate Excel access permissions for users

### Excel Access Configuration
1. **Admin Setup:**
   - Login as admin
   - Navigate to User Management
   - Create/edit users and assign Excel access

2. **User Experience:**
   - Users with Excel access see download buttons in Reports
   - Non-admin users see only their department's data
   - Excel files include professional formatting

---

**Note:** This guide assumes Windows Server environment and includes the new Excel access control features introduced in Version 2.0. Adjust paths and permissions as needed for your specific setup.

**Last Updated:** December 5, 2024  
**Version:** 2.0 IIS Deployment Guide