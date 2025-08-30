from flask import render_template, request, redirect, url_for, flash, session, jsonify, make_response
from app import app, db
from models import User, WorkCenter, ProductionOrder, Department
from datetime import datetime
import io
from openpyxl import Workbook  # type: ignore
from openpyxl.styles import Font, PatternFill, Alignment  # type: ignore

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username, is_active=True).first()
    
    if user and user.check_password(password):
        session['user_id'] = user.id
        session['username'] = user.username
        session['is_admin'] = user.is_admin
        
        if user.is_admin:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('menu'))
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/menu')
def menu():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('menu.html')

@app.route('/in_orders')
def in_orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    workcenters = WorkCenter.query.filter_by(is_active=True).all()
    return render_template('in_orders.html', workcenters=workcenters)

@app.route('/out_orders')
def out_orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    workcenters = WorkCenter.query.filter_by(is_active=True).all()
    return render_template('out_orders.html', workcenters=workcenters)

@app.route('/save_orders', methods=['POST'])
def save_orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    order_type = request.form['order_type']
    orders_data = request.form.getlist('orders')
    
    try:
        for order_data in orders_data:
            if order_data:  # Skip empty entries
                parts = order_data.split('|')
                if len(parts) == 3:
                    workcenter_id, production_order, quantity = parts
                    
                    # Skip if workcenter_id is empty or invalid
                    if not workcenter_id or workcenter_id == "":
                        continue
                    
                    new_order = ProductionOrder()
                    new_order.production_order = production_order.strip() if production_order else ""
                    new_order.workcenter_id = int(workcenter_id)
                    new_order.quantity = int(quantity) if quantity else 0
                    new_order.order_type = order_type
                    new_order.user_id = session['user_id']
                    db.session.add(new_order)
        
        db.session.commit()
        flash(f'{order_type} orders saved successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error saving orders: {str(e)}', 'error')
    
    return redirect(url_for('menu'))

@app.route('/reports')
def reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')
    
    query = db.session.query(ProductionOrder).join(WorkCenter).join(User)
    
    if search:
        query = query.filter(ProductionOrder.production_order.contains(search))
    
    # Sorting
    if sort_by == 'created_at':
        if order == 'asc':
            query = query.order_by(ProductionOrder.created_at.asc())
        else:
            query = query.order_by(ProductionOrder.created_at.desc())
    elif sort_by == 'production_order':
        if order == 'asc':
            query = query.order_by(ProductionOrder.production_order.asc())
        else:
            query = query.order_by(ProductionOrder.production_order.desc())
    elif sort_by == 'quantity':
        if order == 'asc':
            query = query.order_by(ProductionOrder.quantity.asc())
        else:
            query = query.order_by(ProductionOrder.quantity.desc())
    
    orders = query.all()
    
    return render_template('reports.html', orders=orders, search=search, sort_by=sort_by, order=order)

# Admin Routes
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('login'))
    
    # Dashboard statistics
    total_users = User.query.filter_by(is_active=True).count()
    total_workcenters = WorkCenter.query.filter_by(is_active=True).count()
    total_in_orders = ProductionOrder.query.filter_by(order_type='IN').count()
    total_out_orders = ProductionOrder.query.filter_by(order_type='OUT').count()
    
    # Recent orders
    recent_orders = ProductionOrder.query.join(WorkCenter).join(User).order_by(ProductionOrder.created_at.desc()).limit(10).all()
    
    return render_template('admin_dashboard.html', 
                         total_users=total_users,
                         total_workcenters=total_workcenters,
                         total_in_orders=total_in_orders,
                         total_out_orders=total_out_orders,
                         recent_orders=recent_orders)

@app.route('/admin/users')
def admin_users():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('login'))
    
    users = User.query.all()
    departments = Department.query.filter_by(is_active=True).all()
    return render_template('admin_users.html', users=users, departments=departments)

@app.route('/admin/create_user', methods=['POST'])
def create_user():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    username = request.form['username']
    name = request.form.get('name', '')
    department = request.form.get('department', '')
    password = request.form['password']
    is_admin = 'is_admin' in request.form
    
    # Check if username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('Username already exists', 'error')
        return redirect(url_for('admin_users'))
    
    try:
        new_user = User()
        new_user.username = username
        new_user.name = name
        new_user.department = department
        new_user.is_admin = is_admin
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating user: {str(e)}', 'error')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/edit_user/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(user_id)
    
    user.username = request.form['username']
    user.name = request.form.get('name', '')
    user.department = request.form.get('department', '')
    if request.form['password']:
        user.set_password(request.form['password'])
    user.is_admin = 'is_admin' in request.form
    user.is_active = 'is_active' in request.form
    
    try:
        db.session.commit()
        flash('User updated successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating user: {str(e)}', 'error')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting the current admin user
    if user.id == session['user_id']:
        flash('Cannot delete your own account', 'error')
        return redirect(url_for('admin_users'))
    
    try:
        user.is_active = False  # Soft delete
        db.session.commit()
        flash('User deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/reports')
def admin_reports():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('login'))
    
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')
    
    query = db.session.query(ProductionOrder).join(WorkCenter).join(User)
    
    if search:
        query = query.filter(ProductionOrder.production_order.contains(search))
    
    # Sorting
    if sort_by == 'created_at':
        if order == 'asc':
            query = query.order_by(ProductionOrder.created_at.asc())
        else:
            query = query.order_by(ProductionOrder.created_at.desc())
    elif sort_by == 'production_order':
        if order == 'asc':
            query = query.order_by(ProductionOrder.production_order.asc())
        else:
            query = query.order_by(ProductionOrder.production_order.desc())
    elif sort_by == 'quantity':
        if order == 'asc':
            query = query.order_by(ProductionOrder.quantity.asc())
        else:
            query = query.order_by(ProductionOrder.quantity.desc())
    
    orders = query.all()
    
    return render_template('admin_reports.html', orders=orders, search=search, sort_by=sort_by, order=order)

@app.route('/admin/export_excel')
def export_excel():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    # Create workbook and worksheet
    wb = Workbook()
    ws = wb.active
    if ws is not None:
        ws.title = "Production Orders Report"
    
    # Define headers
    headers = ['Production Order', 'Work Center', 'Quantity', 'Type', 'Name', 'Department', 'Date & Time']
    
    # Style for headers
    header_font = Font(bold=True)
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    
    # Add headers
    if ws is not None:
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col, value=header)  # type: ignore
            if cell is not None:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal='center')
        
        # Get all orders
        orders = db.session.query(ProductionOrder).join(WorkCenter).join(User).order_by(ProductionOrder.created_at.desc()).all()
        
        # Add data
        for row, order in enumerate(orders, 2):
            ws.cell(row=row, column=1, value=order.production_order)  # type: ignore
            ws.cell(row=row, column=2, value=order.workcenter.name)  # type: ignore
            ws.cell(row=row, column=3, value=order.quantity)  # type: ignore
            ws.cell(row=row, column=4, value=order.order_type)  # type: ignore
            ws.cell(row=row, column=5, value=order.user.name or order.user.username)  # type: ignore
            ws.cell(row=row, column=6, value=order.user.department or '-')  # type: ignore
            ws.cell(row=row, column=7, value=order.created_at.strftime('%Y-%m-%d %H:%M:%S'))  # type: ignore
        
        # Auto-adjust column widths
        if hasattr(ws, 'columns') and hasattr(ws, 'column_dimensions'):
            for column in ws.columns:  # type: ignore
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width  # type: ignore
    
    # Save to memory
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    # Create response
    response = make_response(output.read())
    response.headers['Content-Disposition'] = f'attachment; filename=production_orders_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    
    return response

@app.route('/admin/master_data')
def master_data():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('login'))
    
    workcenters = WorkCenter.query.all()
    departments = Department.query.all()
    return render_template('master_data.html', workcenters=workcenters, departments=departments)

@app.route('/admin/create_workcenter', methods=['POST'])
def create_workcenter():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    name = request.form['name']
    
    try:
        new_workcenter = WorkCenter()
        new_workcenter.name = name
        db.session.add(new_workcenter)
        db.session.commit()
        flash('Work center created successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating work center: {str(e)}', 'error')
    
    return redirect(url_for('master_data'))

@app.route('/admin/edit_workcenter/<int:wc_id>', methods=['POST'])
def edit_workcenter(wc_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    workcenter = WorkCenter.query.get_or_404(wc_id)
    workcenter.name = request.form['name']
    workcenter.is_active = 'is_active' in request.form
    
    try:
        db.session.commit()
        flash('Work center updated successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating work center: {str(e)}', 'error')
    
    return redirect(url_for('master_data'))

@app.route('/admin/delete_workcenter/<int:wc_id>', methods=['POST'])
def delete_workcenter(wc_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    workcenter = WorkCenter.query.get_or_404(wc_id)
    
    try:
        workcenter.is_active = False  # Soft delete
        db.session.commit()
        flash('Work center deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting work center: {str(e)}', 'error')
    
    return redirect(url_for('master_data'))

# Department Management Routes
@app.route('/admin/create_department', methods=['POST'])
def create_department():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    name = request.form['name']
    
    try:
        new_department = Department()
        new_department.name = name
        db.session.add(new_department)
        db.session.commit()
        flash('Department created successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating department: {str(e)}', 'error')
    
    return redirect(url_for('master_data'))

@app.route('/admin/edit_department/<int:dept_id>', methods=['POST'])
def edit_department(dept_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    department = Department.query.get_or_404(dept_id)
    department.name = request.form['name']
    department.is_active = 'is_active' in request.form
    
    try:
        db.session.commit()
        flash('Department updated successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating department: {str(e)}', 'error')
    
    return redirect(url_for('master_data'))

@app.route('/admin/delete_department/<int:dept_id>', methods=['POST'])
def delete_department(dept_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    department = Department.query.get_or_404(dept_id)
    
    try:
        department.is_active = False  # Soft delete
        db.session.commit()
        flash('Department deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting department: {str(e)}', 'error')
    
    return redirect(url_for('master_data'))
