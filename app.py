#!/usr/bin/env python3
"""
ACEP PCI DSS Audit Web Assistant
A Flask-based audit tool for PCI DSS compliance assessment
Created by Chaitanya Eshwar Prasad
"""

import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'pci-dss-audit-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('database', exist_ok=True)

# Database configuration
DATABASE = 'database/pci_dss_audit.db'

# Template helper functions
def get_file_icon(filename):
    """Get Bootstrap icon class based on file extension"""
    if not filename:
        return 'bi-file'
    
    ext = filename.lower().split('.')[-1] if '.' in filename else ''
    
    icon_map = {
        'pdf': 'bi-file-pdf',
        'doc': 'bi-file-word',
        'docx': 'bi-file-word',
        'xls': 'bi-file-excel',
        'xlsx': 'bi-file-excel',
        'ppt': 'bi-file-ppt',
        'pptx': 'bi-file-ppt',
        'jpg': 'bi-file-image',
        'jpeg': 'bi-file-image',
        'png': 'bi-file-image',
        'gif': 'bi-file-image',
        'txt': 'bi-file-text',
        'zip': 'bi-file-zip',
        'rar': 'bi-file-zip',
        'mp4': 'bi-file-play',
        'avi': 'bi-file-play',
        'mov': 'bi-file-play'
    }
    
    return icon_map.get(ext, 'bi-file')

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if not size_bytes:
        return '0 B'
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f} TB"

# Register template filters
app.jinja_env.filters['get_file_icon'] = get_file_icon
app.jinja_env.filters['format_file_size'] = format_file_size

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with required tables"""
    conn = get_db_connection()
    
    # Users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # PCI DSS Requirements table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pci_requirements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requirement_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT NOT NULL,
            subcategory TEXT,
            status TEXT DEFAULT 'Not Assessed',
            notes TEXT,
            assessed_by TEXT,
            assessed_at TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Evidence table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS evidence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            requirement_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_size INTEGER,
            description TEXT,
            uploaded_by TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (requirement_id) REFERENCES pci_requirements (requirement_id)
        )
    ''')
    
    # Add description column if it doesn't exist (for existing databases)
    try:
        conn.execute('ALTER TABLE evidence ADD COLUMN description TEXT')
        conn.commit()
    except sqlite3.OperationalError:
        # Column already exists
        pass
    
    # Risk register table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS risks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            likelihood INTEGER NOT NULL CHECK (likelihood BETWEEN 1 AND 5),
            impact INTEGER NOT NULL CHECK (impact BETWEEN 1 AND 5),
            risk_score INTEGER GENERATED ALWAYS AS (likelihood * impact) STORED,
            mitigation TEXT,
            owner TEXT,
            status TEXT DEFAULT 'Open',
            created_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Cardholder Data Tracking table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cardholder_data_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_type TEXT NOT NULL,
            description TEXT,
            classification TEXT NOT NULL,
            storage_location TEXT,
            encryption_status TEXT,
            disposal_procedures TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Service Provider Management table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS service_providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_person TEXT,
            email TEXT,
            phone TEXT,
            contract_status TEXT DEFAULT 'Active',
            compliance_status TEXT DEFAULT 'Under Review',
            pci_level TEXT,
            last_assessment_date DATE,
            next_assessment_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    
    # Create default admin user if not exists
    admin_exists = conn.execute('SELECT id FROM users WHERE username = ?', ('acep',)).fetchone()
    if not admin_exists:
        password_hash = generate_password_hash('acep123')
        conn.execute('INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)',
                    ('acep', password_hash, 'acep@chaitanyaeshwarprasad.com'))
        conn.commit()
    
    # Load PCI DSS requirements if not exists
    requirements_exist = conn.execute('SELECT COUNT(*) as count FROM pci_requirements').fetchone()
    if requirements_exist['count'] == 0:
        load_pci_requirements(conn)
    
    conn.close()

def load_pci_requirements(conn):
    """Load PCI DSS v4.0 requirements into database"""
    requirements = [
        # Requirement 1: Install and Maintain Network Security Controls
        ('1.1.1', 'Firewalls installed and configured between untrusted and trusted networks', 'Install and configure firewalls to filter traffic between untrusted networks and any system components in the cardholder data environment (CDE).', 'Network Security Controls'),
        ('1.1.2', 'Default passwords changed on all systems and devices', 'Change all vendor-supplied defaults and remove or disable unnecessary default accounts before installing a system on the network.', 'Network Security Controls'),
        ('1.1.3', 'Firewall rules reviewed every 6 months and documented', 'Establish firewall and router configuration standards that include a formal process for approving and testing all network connections and changes to the firewall and router configurations.', 'Network Security Controls'),
        
        # Requirement 2: Apply Secure Configurations to All System Components
        ('2.1.1', 'Remove unnecessary services, protocols, and accounts', 'For system components that are connected to the cardholder data environment or that could impact the security of the CDE, implement only necessary services, protocols, daemons, etc.', 'Secure Configurations'),
        ('2.1.2', 'Enable only required ports', 'Configure system security parameters to prevent misuse and implement only necessary services, protocols, daemons, etc.', 'Secure Configurations'),
        ('2.1.3', 'Apply secure configuration standards (e.g., CIS benchmarks)', 'Develop configuration standards for all system components. Assure that these standards address all known security vulnerabilities and are consistent with industry-accepted system hardening standards.', 'Secure Configurations'),
        
        # Requirement 3: Protect Stored Account Data
        ('3.1.1', 'Store cardholder data (CHD) only when absolutely necessary', 'Keep cardholder data storage to a minimum by implementing data retention and disposal policies, procedures and processes.', 'Data Protection'),
        ('3.1.2', 'Mask PAN when displayed (show only first 6 and last 4 digits)', 'Protect stored cardholder data through masking when displayed (the first six and last four digits are the maximum number of digits to be displayed).', 'Data Protection'),
        ('3.1.3', 'Encrypt stored CHD using strong encryption', 'Protect stored cardholder data through encryption with strong cryptography and security management processes and procedures.', 'Data Protection'),
        
        # Requirement 4: Protect Cardholder Data with Strong Cryptography During Transmission
        ('4.1.1', 'Use TLS 1.2 or higher for all CHD transmissions', 'Use strong cryptography and security protocols such as TLS to safeguard sensitive cardholder data during transmission over open, public networks.', 'Data Transmission'),
        ('4.1.2', 'Disable insecure protocols (SSL, TLS 1.0/1.1, SSH v1)', 'Never send unprotected PANs by end-user messaging technologies (for example, e-mail, instant messaging, SMS, chat, etc.).', 'Data Transmission'),
        ('4.1.3', 'Verify certificates are valid and not self-signed', 'Ensure proper certificate management and validation for all encrypted connections.', 'Data Transmission'),
        
        # Requirement 5: Protect Systems and Networks from Malicious Software
        ('5.1.1', 'Install and update anti-malware software', 'Deploy anti-virus software on all systems commonly affected by malicious software (particularly personal computers and servers).', 'Malware Protection'),
        ('5.1.2', 'Perform regular scans and monitor alerts', 'Ensure that anti-virus programs are capable of detecting, removing, and protecting against all known types of malicious software.', 'Malware Protection'),
        ('5.1.3', 'Restrict administrative access for malware controls', 'Ensure that anti-virus mechanisms are actively running and cannot be disabled or altered by users, unless specifically authorized by management on a case-by-case basis for a limited time period.', 'Malware Protection'),
        
        # Requirement 6: Develop and Maintain Secure Systems and Applications
        ('6.1.1', 'Apply security patches within 30 days of release', 'Establish a process to identify security vulnerabilities, using reputable outside sources for security vulnerability information, and assign a risk ranking to newly discovered security vulnerabilities.', 'Secure Development'),
        ('6.1.2', 'Perform vulnerability scans and code reviews', 'Ensure that all system components and software are protected from known vulnerabilities by installing applicable vendor-supplied security patches.', 'Secure Development'),
        ('6.1.3', 'Use secure coding practices (OWASP Top 10)', 'Develop internal and external software applications (including web-based administrative access to applications) securely and in accordance with PCI DSS and based on industry standards and/or best practices.', 'Secure Development'),
        
        # Requirement 7: Restrict Access to System Components and Cardholder Data
        ('7.1.1', 'Access granted only on a need-to-know basis', 'Limit access to system components and cardholder data to only those individuals whose job requires such access.', 'Access Control'),
        ('7.1.2', 'Role-based access control implemented', 'Establish an access control system(s) for systems components that restricts access based on a user\'s need to know, and is set to "deny all" unless specifically allowed.', 'Access Control'),
        ('7.1.3', 'Access rights reviewed at least quarterly', 'Document and review access rights at least every six months to ensure access remains appropriate for an individual\'s job function.', 'Access Control'),
        
        # Requirement 8: Identify Users and Authenticate Access to System Components
        ('8.1.1', 'Assign unique IDs to each user', 'Define and implement policies and procedures to ensure proper user identification management for non-consumer users and administrators on all system components.', 'User Authentication'),
        ('8.1.2', 'Enforce multi-factor authentication (MFA) for remote and administrative access', 'In addition to assigning a unique ID, ensure proper user-authentication management for non-consumer users and administrators on all system components by employing at least one of the following methods to authenticate all users.', 'User Authentication'),
        ('8.1.3', 'Lock accounts after multiple failed attempts', 'Implement account lockout after a maximum of six failed attempts, with lockout duration of at least 30 minutes or until administrator enables the user ID.', 'User Authentication'),
        
        # Requirement 9: Restrict Physical Access to Cardholder Data
        ('9.1.1', 'Secure areas containing CHD with locks or access controls', 'Use appropriate facility entry controls to limit and monitor physical access to systems in the cardholder data environment.', 'Physical Security'),
        ('9.1.2', 'Maintain visitor logs', 'Develop procedures to easily distinguish between onsite personnel and visitors, to include identifying onsite personnel and visitors and changing access requirements.', 'Physical Security'),
        ('9.1.3', 'Destroy media containing CHD when no longer needed', 'Physically secure all media and ensure all media containing cardholder data is classified so the sensitivity of the data can be determined.', 'Physical Security'),
        
        # Requirement 10: Log and Monitor All Access to System Components and CHD
        ('10.1.1', 'Enable centralized logging (SIEM or equivalent)', 'Implement audit trails to link all access to system components to each individual user.', 'Logging and Monitoring'),
        ('10.1.2', 'Review logs daily', 'Implement automated audit trails for all system components to reconstruct events, including access to cardholder data and actions taken by any individual with root or administrative privileges.', 'Logging and Monitoring'),
        ('10.1.3', 'Retain logs for at least 12 months', 'Secure audit trails so they cannot be altered and retain audit trail history for at least one year, with a minimum of three months immediately available for analysis.', 'Logging and Monitoring'),
        
        # Requirement 11: Test Security of Systems and Networks Regularly
        ('11.1.1', 'Perform quarterly internal and external vulnerability scans', 'Implement a process to test for the presence of wireless access points (802.11), and detect and identify all authorized and unauthorized wireless access points on a quarterly basis.', 'Security Testing'),
        ('11.1.2', 'Conduct annual penetration tests', 'Run internal and external network vulnerability scans at least quarterly and after any significant change in the network.', 'Security Testing'),
        ('11.1.3', 'Test intrusion detection/prevention systems', 'Perform external penetration testing at least annually and after any significant infrastructure or application upgrade or modification.', 'Security Testing'),
        
        # Requirement 12: Support Information Security with Policies and Programs
        ('12.1.1', 'Maintain a written information security policy', 'Establish, publish, maintain, and disseminate a security policy that addresses all PCI DSS requirements and defines information security roles and responsibilities for all personnel.', 'Security Policies'),
        ('12.1.2', 'Train staff annually on PCI DSS security practices', 'Implement a formal security awareness program to make all personnel aware of the cardholder data security policy and procedures.', 'Security Policies'),
        ('12.1.3', 'Assign a person responsible for PCI DSS compliance', 'Establish usage policies for critical technologies and define proper use of these technologies (for example, remote access, wireless technologies, removable electronic media, laptops, tablets, handheld devices and email).', 'Security Policies')
    ]
    
    for requirement_id, title, description, category in requirements:
        conn.execute('''
            INSERT OR IGNORE INTO pci_requirements (requirement_id, title, description, category)
            VALUES (?, ?, ?, ?)
        ''', (requirement_id, title, description, category))
    
    conn.commit()

# Authentication helper functions
def login_required(f):
    """Decorator to require login for routes"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes (shortened version for testing)
@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with PCI DSS compliance overview"""
    conn = get_db_connection()
    
    # Get requirement statistics
    total_requirements = conn.execute('SELECT COUNT(*) as count FROM pci_requirements').fetchone()['count']
    compliant_requirements = conn.execute("SELECT COUNT(*) as count FROM pci_requirements WHERE status = 'Compliant'").fetchone()['count']
    non_compliant_requirements = conn.execute("SELECT COUNT(*) as count FROM pci_requirements WHERE status = 'Not Compliant'").fetchone()['count']
    not_applicable_requirements = conn.execute("SELECT COUNT(*) as count FROM pci_requirements WHERE status = 'Not Applicable'").fetchone()['count']
    not_assessed_requirements = conn.execute("SELECT COUNT(*) as count FROM pci_requirements WHERE status = 'Not Assessed'").fetchone()['count']
    
    # Get risk statistics
    total_risks = conn.execute('SELECT COUNT(*) as count FROM risks').fetchone()['count']
    high_risks = conn.execute('SELECT COUNT(*) as count FROM risks WHERE risk_score >= 15').fetchone()['count']
    medium_risks = conn.execute('SELECT COUNT(*) as count FROM risks WHERE risk_score >= 8 AND risk_score < 15').fetchone()['count']
    low_risks = conn.execute('SELECT COUNT(*) as count FROM risks WHERE risk_score < 8').fetchone()['count']
    
    # Get Cardholder Data Tracking statistics
    total_cardholder_data_types = conn.execute('SELECT COUNT(*) as count FROM cardholder_data_tracking').fetchone()['count']
    
    # Get Service Provider statistics
    total_service_providers = conn.execute('SELECT COUNT(*) as count FROM service_providers').fetchone()['count']
    active_service_providers = conn.execute("SELECT COUNT(*) as count FROM service_providers WHERE contract_status = 'Active'").fetchone()['count']
    
    # Get recent activity
    recent_requirements = conn.execute('''
        SELECT requirement_id, title, status, assessed_at 
        FROM pci_requirements 
        WHERE assessed_at IS NOT NULL 
        ORDER BY assessed_at DESC 
        LIMIT 5
    ''').fetchall()
    
    # Calculate compliance percentage
    assessed_requirements = total_requirements - not_assessed_requirements
    compliance_percentage = round((compliant_requirements / assessed_requirements * 100) if assessed_requirements > 0 else 0, 1)
    
    # Get current date and time
    current_date = datetime.now().strftime('%d %B %Y')
    current_time = datetime.now().strftime('%H:%M')
    
    conn.close()
    
    return render_template('dashboard.html',
                         total_requirements=total_requirements,
                         compliant_requirements=compliant_requirements,
                         non_compliant_requirements=non_compliant_requirements,
                         not_applicable_requirements=not_applicable_requirements,
                         not_assessed_requirements=not_assessed_requirements,
                         compliance_percentage=compliance_percentage,
                         total_risks=total_risks,
                         high_risks=high_risks,
                         medium_risks=medium_risks,
                         low_risks=low_risks,
                         total_cardholder_data_types=total_cardholder_data_types,
                         total_service_providers=total_service_providers,
                         active_service_providers=active_service_providers,
                         recent_requirements=recent_requirements,
                         current_date=current_date,
                         current_time=current_time)

@app.route('/audit')
@login_required
def audit_checklist():
    """PCI DSS requirements checklist"""
    conn = get_db_connection()
    
    # Get all requirements grouped by category
    requirements = conn.execute('''
        SELECT * FROM pci_requirements 
        ORDER BY category, requirement_id
    ''').fetchall()
    
    # Group by category
    categories = {}
    for req in requirements:
        if req['category'] not in categories:
            categories[req['category']] = []
        categories[req['category']].append(req)
    
    conn.close()
    
    return render_template('audit_checklist.html', categories=categories)

@app.route('/audit/update', methods=['POST'])
@login_required
def update_requirement():
    """Update requirement status and notes"""
    requirement_id = request.form['requirement_id']
    status = request.form['status']
    notes = request.form['notes']
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE pci_requirements 
        SET status = ?, notes = ?, assessed_by = ?, assessed_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
        WHERE requirement_id = ?
    ''', (status, notes, session['username'], requirement_id))
    conn.commit()
    conn.close()
    
    flash('Requirement updated successfully!', 'success')
    return redirect(url_for('audit_checklist'))

@app.route('/evidence')
@login_required
def evidence():
    """Evidence management for PCI DSS requirements"""
    conn = get_db_connection()
    
    # Get all evidence with requirement details
    evidence_list = conn.execute('''
        SELECT e.*, h.title as requirement_title, h.requirement_id
        FROM evidence e
        JOIN pci_requirements h ON e.requirement_id = h.requirement_id
        ORDER BY e.uploaded_at DESC
    ''').fetchall()
    
    # Get requirements for dropdown
    requirements = conn.execute('SELECT requirement_id, title FROM pci_requirements ORDER BY requirement_id').fetchall()
    
    # Calculate today's uploads
    today = datetime.now().strftime('%Y-%m-%d')
    today_uploads = sum(1 for e in evidence_list if e['uploaded_at'] and str(e['uploaded_at'])[:10] == today)
    
    conn.close()
    
    return render_template('evidence.html', evidence_list=evidence_list, requirements=requirements, today_uploads=today_uploads)

@app.route('/evidence/upload', methods=['POST'])
@login_required
def upload_evidence():
    """Upload evidence file"""
    if 'file' not in request.files:
        flash('No file selected!', 'error')
        return redirect(url_for('evidence'))
    
    file = request.files['file']
    requirement_id = request.form['requirement_id']
    description = request.form.get('description', '')
    
    if file.filename == '':
        flash('No file selected!', 'error')
        return redirect(url_for('evidence'))
    
    if file:
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO evidence (requirement_id, filename, original_filename, file_path, file_size, description, uploaded_by)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (requirement_id, unique_filename, filename, file_path, file_size, description, session['username']))
        conn.commit()
        conn.close()
        
        flash('Evidence uploaded successfully!', 'success')
    
    return redirect(url_for('evidence'))

@app.route('/evidence/download/<int:evidence_id>')
@login_required
def download_evidence(evidence_id):
    """Download evidence file"""
    conn = get_db_connection()
    evidence = conn.execute('SELECT * FROM evidence WHERE id = ?', (evidence_id,)).fetchone()
    conn.close()
    
    if evidence:
        return send_file(evidence['file_path'], as_attachment=True, download_name=evidence['original_filename'])
    
    flash('Evidence not found!', 'error')
    return redirect(url_for('evidence'))

@app.route('/evidence/delete/<int:evidence_id>', methods=['POST'])
@login_required
def delete_evidence(evidence_id):
    """Delete evidence file"""
    conn = get_db_connection()
    evidence = conn.execute('SELECT * FROM evidence WHERE id = ?', (evidence_id,)).fetchone()
    
    if evidence:
        # Delete file from filesystem
        try:
            os.remove(evidence['file_path'])
        except:
            pass
        
        # Delete from database
        conn.execute('DELETE FROM evidence WHERE id = ?', (evidence_id,))
        conn.commit()
        flash('Evidence deleted successfully!', 'success')
    else:
        flash('Evidence not found!', 'error')
    
    conn.close()
    return redirect(url_for('evidence'))

@app.route('/risks')
@login_required
def risk_register():
    """Risk register for PCI DSS compliance"""
    conn = get_db_connection()
    
    risks = conn.execute('''
        SELECT * FROM risks 
        ORDER BY risk_score DESC, created_at DESC
    ''').fetchall()
    
    conn.close()
    
    return render_template('risk_register.html', risks=risks)

@app.route('/risks/add', methods=['POST'])
@login_required
def add_risk():
    """Add new risk to register"""
    title = request.form['title']
    description = request.form['description']
    likelihood = int(request.form['likelihood'])
    impact = int(request.form['impact'])
    mitigation = request.form.get('mitigation', '')
    owner = request.form.get('owner', '')
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO risks (title, description, likelihood, impact, mitigation, owner, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, description, likelihood, impact, mitigation, owner, session['username']))
    conn.commit()
    conn.close()
    
    flash('Risk added successfully!', 'success')
    return redirect(url_for('risk_register'))

@app.route('/risks/update/<int:risk_id>', methods=['POST'])
@login_required
def update_risk(risk_id):
    """Update existing risk"""
    title = request.form['title']
    description = request.form['description']
    likelihood = int(request.form['likelihood'])
    impact = int(request.form['impact'])
    mitigation = request.form.get('mitigation', '')
    owner = request.form.get('owner', '')
    status = request.form.get('status', 'Open')
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE risks 
        SET title = ?, description = ?, likelihood = ?, impact = ?, mitigation = ?, owner = ?, status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (title, description, likelihood, impact, mitigation, owner, status, risk_id))
    conn.commit()
    conn.close()
    
    flash('Risk updated successfully!', 'success')
    return redirect(url_for('risk_register'))

@app.route('/risks/delete/<int:risk_id>', methods=['POST'])
@login_required
def delete_risk(risk_id):
    """Delete risk from register"""
    conn = get_db_connection()
    conn.execute('DELETE FROM risks WHERE id = ?', (risk_id,))
    conn.commit()
    conn.close()
    
    flash('Risk deleted successfully!', 'success')
    return redirect(url_for('risk_register'))

@app.route('/cardholder-data-tracking')
@login_required
def cardholder_data_tracking():
    """Cardholder Data Tracking and Management"""
    conn = get_db_connection()
    
    cardholder_data_types = conn.execute('SELECT * FROM cardholder_data_tracking ORDER BY created_at DESC').fetchall()
    
    conn.close()
    
    return render_template('cardholder_data_tracking.html', cardholder_data_types=cardholder_data_types)

@app.route('/cardholder-data-tracking/add', methods=['POST'])
@login_required
def add_cardholder_data_type():
    """Add new cardholder data type"""
    data_type = request.form['data_type']
    description = request.form.get('description', '')
    classification = request.form['classification']
    storage_location = request.form.get('storage_location', '')
    encryption_status = request.form.get('encryption_status', '')
    disposal_procedures = request.form.get('disposal_procedures', '')
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO cardholder_data_tracking (data_type, description, classification, storage_location, encryption_status, disposal_procedures)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (data_type, description, classification, storage_location, encryption_status, disposal_procedures))
    conn.commit()
    conn.close()
    
    flash('Cardholder data type added successfully!', 'success')
    return redirect(url_for('cardholder_data_tracking'))

@app.route('/cardholder-data-tracking/update/<int:data_id>', methods=['POST'])
@login_required
def update_cardholder_data_type(data_id):
    """Update existing cardholder data type"""
    data_type = request.form['data_type']
    description = request.form.get('description', '')
    classification = request.form['classification']
    storage_location = request.form.get('storage_location', '')
    encryption_status = request.form.get('encryption_status', '')
    disposal_procedures = request.form.get('disposal_procedures', '')
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE cardholder_data_tracking 
        SET data_type = ?, description = ?, classification = ?, storage_location = ?, encryption_status = ?, disposal_procedures = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (data_type, description, classification, storage_location, encryption_status, disposal_procedures, data_id))
    conn.commit()
    conn.close()
    
    flash('Cardholder data type updated successfully!', 'success')
    return redirect(url_for('cardholder_data_tracking'))

@app.route('/cardholder-data-tracking/delete/<int:data_id>', methods=['POST'])
@login_required
def delete_cardholder_data_type(data_id):
    """Delete cardholder data type"""
    conn = get_db_connection()
    conn.execute('DELETE FROM cardholder_data_tracking WHERE id = ?', (data_id,))
    conn.commit()
    conn.close()
    
    flash('Cardholder data type deleted successfully!', 'success')
    return redirect(url_for('cardholder_data_tracking'))

@app.route('/service-providers')
@login_required
def service_providers():
    """Service Provider management"""
    conn = get_db_connection()
    
    service_providers_list = conn.execute('SELECT * FROM service_providers ORDER BY created_at DESC').fetchall()
    
    conn.close()
    
    return render_template('service_providers.html', service_providers=service_providers_list)

@app.route('/service-providers/add', methods=['POST'])
@login_required
def add_service_provider():
    """Add new Service Provider"""
    name = request.form['name']
    contact_person = request.form.get('contact_person', '')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    contract_status = request.form.get('contract_status', 'Active')
    compliance_status = request.form.get('compliance_status', 'Not Assessed')
    pci_level = request.form.get('pci_level', '')
    last_assessment_date = request.form.get('last_assessment_date')
    next_assessment_date = request.form.get('next_assessment_date')
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO service_providers (name, contact_person, email, phone, contract_status, compliance_status, pci_level, last_assessment_date, next_assessment_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, contact_person, email, phone, contract_status, compliance_status, pci_level, last_assessment_date, next_assessment_date))
    conn.commit()
    conn.close()
    
    flash('Service Provider added successfully!', 'success')
    return redirect(url_for('service_providers'))

@app.route('/service-providers/edit/<int:sp_id>', methods=['POST'])
@login_required
def edit_service_provider(sp_id):
    """Edit Service Provider"""
    name = request.form['name']
    contact_person = request.form.get('contact_person', '')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    contract_status = request.form.get('contract_status', 'Active')
    compliance_status = request.form.get('compliance_status', 'Not Assessed')
    pci_level = request.form.get('pci_level', '')
    last_assessment_date = request.form.get('last_assessment_date')
    next_assessment_date = request.form.get('next_assessment_date')
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE service_providers 
        SET name = ?, contact_person = ?, email = ?, phone = ?, contract_status = ?, compliance_status = ?, pci_level = ?, last_assessment_date = ?, next_assessment_date = ?
        WHERE id = ?
    ''', (name, contact_person, email, phone, contract_status, compliance_status, pci_level, last_assessment_date, next_assessment_date, sp_id))
    conn.commit()
    conn.close()
    
    flash('Service Provider updated successfully!', 'success')
    return redirect(url_for('service_providers'))

@app.route('/service-providers/delete/<int:sp_id>', methods=['POST'])
@login_required
def delete_service_provider(sp_id):
    """Delete Service Provider"""
    conn = get_db_connection()
    conn.execute('DELETE FROM service_providers WHERE id = ?', (sp_id,))
    conn.commit()
    conn.close()
    
    flash('Service Provider deleted successfully!', 'success')
    return redirect(url_for('service_providers'))

@app.route('/reports')
@login_required
def reports():
    """Report generation interface"""
    conn = get_db_connection()
    
    # Get summary statistics for reports
    total_requirements = conn.execute('SELECT COUNT(*) as count FROM pci_requirements').fetchone()['count']
    compliant_requirements = conn.execute("SELECT COUNT(*) as count FROM pci_requirements WHERE status = 'Compliant'").fetchone()['count']
    total_risks = conn.execute('SELECT COUNT(*) as count FROM risks').fetchone()['count']
    high_risks = conn.execute('SELECT COUNT(*) as count FROM risks WHERE risk_score >= 15').fetchone()['count']
    
    conn.close()
    
    return render_template('reports.html', 
                         total_requirements=total_requirements,
                         compliant_requirements=compliant_requirements,
                         total_risks=total_risks,
                         high_risks=high_risks)

@app.route('/reports/generate', methods=['POST'])
@login_required
def generate_report():
    """Generate PCI DSS compliance report"""
    try:
        report_type = request.form.get('report_type', 'compliance')
        
        conn = get_db_connection()
        
        if report_type == 'compliance':
            # Generate compliance report
            requirements = conn.execute('''
                SELECT * FROM pci_requirements 
                ORDER BY category, requirement_id
            ''').fetchall()
            
            evidence = conn.execute('''
                SELECT e.*, h.title as requirement_title 
                FROM evidence e 
                LEFT JOIN pci_requirements h ON e.requirement_id = h.requirement_id
            ''').fetchall()
            
            risks = conn.execute('SELECT * FROM risks ORDER BY risk_score DESC').fetchall()
            
            # Calculate compliance statistics
            total_requirements = len(requirements) if requirements else 0
            compliant_requirements = len([r for r in requirements if r['status'] == 'Compliant']) if requirements else 0
            non_compliant_requirements = len([r for r in requirements if r['status'] == 'Not Compliant']) if requirements else 0
            not_applicable_requirements = len([r for r in requirements if r['status'] == 'Not Applicable']) if requirements else 0
            not_assessed_requirements = len([r for r in requirements if r['status'] == 'Not Assessed']) if requirements else 0
            
            # Calculate compliance percentage
            assessed_requirements = total_requirements - not_assessed_requirements
            compliance_percentage = round((compliant_requirements / assessed_requirements * 100) if assessed_requirements > 0 else 0, 1)
            
            # Get evidence count
            evidence_count = len(evidence) if evidence else 0
            
            # Get risk statistics
            high_risks = len([r for r in risks if r['risk_score'] >= 15]) if risks else 0
            medium_risks = len([r for r in risks if 8 <= r['risk_score'] < 15]) if risks else 0
            low_risks = len([r for r in risks if r['risk_score'] < 8]) if risks else 0
            
            conn.close()
            
            return render_template('report.html',
                                 report_type='PCI DSS Compliance Report',
                                 requirements=requirements or [],
                                 evidence=evidence or [],
                                 risks=risks or [],
                                 total_requirements=total_requirements,
                                 compliant_requirements=compliant_requirements,
                                 non_compliant_requirements=non_compliant_requirements,
                                 not_applicable_requirements=not_applicable_requirements,
                                 not_assessed_requirements=not_assessed_requirements,
                                 compliance_percentage=compliance_percentage,
                                 evidence_count=evidence_count,
                                 high_risks=high_risks,
                                 medium_risks=medium_risks,
                                 low_risks=low_risks,
                                 generated_at=datetime.now(),
                                 generated_by=session['username'])
        elif report_type == 'evidence':
            # Generate evidence report
            evidence = conn.execute('''
                SELECT e.*, h.title as requirement_title 
                FROM evidence e 
                LEFT JOIN pci_requirements h ON e.requirement_id = h.requirement_id
                ORDER BY e.uploaded_at DESC
            ''').fetchall()
            
            # Calculate today's uploads
            today = datetime.now().strftime('%Y-%m-%d')
            today_uploads = sum(1 for e in evidence if e['uploaded_at'] and str(e['uploaded_at'])[:10] == today) if evidence else 0
            
            conn.close()
            
            return render_template('report.html',
                                 report_type='PCI DSS Evidence Documentation Report',
                                 evidence=evidence or [],
                                 today_uploads=today_uploads,
                                 requirements=[],
                                 risks=[],
                                 total_requirements=0,
                                 compliant_requirements=0,
                                 non_compliant_requirements=0,
                                 not_applicable_requirements=0,
                                 not_assessed_requirements=0,
                                 compliance_percentage=0,
                                 evidence_count=len(evidence) if evidence else 0,
                                 high_risks=0,
                                 medium_risks=0,
                                 low_risks=0,
                                 generated_at=datetime.now(),
                                 generated_by=session['username'])
                                 
        elif report_type == 'risk':
            # Generate risk report
            risks = conn.execute('SELECT * FROM risks ORDER BY risk_score DESC').fetchall()
            
            conn.close()
            
            return render_template('report.html',
                                 report_type='PCI DSS Risk Assessment Report',
                                 risks=risks or [],
                                 evidence=[],
                                 requirements=[],
                                 total_requirements=0,
                                 compliant_requirements=0,
                                 non_compliant_requirements=0,
                                 not_applicable_requirements=0,
                                 not_assessed_requirements=0,
                                 compliance_percentage=0,
                                 evidence_count=0,
                                 high_risks=len([r for r in risks if r['risk_score'] >= 15]) if risks else 0,
                                 medium_risks=len([r for r in risks if 8 <= r['risk_score'] < 15]) if risks else 0,
                                 low_risks=len([r for r in risks if r['risk_score'] < 8]) if risks else 0,
                                 generated_at=datetime.now(),
                                 generated_by=session['username'])
        else:
            conn.close()
            flash('Invalid report type!', 'error')
            return redirect(url_for('reports'))
            
    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'error')
        return redirect(url_for('reports'))

if __name__ == '__main__':
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
