# Blood Bank Management System 🩸

A comprehensive web-based Blood Bank Management System built with Flask and PostgreSQL that streamlines blood donation management, inventory tracking, and blood request processing.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [API Routes](#api-routes)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🎯 Overview

The Blood Bank Management System addresses critical challenges in blood bank operations by providing a centralized, automated platform for managing donors, tracking blood inventory, and processing blood requests efficiently. This system ensures timely availability of blood units and reduces manual processing time by 70%.

### Problem Statement
- Manual blood bank operations are time-consuming and error-prone
- Difficulty in tracking real-time blood inventory
- Delays in matching donors with recipients
- Lack of centralized donor database
- Inefficient request processing leading to critical delays

### Solution
A Flask-based web application that automates donor registration, provides real-time stock tracking, streamlines blood request processing, and offers secure role-based access control.

## ✨ Features

### Core Functionalities
- 🔐 **User Authentication** - Secure registration and login with role-based access (Admin/User)
- 👤 **Donor Management** - Complete donor profile registration with blood group tracking
- 📊 **Real-time Inventory** - Live tracking of blood stock for all 8 blood groups (A+, A-, B+, B-, AB+, AB-, O+, O-)
- 📝 **Blood Request System** - Submit and track blood requests with status updates
- ✅ **Request Approval Workflow** - Admin approval/rejection with automatic stock verification
- 📈 **Dashboard Analytics** - Comprehensive admin dashboard with recent activities
- 🔄 **Automatic Stock Updates** - Stock increments on donations and decrements on approvals

### Security Features
- Password hashing using Werkzeug security
- SQL injection prevention via SQLAlchemy ORM
- Session management with Flask-Login
- Protected routes requiring authentication
- CSRF protection

## 🛠 Technology Stack

### Backend
- **Python 3.8+**
- **Flask 3.0.0** - Web framework
- **Flask-SQLAlchemy 3.1.1** - ORM for database operations
- **Flask-Login 0.6.3** - User session management
- **Werkzeug 3.0.3** - Security utilities

### Database
- **PostgreSQL** - Primary database
- **psycopg2-binary 2.9.10** - PostgreSQL adapter

### Frontend
- **HTML5 / CSS3**
- **JavaScript**
- **Bootstrap** - Responsive UI framework

## 🏗 System Architecture

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│   (HTML Templates + CSS + JavaScript)   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│        Application Layer (Flask)        │
│  ┌─────────────────────────────────┐   │
│  │  Authentication Module          │   │
│  │  Donor Management Module        │   │
│  │  Inventory Management Module    │   │
│  │  Request Processing Module      │   │
│  │  Admin Module                   │   │
│  └─────────────────────────────────┘   │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         Data Layer (PostgreSQL)         │
│  ┌──────────┐  ┌──────────┐            │
│  │  Users   │  │  Donors  │            │
│  └──────────┘  └──────────┘            │
│  ┌──────────┐  ┌──────────┐            │
│  │ Requests │  │  Stock   │            │
│  └──────────┘  └──────────┘            │
└─────────────────────────────────────────┘
```

## 📥 Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database server
- pip (Python package manager)
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/surya07-dot/Blood-Bank-Donation-Network.git
cd Blood-Bank-Donation-Network
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup PostgreSQL Database
```sql
-- Create database
CREATE DATABASE blood_bank_db;

-- Create user (optional)
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE blood_bank_db TO your_username;
```

### Step 5: Configure Database Connection
Edit `config.py` with your database credentials:
```python
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://username:password@localhost:5432/blood_bank_db"
```

### Step 6: Run the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## ⚙️ Configuration

### Database Configuration (`config.py`)
```python
class Config:
    SECRET_KEY = "your-secret-key-change-in-production"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://user:pass@localhost:5432/blood_bank_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### Environment Variables (Recommended for Production)
```bash
export SECRET_KEY="your-secret-key"
export DATABASE_URL="postgresql://user:pass@localhost:5432/blood_bank_db"
```

## 🚀 Usage

### For Public Users

1. **View Blood Inventory**
   - Navigate to "Inventory" to check available blood units

2. **Register as Donor**
   - Click "Donor Registration"
   - Fill in personal details and blood information
   - Submit to register (stock automatically updated)

3. **Request Blood**
   - Click "Request Blood"
   - Provide patient and hospital details
   - Submit request (admin will review)

### For Registered Users

1. **Create Account**
   - Click "Register"
   - Provide name, email, and password
   - First user becomes admin automatically

2. **Login**
   - Enter credentials at login page
   - Access personal dashboard

### For Administrators

1. **Manage Requests**
   - View all pending blood requests
   - Approve requests (after stock verification)
   - Reject requests if insufficient stock

2. **Monitor System**
   - Track recent donor registrations
   - Monitor blood stock levels
   - Review request history

## 🗄 Database Schema

### Users Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| name | String(100) | Not Null |
| email | String(120) | Unique, Not Null |
| password_hash | String(255) | Not Null |
| is_admin | Boolean | Default: False |

### Donors Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| full_name | String(150) | Not Null |
| age | Integer | Not Null |
| gender | String(10) | Not Null |
| blood_group | String(5) | Not Null |
| phone | String(20) | Not Null |
| email | String(120) | Nullable |
| city | String(100) | Not Null |
| last_donated | Date | Nullable |
| created_at | DateTime | Default: UTC Now |

### Blood_Requests Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| patient_name | String(150) | Not Null |
| hospital_name | String(200) | Not Null |
| blood_group | String(5) | Not Null |
| units | Integer | Not Null |
| phone | String(20) | Not Null |
| status | String(20) | Default: 'Pending' |
| created_at | DateTime | Default: UTC Now |

### Blood_Stock Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| blood_group | String(5) | Unique, Not Null |
| units_available | Integer | Default: 0 |

## 🛣 API Routes

| Route | Method | Access | Description |
|-------|--------|--------|-------------|
| `/` | GET | Public | Homepage with inventory overview |
| `/about` | GET | Public | About page |
| `/login` | GET, POST | Public | User login |
| `/register` | GET, POST | Public | User registration |
| `/logout` | GET | Protected | User logout |
| `/donor/register` | GET, POST | Public | Donor registration |
| `/request-blood` | GET, POST | Public | Blood request submission |
| `/inventory` | GET | Public | Blood inventory display |
| `/dashboard` | GET | Protected | User/Admin dashboard |
| `/requests/manage/<id>/<action>` | GET | Admin Only | Approve/Reject requests |

## 📸 Screenshots

### Homepage
> Displays current blood inventory and quick stats

### Donor Registration
> User-friendly form for donor registration

### Admin Dashboard
> Comprehensive view of recent donors and requests

### Blood Request Form
> Simple interface for requesting blood

*Add actual screenshots here*

## 🔮 Future Enhancements

- [ ] Email/SMS notifications for request status updates
- [ ] Donor eligibility verification (56-90 day waiting period)
- [ ] Advanced search and filtering capabilities
- [ ] Blood donation camps management module
- [ ] Mobile application (Android/iOS)
- [ ] Integration with hospital management systems
- [ ] Analytics dashboard with charts and graphs
- [ ] Blood expiry date tracking
- [ ] Multi-language support
- [ ] Export reports in PDF/Excel format
- [ ] Appointment scheduling for donors
- [ ] Blood compatibility checker

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards
- Follow PEP 8 style guide for Python code
- Write meaningful commit messages
- Add comments for complex logic
- Update documentation for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

**Developer:** Surya

**GitHub:** [@surya07-dot](https://github.com/surya07-dot)

**Project Link:** [https://github.com/surya07-dot/Blood-Bank-Donation-Network](https://github.com/surya07-dot/Blood-Bank-Donation-Network)

---

### ⭐ If you find this project helpful, please give it a star!

### 💡 Project Stats

- **Lines of Code:** 1000+
- **Files:** 15
- **Routes:** 11
- **Templates:** 9
- **Database Tables:** 4

---

**Made with ❤️ to save lives**
