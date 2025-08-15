# 🏦 ACEP PCI DSS Audit Assistant

<div align="center">

![ACEP PCI DSS Audit](https://img.shields.io/badge/ACEP-PCI%20DSS%20Audit%20Assistant-blue?style=for-the-badge&logo=shield-check&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3+-red?style=for-the-badge&logo=flask&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3+-purple?style=for-the-badge&logo=bootstrap&logoColor=white)

**Professional Payment Card Industry Compliance & PCI DSS Audit Management Tool**

*Built for cybersecurity professionals, by cybersecurity professionals*

[![Website](https://img.shields.io/badge/🌐_Website-chaitanyaeshwarprasad.com-blue?style=for-the-badge&logo=globe&logoColor=white)](https://chaitanyaeshwarprasad.com)
[![LinkedIn](https://img.shields.io/badge/💼_LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/chaitanya-eshwar-prasad)
[![GitHub](https://img.shields.io/badge/🐙_GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/chaitanyaeshwarprasad)

</div>

---

## 🎯 **What is ACEP PCI DSS Audit Assistant?**

The **ACEP PCI DSS Audit Assistant** is a comprehensive, enterprise-grade audit management system designed to streamline and automate PCI DSS (Payment Card Industry Data Security Standard) assessments. Built with modern web technologies and a focus on user experience, this tool empowers organizations to achieve and maintain full PCI DSS compliance through systematic evaluation, evidence management, and risk assessment.

**🚀 One-Command Setup:** Simply run `./setup.sh` and everything is automatically configured and ready to use!

### **🌟 Key Features**

- **🔒 Complete PCI DSS v4.0 Coverage** - All 12 requirements with 33 sub-requirements
- **📊 Real-Time Dashboard** - Live compliance status and progress tracking
- **📁 Evidence Management** - Secure file upload and organization system
- **⚠️ Risk Assessment** - Comprehensive risk scoring and mitigation tracking
- **🏢 Service Provider Management** - Complete provider compliance tracking
- **💳 Cardholder Data Tracking** - CHD and SAD monitoring and protection
- **📋 Professional Reporting** - Executive-ready compliance reports
- **📱 Modern Interface** - Responsive design for all devices

---

## 🚀 **Quick Start - Kali Linux**

### **Prerequisites**
- **Kali Linux 2023.3+** (Primary platform)
- **Python 3.8+** (3.9+ recommended)
- **4GB+ RAM** recommended
- **500MB** free disk space

### **🚀 One-Command Setup**

```bash
# 1. Navigate to project directory
cd "PCI DSS"

# 2. Make setup script executable
chmod +x setup.sh

# 3. Run complete setup (handles everything automatically)
./setup.sh
```

**🎉 That's it! The script handles everything: dependencies, Python, virtual environment, database, and launches the app!**

### **Access & Login**
- **🌐 URL:** http://localhost:5000
- **👤 Username:** `acep`
- **🔑 Password:** `acep123`
- **🖥️ Platform:** Kali Linux optimized

---

## 🏗️ **Project Architecture**

```
PCI DSS/
├── 🐍 app.py                           # Main Flask application
├── 📋 requirements.txt                 # Python dependencies
├── 🚀 setup.sh                         # Complete all-in-one setup script
├── 🚀 run_acep_pci_dss.sh             # Quick launcher script
├── 🎨 templates/                      # HTML templates
│   ├── base.html                      # Base layout template
│   ├── dashboard.html                 # Main dashboard
│   ├── audit_checklist.html           # PCI DSS requirements
│   ├── evidence.html                  # Evidence management
│   ├── risk_register.html             # Risk assessment
│   ├── cardholder_data_tracking.html  # CHD monitoring
│   ├── service_providers.html         # Service providers
│   ├── reports.html                   # Reports interface
│   └── report.html                    # Generated reports
├── 🎨 static/                         # Assets
│   ├── css/styles.css                 # Custom styling
│   ├── js/main.js                     # JavaScript
│   └── uploads/                       # File storage
├── 🗄️ database/                      # SQLite database
└── 📁 logs/                            # Application logs
```

---

## 🔒 **PCI DSS v4.0 Requirements Covered**

| Requirement | Description | Status |
|-------------|-------------|---------|
| **Req 1** | Install and Maintain Network Security Controls | ✅ Complete |
| **Req 2** | Apply Secure Configurations to All System Components | ✅ Complete |
| **Req 3** | Protect Stored Account Data | ✅ Complete |
| **Req 4** | Protect Cardholder Data with Strong Cryptography | ✅ Complete |
| **Req 5** | Protect Systems and Networks from Malicious Software | ✅ Complete |
| **Req 6** | Develop and Maintain Secure Systems and Applications | ✅ Complete |
| **Req 7** | Restrict Access to System Components and CHD | ✅ Complete |
| **Req 8** | Identify Users and Authenticate Access | ✅ Complete |
| **Req 9** | Restrict Physical Access to Cardholder Data | ✅ Complete |
| **Req 10** | Log and Monitor All Access to System Components | ✅ Complete |
| **Req 11** | Test Security of Systems and Networks Regularly | ✅ Complete |
| **Req 12** | Support Information Security with Policies | ✅ Complete |

---

## 🎨 **User Interface Features**

### **📊 Dashboard**
- **Real-time Statistics** - Live compliance metrics
- **Quick Actions** - One-click navigation
- **Progress Tracking** - Visual compliance indicators
- **Recent Activity** - Latest updates and tasks

### **📋 Requirements Assessment**
- **Interactive Checklist** - Easy compliance evaluation
- **Status Updates** - Real-time status changes
- **Requirement Details** - Comprehensive guidance
- **Progress Bars** - Visual completion tracking

### **📁 Evidence Management**
- **File Upload** - PDF, DOCX, JPG, PNG support
- **Requirement Linking** - Connect evidence to requirements
- **Search & Filter** - Advanced file organization
- **Secure Storage** - Protected file access

### **⚠️ Risk Assessment**
- **Risk Register** - Comprehensive risk identification
- **Scoring System** - Quantitative risk evaluation
- **Mitigation Tracking** - Risk reduction strategies
- **Priority Sorting** - Focus on high-impact risks

### **🏢 Service Provider Management**
- **Provider Registry** - Complete provider database
- **Compliance Status** - Track provider compliance
- **Assessment Scheduling** - Manage provider reviews
- **Contract Management** - Compliance requirements

---

## 📊 **Reporting & Analytics**

### **📋 Available Reports**
1. **PCI DSS Compliance Summary** - Complete compliance overview
2. **Risk Assessment Report** - Detailed risk analysis
3. **Evidence Documentation** - Evidence file summary

### **📤 Export Options**
- **🖨️ Print Report** - Professional PDF-ready format
- **📊 Export CSV** - Spreadsheet-compatible data
- **🌐 Export HTML** - Standalone web report
- **📄 Export JSON** - Machine-readable format
- **🔗 Copy Link** - Shareable report URL

---

## 🛠️ **Technology Stack**

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Backend** | Flask | 2.3.3 | Web framework |
| **Database** | SQLite | Built-in | Data storage |
| **Frontend** | HTML5 + Bootstrap 5 | Latest | UI components |
| **Styling** | Custom CSS3 | Modern | Professional theme |
| **JavaScript** | ES6+ | Modern | Interactive features |
| **Templates** | Jinja2 | 3.1.2 | Dynamic content |

---

## 🔧 **Development & Customization**

### **After Setup - Quick Launch**
```bash
# Quick launch (if already set up)
./run_acep_pci_dss.sh

# Or manual launch
source acep_pci_dss_venv/bin/activate
python3 app.py
```

### **Development Mode**
```bash
# Set development environment
export FLASK_ENV=development
export FLASK_DEBUG=1

# Run with auto-reload
python3 app.py
```

### **Database Management**
```bash
# Reset database (if needed)
rm database/pci_dss_audit.db
python3 app.py

# Backup database
cp database/pci_dss_audit.db database/pci_dss_audit_backup.db
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **Setup Script Issues**
```bash
# Make script executable
chmod +x setup.sh

# Run with verbose output
bash -x setup.sh

# Check system requirements
free -m  # Check RAM
df -h    # Check disk space
```

#### **Python Not Found**
```bash
# Install Python on Kali Linux
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Verify installation
python3 --version
```

#### **Module Not Found**
```bash
# Activate virtual environment
source acep_pci_dss_venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### **Port Already in Use**
```bash
# Kill process using port 5000
sudo netstat -tulpn | grep :5000
sudo kill -9 <PID>

# Or change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

#### **Permission Issues**
```bash
# Fix permissions
sudo chown -R $USER:$USER .
chmod +x setup.sh run_acep_pci_dss.sh
```

---

## 👨‍💻 **Creator & Maintainer**

<div align="center">

### **👤 Chaitanya Eshwar Prasad**
**Cybersecurity Professional & PCI DSS Compliance Expert**

> *"Empowering organizations with modern, efficient compliance tools that protect cardholder data and ensure regulatory adherence."*

### **🌐 Connect & Follow**

| Platform | Link | Description |
|----------|------|-------------|
| **🌐 Website** | [chaitanyaeshwarprasad.com](https://chaitanyaeshwarprasad.com) | Personal portfolio and cybersecurity blog |
| **💼 LinkedIn** | [linkedin.com/in/chaitanya-eshwar-prasad](https://linkedin.com/in/chaitanya-eshwar-prasad) | Professional network and updates |
| **🐙 GitHub** | [github.com/chaitanyaeshwarprasad](https://github.com/chaitanyaeshwarprasad) | Open source projects and code |
| **🎥 YouTube** | [youtube.com/@chaitanya.eshwar.prasad](https://youtube.com/@chaitanya.eshwar.prasad) | Cybersecurity tutorials and insights |
| **📸 Instagram** | [instagram.com/acep.tech.in.telugu](https://instagram.com/acep.tech.in.telugu) | Tech insights and updates |
| **🛡️ YesWeHack** | [yeswehack.com/hunters/chaitanya-eshwar-prasad](https://yeswehack.com/hunters/chaitanya-eshwar-prasad) | Bug bounty and security research |

</div>

---

## 🤝 **Contributing**

We welcome contributions from the cybersecurity and compliance communities!

### **How to Contribute**
1. **Fork** the project
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

### **Areas for Contribution**
- **Security Enhancements** - Additional security features
- **PCI DSS Updates** - Keep up with standard changes
- **Performance Optimization** - Improve application speed
- **UI/UX Improvements** - Better user experience
- **Documentation** - User guides and technical docs

---

## 📞 **Support & Help**

### **Getting Help**
- **📖 Documentation** - Check this README first
- **🐛 Issues** - Report bugs through GitHub
- **💬 Discussions** - Join community discussions
- **📧 Contact** - Reach out via LinkedIn

### **Community**
- **⭐ Star** the project on GitHub
- **🔄 Share** with cybersecurity colleagues
- **📢 Mention** in your compliance projects
- **🏢 Deploy** in your organization

---



---

<div align="center">

## 🎉 **Thank You!**

**Thank you for choosing ACEP PCI DSS Audit Assistant!**

Our mission is to **democratize PCI DSS compliance** by providing professional-grade tools that make payment card industry compliance accessible, efficient, and effective for organizations of all sizes.

---

**🏦 Built with ❤️ for PCI DSS Compliance**

**🔒 Secure • Professional • Reliable • Compliant**

**Created by Chaitanya Eshwar Prasad**

🌐 [chaitanyaeshwarprasad.com](https://chaitanyaeshwarprasad.com) | 💼 [LinkedIn](https://linkedin.com/in/chaitanya-eshwar-prasad) | 🐙 [GitHub](https://github.com/chaitanyaeshwarprasad)

🎥 [YouTube](https://youtube.com/@chaitanya.eshwar.prasad) | 📸 [Instagram](https://instagram.com/acep.tech.in.telugu) | 🛡️ [YesWeHack](https://yeswehack.com/hunters/chaitanya-eshwar-prasad)

---

**🌟 Join thousands of organizations using ACEP PCI DSS Audit Assistant!**

*Empowering cybersecurity professionals with modern, efficient PCI DSS compliance tools since 2024*

</div>