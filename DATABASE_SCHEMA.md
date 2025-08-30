# Database Schema Documentation

Comprehensive documentation for the Production Order Tracking System database structure, optimized for PostgreSQL with simplified two-tier role system and manufacturing workflow support.

## Overview

The system uses a modern relational database architecture with **4 core tables** supporting user management, work center definitions, departmental organization, and comprehensive production order lifecycle tracking. Designed for PostgreSQL primary deployment with UTC timezone support and optimized for Replit environment.

**Database Tables:**
1. **users** - User authentication and profile management with role-based access
2. **work_centers** - Production facility definitions and work center management
3. **departments** - Organizational unit definitions and departmental structure
4. **production_orders** - Core production order lifecycle with IN/OUT tracking and audit trails

## Database Architecture

### **Core Design Principles**
- **Simplified Role Structure**: Two-tier system (Regular User and Administrator)
- **Audit Trail**: Complete tracking of production orders and user actions
- **Performance Optimized**: Strategic indexing and connection pooling
- **Manufacturing Focus**: Specialized for production order tracking workflows
- **Data Integrity**: Foreign key constraints and comprehensive validation

## Database Configuration

### Create Production Order Database

```sql
-- Connect as postgres superuser
psql -U postgres

-- Create database
CREATE DATABASE production_order_tracking;

-- Create dedicated user (recommended)
CREATE USER production_user WITH PASSWORD 'production_password_2024';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE production_order_tracking TO production_user;

-- Connect to new database
\c production_order_tracking

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO production_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO production_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO production_user;

-- Exit
\q
```

## Database Tables

### 1. Users Table (`users`)

Central user management with authentication, role assignment, and departmental organization.

```sql
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
```

**Field Specifications:**
- `id`: Auto-incrementing primary key
- `username`: Unique login identifier (3-80 chars, required for authentication)
- `name`: Full user name (optional, up to 100 chars)
- `department`: Departmental assignment (max 100 chars)
- `password_hash`: Werkzeug-secured password hash (256 chars for security)
- `is_admin`: Boolean flag for administrative privileges (default: false)
- `is_active`: Account status flag for soft deletion (default: true)
- `created_at`: Account creation timestamp (UTC, auto-generated)

**Indexes & Constraints:**
```sql
CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_is_admin ON users(is_admin);
CREATE INDEX idx_users_is_active ON users(is_active);
CREATE INDEX idx_users_department ON users(department);
CREATE INDEX idx_users_created_at ON users(created_at);
```

**Default Admin User Creation:**
```sql
-- Automatically created on first application startup
INSERT INTO users (username, name, password_hash, is_admin, is_active)
VALUES ('admin', 'System Administrator', '[HASHED_PASSWORD]', TRUE, TRUE);
```

### 2. Work Centers Table (`work_centers`)

Production facility definitions with status management and creation tracking.

```sql
CREATE TABLE work_centers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Field Specifications:**
- `id`: Auto-incrementing primary key
- `name`: Work center identifier/name (required, max 100 chars)
- `is_active`: Status flag for operational work centers (default: true)
- `created_at`: Work center creation timestamp (UTC, auto-generated)

**Indexes & Constraints:**
```sql
CREATE INDEX idx_work_centers_name ON work_centers(name);
CREATE INDEX idx_work_centers_is_active ON work_centers(is_active);
CREATE INDEX idx_work_centers_created_at ON work_centers(created_at);
```

**Default Work Centers:**
```sql
-- Automatically created on first application startup
INSERT INTO work_centers (name, is_active) VALUES
('WC001 - Assembly', TRUE),
('WC002 - Machining', TRUE),
('WC003 - Welding', TRUE),
('WC004 - Painting', TRUE),
('WC005 - Quality Control', TRUE);
```

### 3. Departments Table (`departments`)

Organizational structure definitions for user categorization and reporting.

```sql
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Field Specifications:**
- `id`: Auto-incrementing primary key
- `name`: Department name/identifier (required, max 100 chars)
- `is_active`: Status flag for active departments (default: true)
- `created_at`: Department creation timestamp (UTC, auto-generated)

**Indexes & Constraints:**
```sql
CREATE INDEX idx_departments_name ON departments(name);
CREATE INDEX idx_departments_is_active ON departments(is_active);
CREATE INDEX idx_departments_created_at ON departments(created_at);
```

**Default Departments:**
```sql
-- Automatically created on first application startup
INSERT INTO departments (name, is_active) VALUES
('Engineering', TRUE),
('Production', TRUE),
('Quality Control', TRUE),
('Maintenance', TRUE),
('Operations', TRUE),
('Management', TRUE);
```

### 4. Production Orders Table (`production_orders`)

Core production order lifecycle management with comprehensive tracking and audit capabilities.

```sql
CREATE TABLE production_orders (
    id SERIAL PRIMARY KEY,
    production_order VARCHAR(50) NOT NULL,
    workcenter_id INTEGER REFERENCES work_centers(id) NOT NULL,
    quantity INTEGER NOT NULL,
    order_type VARCHAR(10) NOT NULL CHECK (order_type IN ('IN', 'OUT')),
    user_id INTEGER REFERENCES users(id) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Field Specifications:**
- `id`: Auto-incrementing primary key
- `production_order`: Production order identifier/number (max 50 chars, required)
- `workcenter_id`: Foreign key reference to work_centers table (required)
- `quantity`: Order quantity (integer, required, must be positive)
- `order_type`: Order direction - 'IN' for incoming, 'OUT' for outgoing (required)
- `user_id`: Foreign key reference to users table (order creator, required)
- `created_at`: Order creation timestamp (UTC, auto-generated)

**Indexes & Constraints:**
```sql
CREATE INDEX idx_production_orders_production_order ON production_orders(production_order);
CREATE INDEX idx_production_orders_workcenter_id ON production_orders(workcenter_id);
CREATE INDEX idx_production_orders_user_id ON production_orders(user_id);
CREATE INDEX idx_production_orders_order_type ON production_orders(order_type);
CREATE INDEX idx_production_orders_created_at ON production_orders(created_at);
CREATE INDEX idx_production_orders_quantity ON production_orders(quantity);

-- Composite indexes for common query patterns
CREATE INDEX idx_production_orders_type_workcenter ON production_orders(order_type, workcenter_id);
CREATE INDEX idx_production_orders_date_type ON production_orders(created_at, order_type);
CREATE INDEX idx_production_orders_user_date ON production_orders(user_id, created_at);
```

**Check Constraints:**
```sql
-- Ensure valid order types
ALTER TABLE production_orders ADD CONSTRAINT chk_order_type 
CHECK (order_type IN ('IN', 'OUT'));

-- Ensure positive quantities
ALTER TABLE production_orders ADD CONSTRAINT chk_positive_quantity 
CHECK (quantity > 0);
```

## Relationship Mapping

### **User Relationships**
```sql
-- Users can create multiple production orders
users(id) ←→ production_orders(user_id) [1:Many]

-- Users belong to departments (referenced by name, not FK)
users.department ←→ departments.name [Many:1 via name reference]
```

### **Work Center Relationships**
```sql
-- Work centers can have multiple production orders
work_centers(id) ←→ production_orders(workcenter_id) [1:Many]
```

### **Production Order Relationships**
```sql
-- Production orders are created by users
production_orders(user_id) ←→ users(id) [Many:1]

-- Production orders are assigned to work centers
production_orders(workcenter_id) ←→ work_centers(id) [Many:1]
```

## Data Flow and Business Logic

### **Production Order Lifecycle**

1. **Order Creation**:
   ```sql
   INSERT INTO production_orders (production_order, workcenter_id, quantity, order_type, user_id)
   VALUES ('PO-2024-001', 1, 100, 'IN', 1);
   ```

2. **Order Tracking**:
   ```sql
   -- Query orders by work center
   SELECT po.*, wc.name as workcenter_name, u.username
   FROM production_orders po
   JOIN work_centers wc ON po.workcenter_id = wc.id
   JOIN users u ON po.user_id = u.id
   WHERE wc.id = 1;
   ```

3. **Reporting Queries**:
   ```sql
   -- Daily production summary
   SELECT 
       wc.name as workcenter,
       po.order_type,
       COUNT(*) as order_count,
       SUM(po.quantity) as total_quantity
   FROM production_orders po
   JOIN work_centers wc ON po.workcenter_id = wc.id
   WHERE DATE(po.created_at) = CURRENT_DATE
   GROUP BY wc.name, po.order_type
   ORDER BY wc.name, po.order_type;
   ```

## Performance Optimization

### **Query Optimization Strategies**

1. **Common Query Patterns**:
   ```sql
   -- Optimized for reports page
   EXPLAIN ANALYZE
   SELECT po.*, wc.name as workcenter_name, u.username
   FROM production_orders po
   JOIN work_centers wc ON po.workcenter_id = wc.id
   JOIN users u ON po.user_id = u.id
   ORDER BY po.created_at DESC
   LIMIT 50;
   ```

2. **Index Usage Verification**:
   ```sql
   -- Check index usage statistics
   SELECT 
       schemaname,
       tablename,
       indexname,
       idx_scan,
       idx_tup_read,
       idx_tup_fetch
   FROM pg_stat_user_indexes
   WHERE tablename IN ('users', 'work_centers', 'departments', 'production_orders')
   ORDER BY idx_scan DESC;
   ```

### **Database Statistics**

```sql
-- Table size and row count analysis
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
    n_tup_ins as inserts,
    n_tup_upd as updates,
    n_tup_del as deletes,
    n_live_tup as live_rows
FROM pg_tables 
JOIN pg_stat_user_tables USING (tablename)
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## Data Validation and Integrity

### **Application-Level Validations**

1. **User Validation**:
   ```python
   # Username: 3-80 characters, alphanumeric
   # Password: Minimum 6 characters (configurable)
   # Department: Optional, max 100 characters
   ```

2. **Production Order Validation**:
   ```python
   # Production Order: Required, max 50 characters
   # Quantity: Required, positive integer
   # Order Type: Must be 'IN' or 'OUT'
   # Work Center: Must exist and be active
   ```

### **Database-Level Constraints**

```sql
-- Foreign key constraints ensure referential integrity
ALTER TABLE production_orders 
ADD CONSTRAINT fk_production_orders_workcenter
FOREIGN KEY (workcenter_id) REFERENCES work_centers(id);

ALTER TABLE production_orders 
ADD CONSTRAINT fk_production_orders_user
FOREIGN KEY (user_id) REFERENCES users(id);

-- Check constraints ensure data validity
ALTER TABLE production_orders 
ADD CONSTRAINT chk_order_type_valid
CHECK (order_type IN ('IN', 'OUT'));

ALTER TABLE production_orders 
ADD CONSTRAINT chk_quantity_positive
CHECK (quantity > 0);
```

## Backup and Maintenance

### **Regular Maintenance Scripts**

```sql
-- Weekly maintenance routine
VACUUM ANALYZE;

-- Check for unused indexes
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) as size
FROM pg_stat_user_indexes
WHERE idx_scan = 0 AND schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;

-- Update table statistics
ANALYZE users;
ANALYZE work_centers;
ANALYZE departments;
ANALYZE production_orders;
```

### **Data Cleanup Routines**

```sql
-- Archive old production orders (example: older than 1 year)
-- Note: Implement as per business requirements
CREATE TABLE production_orders_archive AS
SELECT * FROM production_orders
WHERE created_at < CURRENT_DATE - INTERVAL '1 year';

-- Clean up inactive users (soft delete verification)
UPDATE users SET is_active = FALSE
WHERE username != 'admin' 
AND id NOT IN (
    SELECT DISTINCT user_id 
    FROM production_orders 
    WHERE created_at > CURRENT_DATE - INTERVAL '90 days'
);
```

## Security Considerations

### **Access Control**

1. **Database User Permissions**:
   ```sql
   -- Create read-only reporting user
   CREATE USER production_readonly WITH PASSWORD 'readonly_password';
   GRANT CONNECT ON DATABASE production_order_tracking TO production_readonly;
   GRANT USAGE ON SCHEMA public TO production_readonly;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO production_readonly;
   ```

2. **Row-Level Security** (optional for advanced deployments):
   ```sql
   -- Example: Users can only see their own orders
   ALTER TABLE production_orders ENABLE ROW LEVEL SECURITY;
   
   CREATE POLICY production_orders_user_policy ON production_orders
   FOR ALL TO application_role
   USING (user_id = current_setting('app.current_user_id')::INTEGER);
   ```

### **Data Protection**

- **Password Security**: Werkzeug password hashing with salt
- **Session Security**: Secure session management with configurable secrets
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries
- **Input Validation**: Comprehensive form validation and sanitization

## Monitoring and Troubleshooting

### **Common Issues and Solutions**

1. **Foreign Key Violations**:
   ```sql
   -- Check for orphaned records
   SELECT po.id, po.workcenter_id
   FROM production_orders po
   LEFT JOIN work_centers wc ON po.workcenter_id = wc.id
   WHERE wc.id IS NULL;
   ```

2. **Performance Issues**:
   ```sql
   -- Identify slow queries
   SELECT query, calls, total_time, mean_time
   FROM pg_stat_statements
   WHERE query LIKE '%production_orders%'
   ORDER BY mean_time DESC
   LIMIT 10;
   ```

3. **Connection Issues**:
   ```sql
   -- Monitor active connections
   SELECT 
       pid,
       usename,
       application_name,
       client_addr,
       state,
       query_start
   FROM pg_stat_activity
   WHERE state = 'active'
   AND datname = 'production_order_tracking';
   ```

---

**Schema Version**: 1.0  
**Last Updated**: August 30, 2025  
**PostgreSQL Compatibility**: 12+  
**Encoding**: UTF-8  
**Timezone**: UTC (converted to local in application layer)