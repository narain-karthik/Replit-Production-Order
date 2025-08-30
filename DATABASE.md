# Database Setup Guide

This document explains how to set up and configure the PostgreSQL database for the Production Order Tracking System.

## Database Requirements

The application requires PostgreSQL as the database backend. The database stores:
- User accounts and authentication data
- Work center definitions
- Production orders (IN/OUT)
- Department information

## Replit Environment Setup

If you're running this on Replit, the database is automatically configured:

1. **Automatic Provisioning**: Replit provides a built-in PostgreSQL database
2. **Environment Variables**: The following are automatically set:
   - `DATABASE_URL`: Complete connection string
   - `PGHOST`: Database host
   - `PGPORT`: Database port
   - `PGUSER`: Database username
   - `PGPASSWORD`: Database password
   - `PGDATABASE`: Database name

3. **No Manual Setup Required**: The application will automatically:
   - Connect to the database using `DATABASE_URL`
   - Create all required tables on first run
   - Set up default data (admin user, work centers, departments)

## Local Development Setup

If running locally, you'll need to set up PostgreSQL:

### 1. Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Windows:**
Download and install from [postgresql.org](https://www.postgresql.org/download/windows/)

### 2. Create Database

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE production_orders;
CREATE USER app_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE production_orders TO app_user;
\q
```

### 3. Set Environment Variables

Create a `.env` file or set environment variables:

```bash
export DATABASE_URL="postgresql://app_user:your_password@localhost:5432/production_orders"
export SESSION_SECRET="your-secret-key-here"
```

## Database Schema

The application creates the following tables automatically:

### Users Table
- `id`: Primary key
- `username`: Unique username
- `password_hash`: Hashed password
- `is_admin`: Boolean for admin access
- `created_at`: Timestamp

### Work Centers Table
- `id`: Primary key
- `name`: Work center name
- `created_at`: Timestamp

### Production Orders Table
- `id`: Primary key
- `order_number`: Unique order identifier
- `order_type`: 'IN' or 'OUT'
- `quantity`: Order quantity
- `work_center_id`: Foreign key to work centers
- `user_id`: Foreign key to users
- `created_at`: Timestamp

### Departments Table
- `id`: Primary key
- `name`: Department name
- `created_at`: Timestamp

## Default Data

On first startup, the application automatically creates:

### Default Admin User
- **Username**: admin
- **Password**: admin123
- **Role**: Administrator

### Default Work Centers
- WC001 - Assembly
- WC002 - Machining
- WC003 - Welding
- WC004 - Painting
- WC005 - Quality Control

### Default Departments
- Engineering
- Production
- Quality Control
- Maintenance
- Operations
- Management

## Database Configuration

### Connection Settings
The application uses SQLAlchemy with these configurations:
- **Pool Recycle**: 300 seconds (prevents stale connections)
- **Pool Pre-ping**: Enabled (tests connections before use)
- **Automatic Reconnection**: Handles connection drops

### Environment Variables Required

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Complete PostgreSQL connection string | `postgresql://user:pass@host:5432/dbname` |
| `SESSION_SECRET` | Secret key for session encryption | `your-secret-key-here` |

## Troubleshooting

### Common Issues

**Connection Refused:**
- Check if PostgreSQL is running
- Verify connection parameters
- Check firewall settings

**Permission Denied:**
- Ensure database user has proper privileges
- Check password authentication

**Table Does Not Exist:**
- The application creates tables automatically
- Check for database connection errors in logs

### Checking Database Status

**In Replit:**
- Database is managed automatically
- Check the "Database" tab in your replit

**Local Development:**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Connect to database
psql $DATABASE_URL

# List tables
\dt

# Check table contents
SELECT * FROM users;
```

## Backup and Recovery

### Creating Backups
```bash
pg_dump $DATABASE_URL > backup.sql
```

### Restoring from Backup
```bash
psql $DATABASE_URL < backup.sql
```

## Production Considerations

For production deployments:
1. Use strong database passwords
2. Enable SSL connections
3. Configure regular backups
4. Monitor connection pooling
5. Set up database monitoring
6. Consider read replicas for high load

## Database Migrations

The application uses SQLAlchemy's `create_all()` method for initial setup. For production environments, consider using database migration tools like Alembic for schema changes.