#!/bin/bash

# ACEP PCI DSS AUDIT ASSISTANT - Complete All-in-One Setup Script
# Created by Chaitanya Eshwar Prasad
# This script handles everything: system setup, Python installation, dependencies, and app setup

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

print_header() {
    echo -e "${CYAN}[HEADER]${NC} $1"
}

# Banner
echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                 ACEP PCI DSS Audit Assistant            ║"
echo "║                 Complete All-in-One Setup Script             ║"
echo "║                                                              ║"
echo "║  This script will automatically:                             ║"
echo "║  1. Check system requirements                                ║"
echo "║  2. Install system dependencies                              ║"
echo "║  3. Install Python if needed                                 ║"
echo "║  4. Create virtual environment                               ║"
echo "║  5. Install Python packages                                  ║"
echo "║  6. Set up database                                          ║"
echo "║  7. Configure application                                    ║"
echo "║  8. Launch the application                                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_warning "This script should not be run as root. Please run as a regular user."
   exit 1
fi

# Check if running on Kali Linux
print_step "Step 1: Checking system requirements..."
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
    print_status "Detected OS: $OS $VER"
    
    if [[ "$OS" != *"Kali"* ]]; then
        print_warning "This script is optimized for Kali Linux. Other distributions may work but are not guaranteed."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_error "Setup cancelled by user."
            exit 1
        fi
    fi
else
    print_error "Cannot detect OS. This script is designed for Linux distributions."
    exit 1
fi

# Check system resources
print_step "Step 2: Checking system resources..."
TOTAL_MEM=$(free -m | awk 'NR==2{printf "%.0f", $2}')
TOTAL_DISK=$(df -m . | awk 'NR==2{printf "%.0f", $4}')

print_status "Available RAM: ${TOTAL_MEM}MB"
print_status "Available Disk Space: ${TOTAL_DISK}MB"

if [ $TOTAL_MEM -lt 2048 ]; then
    print_warning "Warning: Less than 2GB RAM available. Performance may be affected."
fi

if [ $TOTAL_DISK -lt 500 ]; then
    print_error "Error: Less than 500MB disk space available. Please free up space and try again."
    exit 1
fi

# Determine package manager
print_step "Step 3: Detecting package manager..."
if command -v apt &> /dev/null; then
    PKG_MANAGER="apt"
    PKG_INSTALL="sudo apt install -y"
    PKG_UPDATE="sudo apt update"
    PKG_UPGRADE="sudo apt upgrade -y"
    PYTHON_PKG="python3 python3-pip python3-venv python3-dev"
elif command -v yum &> /dev/null; then
    PKG_MANAGER="yum"
    PKG_INSTALL="sudo yum install -y"
    PKG_UPDATE="sudo yum update -y"
    PKG_UPGRADE="sudo yum upgrade -y"
    PYTHON_PKG="python3 python3-pip python3-venv python3-devel"
elif command -v dnf &> /dev/null; then
    PKG_MANAGER="dnf"
    PKG_INSTALL="sudo dnf install -y"
    PKG_UPDATE="sudo dnf update -y"
    PKG_UPGRADE="sudo dnf upgrade -y"
    PYTHON_PKG="python3 python3-pip python3-venv python3-devel"
else
    print_error "No supported package manager found. Please install Python 3.8+ manually."
    exit 1
fi

print_success "Package manager detected: $PKG_MANAGER"

# Update system packages
print_step "Step 4: Updating system packages..."
print_status "Updating package lists..."
$PKG_UPDATE

print_status "Upgrading system packages..."
$PKG_UPGRADE

# Install system dependencies
print_step "Step 5: Installing system dependencies..."
print_status "Installing system packages..."
$PKG_INSTALL $PYTHON_PKG

# Install additional tools
print_status "Installing additional tools..."
$PKG_INSTALL sqlite3 curl wget git build-essential

# Check Python installation
print_step "Step 6: Verifying Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python $PYTHON_VERSION is installed"
    
    # Check Python version
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
        print_success "Python version meets requirements (3.8+)"
    else
        print_error "Python version $PYTHON_VERSION does not meet minimum requirement (3.8+)"
        exit 1
    fi
else
    print_error "Python 3 installation failed. Please install manually."
    exit 1
fi

# Create project directories
print_step "Step 7: Creating project directories..."
print_status "Creating necessary directories..."
mkdir -p database
mkdir -p static/uploads
mkdir -p logs

# Create virtual environment
print_step "Step 8: Setting up Python virtual environment..."
if [ -d "acep_pci_dss_venv" ]; then
    print_warning "Virtual environment already exists. Removing old one..."
    rm -rf acep_pci_dss_venv
fi

print_status "Creating virtual environment..."
python3 -m venv acep_pci_dss_venv

print_status "Activating virtual environment..."
source acep_pci_dss_venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_step "Step 9: Installing Python dependencies..."
print_status "Installing requirements..."
pip install -r requirements.txt

# Create configuration file
print_step "Step 10: Creating configuration file..."
cat > config.py << 'EOF'
# ACEP PCI DSS Audit Assistant - Configuration File
# Created by Chaitanya Eshwar Prasad

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Application Settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'acep-pci-dss-secret-key-2024'
    APP_NAME = 'ACEP PCI DSS Audit Assistant'
    APP_VERSION = '2.0.0'
    
    # Database Settings
    DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'pci_dss_audit.db')
    
    # File Upload Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx'}
    
    # Session Settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)  # 8 hour session timeout
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    
    # Security Settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour CSRF token expiry
    
    # Pagination Settings
    ITEMS_PER_PAGE = 20
    
    # Report Settings
    REPORT_EXPORT_FORMATS = ['html', 'csv', 'json', 'pdf']
    REPORT_MAX_SIZE = 10 * 1024 * 1024  # 10MB max report size
    
    # Logging Settings
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/pci_dss.log'
    
    # PCI DSS Specific Settings
    PCI_DSS_VERSION = '4.0'
    PCI_DSS_REQUIREMENTS_COUNT = 12
    PCI_DSS_SUB_REQUIREMENTS_COUNT = 33
    
    # Risk Assessment Settings
    RISK_SCORE_MIN = 1
    RISK_SCORE_MAX = 25
    RISK_LEVELS = {
        'Low': (1, 7),
        'Medium': (8, 14),
        'High': (15, 25)
    }
    
    # Compliance Status Options
    COMPLIANCE_STATUSES = [
        'Compliant',
        'Non-Compliant', 
        'Not Applicable',
        'Not Assessed'
    ]

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    LOG_LEVEL = 'WARNING'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    DATABASE = ':memory:'  # Use in-memory database for testing

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'default')
    return config.get(env, config['default'])
EOF

print_success "Configuration file created"

# Create launcher script
print_step "Step 11: Creating launcher script..."
cat > run_acep_pci_dss.sh << 'EOF'
#!/bin/bash

# ACEP PCI DSS Audit Assistant - Quick Launcher
# Created by Chaitanya Eshwar Prasad

echo "🏦 ACEP PCI DSS AUDIT ASSISTANT"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ -d "acep_pci_dss_venv" ]; then
    echo "✅ Virtual environment found"
    echo "🚀 Activating virtual environment..."
    source acep_pci_dss_venv/bin/activate
    
    echo "🔧 Starting PCI DSS Compliance Assistant..."
    echo "🌐 Access at: http://localhost:5000"
    echo "👤 Default login: acep / acep123"
    echo ""
    echo "Press Ctrl+C to stop the application"
    echo ""
    
    python3 app.py
else
    echo "❌ Virtual environment not found"
    echo "🔧 Please run the setup script first:"
    echo "   ./setup.sh"
    echo ""
    echo "Or create the virtual environment manually:"
    echo "   python3 -m venv acep_pci_dss_venv"
    echo "   source acep_pci_dss_venv/bin/activate"
    echo "   pip install -r requirements.txt"
    echo "   python3 app.py"
fi
EOF

chmod +x run_acep_pci_dss.sh
print_success "Launcher script created"

# Create database
print_step "Step 12: Setting up database..."
print_status "Creating database..."
python3 -c "
from app import app, init_database
with app.app_context():
    init_database()
    print('Database initialized successfully')
"

# Create log file
print_status "Creating log file..."
touch logs/pci_dss.log
chmod 644 logs/pci_dss.log

# Set file permissions
print_step "Step 13: Setting file permissions..."
print_status "Setting file permissions..."
chmod +x setup.sh
chmod +x run_acep_pci_dss.sh
chmod 644 config.py
chmod 644 requirements.txt

# Create systemd service (optional)
print_step "Step 14: Creating systemd service (optional)..."
if command -v systemctl &> /dev/null; then
    print_status "Creating systemd service..."
    sudo tee /etc/systemd/system/acep-pci-dss.service > /dev/null << EOF
[Unit]
Description=ACEP PCI DSS Audit Assistant
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/acep_pci_dss_venv/bin
ExecStart=$(pwd)/acep_pci_dss_venv/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    print_status "Reloading systemd..."
    sudo systemctl daemon-reload
    
    print_status "Enabling service..."
    sudo systemctl enable acep-pci-dss.service
    
    print_success "Systemd service created and enabled"
    print_status "You can now use: sudo systemctl start/stop/restart acep-pci-dss"
else
    print_warning "Systemd not available, skipping service creation"
fi

# Success message
echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🎉 SETUP COMPLETE! 🎉                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

print_success "ACEP PCI DSS Audit Assistant has been set up successfully!"
print_status "You can now run the application using: ./run_acep_pci_dss.sh"
print_status "Or manually with: source acep_pci_dss_venv/bin/activate && python3 app.py"

# Launch application
print_step "Step 15: Launching the application..."
print_status "Starting ACEP PCI DSS Audit Assistant..."
echo ""
echo "🌐 Access at: http://localhost:5000"
echo "👤 Default login: acep / acep123"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Start the application
python3 app.py
