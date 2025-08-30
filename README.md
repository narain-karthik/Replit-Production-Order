# Production Order Tracking System

A Flask-based web application for tracking production orders in a manufacturing environment. The system allows users to record incoming (IN) and outgoing (OUT) production orders across different work centers, with role-based access control for administrators and regular users.

## Features

- **User Management**: Admin and regular user roles with secure authentication
- **Work Center Management**: Track production across multiple work centers
- **Order Tracking**: Record and monitor IN/OUT production orders
- **Reporting**: Generate reports and export data to Excel
- **Responsive Design**: Bootstrap-based UI that works on all devices
- **Dark Theme**: Professional dark theme interface

## Quick Start

1. **Database Setup**: The application uses PostgreSQL. See [DATABASE.md](DATABASE.md) for setup instructions.

2. **Environment Variables**: Set the following environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `SESSION_SECRET`: Secret key for session encryption

3. **Installation**: Dependencies are managed through `pyproject.toml`
   ```bash
   # Dependencies will be automatically installed in Replit
   ```

4. **Run the Application**:
   ```bash
   python main.py
   ```
   Or use gunicorn for production:
   ```bash
   gunicorn app:app
   ```

5. **Access the Application**: Open your browser to `http://localhost:5000`

## Default Login

- **Username**: admin
- **Password**: admin123

*Important*: Change the default admin password after first login.

## Project Structure

```
├── app.py              # Flask application setup and configuration
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # URL routing and request handling
├── static/             # Static files (CSS, JS, images)
├── templates/          # HTML templates
└── pyproject.toml      # Python dependencies
```

## Core Models

- **User**: Authentication and role management
- **WorkCenter**: Production facility definitions  
- **ProductionOrder**: Order tracking with relationships
- **Department**: Organizational units

## Technology Stack

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **PostgreSQL**: Database
- **Werkzeug**: Security utilities

### Frontend
- **Bootstrap 5**: UI framework with dark theme
- **Font Awesome**: Icons
- **Jinja2**: Template engine
- **Vanilla JavaScript**: Client-side functionality

## Security Features

- Password hashing with Werkzeug
- Session-based authentication
- Role-based access control
- CSRF protection
- Proxy middleware support

## Export Functionality

- Export production orders to Excel
- Configurable date ranges
- Work center filtering
- Professional formatting

## Development

The application follows Flask best practices with:
- Modular structure separating concerns
- Database connection pooling
- Automatic table creation
- Default data provisioning
- Comprehensive logging

## Production Deployment

For production deployment:
1. Use a production WSGI server (gunicorn included)
2. Set `DEBUG=False`
3. Use strong session secrets
4. Configure proper database connections
5. Set up reverse proxy if needed

## Support

For issues or questions about this production order tracking system, refer to the application logs or check the database configuration in [DATABASE.md](DATABASE.md).