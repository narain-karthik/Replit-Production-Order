# Production Order Tracking System

## Overview

This is a Flask-based web application for tracking production orders in a manufacturing environment. The system allows users to record incoming (IN) and outgoing (OUT) production orders across different work centers, with role-based access control for administrators and regular users. It features user management, work center management, order tracking, reporting capabilities, and Excel export functionality.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Flask for server-side rendering
- **UI Framework**: Bootstrap 5 with dark theme for responsive design
- **Icons**: Font Awesome 6.4.0 for consistent iconography
- **Client-side**: Vanilla JavaScript for form validation, search functionality, and UI interactions

### Backend Architecture
- **Web Framework**: Flask with modular structure separating routes, models, and application configuration
- **Database ORM**: SQLAlchemy with declarative base for database operations
- **Authentication**: Session-based authentication with password hashing using Werkzeug security utilities
- **File Structure**: 
  - `app.py`: Application factory and configuration
  - `models.py`: Database models and relationships
  - `routes.py`: URL routing and request handling
  - `main.py`: Application entry point

### Data Storage
- **Database**: SQLAlchemy ORM with configurable database backend (configured via DATABASE_URL environment variable)
- **Models**:
  - User: Authentication and role management
  - WorkCenter: Production facility definitions
  - ProductionOrder: Order tracking with relationships to users and work centers
- **Connection Management**: Connection pooling with automatic reconnection and health checks

### Authentication & Authorization
- **Session Management**: Flask sessions with configurable secret key
- **Password Security**: Werkzeug password hashing with salt
- **Role-based Access**: Admin and regular user roles with different permission levels
- **Auto-provisioning**: Default admin user creation on first startup

## External Dependencies

### Frontend Libraries
- **Bootstrap CSS**: CDN-hosted dark theme variant for responsive UI components
- **Font Awesome**: CDN-hosted icon library for consistent visual elements

### Python Packages
- **Flask**: Core web framework for request handling and templating
- **Flask-SQLAlchemy**: Database ORM integration with Flask
- **Werkzeug**: Password hashing, security utilities, and proxy fix middleware
- **OpenPyXL**: Excel file generation for data export functionality

### Infrastructure
- **Database**: Configurable via DATABASE_URL environment variable (supports PostgreSQL, SQLite, etc.)
- **Session Storage**: Configurable session secret via SESSION_SECRET environment variable
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies