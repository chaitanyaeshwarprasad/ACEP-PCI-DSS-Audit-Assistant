# 🐉 **ACEP PCI DSS Audit Assistant - Kali Linux**

## **🚀 One-Command Setup for Kali Linux**

This is a **complete all-in-one setup** for the ACEP PCI DSS Audit Assistant, optimized specifically for **Kali Linux** and cybersecurity professionals.

---

## **⚡ Quick Start**

### **Prerequisites**
- **Kali Linux 2023.3+** (Primary platform)
- **4GB+ RAM** recommended
- **500MB** free disk space

### **🚀 Complete Setup in One Command**
```bash
cd "PCI DSS"
chmod +x setup.sh
./setup.sh
```

**🎉 That's it! The script handles everything automatically and launches the app!**

---

## **🖥️ After Setup - Launch the App**

### **Quick Launch (Recommended)**
```bash
./run_acep_pci_dss.sh
```

### **Manual Launch**
```bash
source acep_pci_dss_venv/bin/activate
python3 app.py
```

---

## **🔐 Access & Login**

- **🌐 URL:** http://localhost:5000
- **👤 Username:** `acep`
- **🔑 Password:** `acep123`
- **🖥️ Platform:** Kali Linux optimized

---

## **📊 What You Get**

### **PCI DSS v4.0 Coverage**
- ✅ **All 12 Requirements** - Complete compliance framework
- ✅ **33 Sub-Requirements** - Detailed assessment criteria
- ✅ **Real-Time Tracking** - Live compliance status
- ✅ **Professional Reports** - Export to HTML, CSV, JSON

### **Professional Tools**
- ✅ **Evidence Management** - Secure file organization
- ✅ **Risk Assessment** - Comprehensive risk scoring
- ✅ **Service Provider Tracking** - Third-party compliance
- ✅ **Cardholder Data Protection** - CHD and SAD monitoring

---

## **🚨 Troubleshooting**

### **Setup Issues**
```bash
# Make script executable
chmod +x setup.sh

# Run with verbose output
bash -x setup.sh

# Check system requirements
free -m  # Check RAM
df -h    # Check disk space
```

### **Permission Issues**
```bash
# Fix permissions
sudo chown -R $USER:$USER .
chmod +x setup.sh run_acep_pci_dss.sh
```

### **Python Issues**
```bash
# Install Python on Kali
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Verify installation
python3 --version
```

---

## **📁 Project Structure**

```
PCI DSS/
├── 🐍 app.py                           # Main Flask application
├── 📋 requirements.txt                 # Python dependencies
├── 🚀 setup.sh                         # Complete all-in-one setup script
├── 📚 README.md                        # Documentation
├── 📋 CHANGELOG.md                     # Version history
├── 🤝 CONTRIBUTING.md                  # Contribution guidelines
├── 🗄️ database/                       # SQLite database
├── 🎨 static/                          # CSS, JS, uploads
├── 🎨 templates/                       # HTML templates
└── 📁 logs/                            # Application logs (created by setup)
```

---

## **🎯 Perfect for Kali Linux**

### **🐉 Kali Linux Integration**
- **Penetration Testing Environment** - Optimized for cybersecurity work
- **Security Tools Compatibility** - Works with Kali ecosystem
- **Professional Scripts** - Enterprise-grade automation
- **Security Focus** - Built for compliance and security assessment

---

## **🚀 Ready to Use!**

**Simply run:**
```bash
chmod +x setup.sh
./setup.sh
```

**And your PCI DSS Compliance Assistant will be fully configured and running!**

---

**🎯 Your project is now a professional, enterprise-grade compliance tool with one-command setup for Kali Linux!**

**Created by Chaitanya Eshwar Prasad**  
*Cybersecurity Professional & PCI DSS Compliance Expert*

**🌐 [chaitanyaeshwarprasad.com](https://chaitanyaeshwarprasad.com) | 💼 [LinkedIn](https://linkedin.com/in/chaitanya-eshwar-prasad) | 🐙 [GitHub](https://github.com/chaitanyaeshwarprasad)**
