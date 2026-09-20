<div align="center">

<img src="logo.png" alt="CaseFlow Logo" width="120">

# CaseFlow

### Incident Reporting and Case Workflow Platform

A Django-based platform that enables citizens to report incidents with supporting evidence and allows authorized police staff to review, prioritize, investigate, and manage cases through a structured workflow.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-UI-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)

</div>

---

## Overview

CaseFlow provides a centralized system for reporting incidents and tracking their progress.

Citizens can submit detailed reports, select the incident location on an interactive map, upload supporting evidence, and monitor status updates. Police staff receive a dedicated dashboard to review incoming reports, assign priorities, update investigation status, add notes, publish public alerts, and view analytics.

## Key Features

### Citizen Portal

- Secure account registration and login
- Submit detailed incident reports
- Specify incident type, description, date, time, and priority
- Select the incident location using an interactive map
- Automatic address lookup using reverse geocoding
- Upload multiple forms of evidence:
  - Images
  - Audio recordings
  - Videos
- Track submitted reports from a personal dashboard
- Search and filter reports
- View report status and police notes
- Receive notifications when a report is submitted or updated
- View public safety alerts
- View and update profile information

### Police and Staff Portal

- Staff-restricted police dashboard
- View and manage all submitted reports
- Search reports by crime type, citizen, location, or date
- Filter reports by:
  - Status
  - Crime type
  - Priority
- Review complete incident information and evidence
- Update case status
- Add investigation notes
- View citizen profiles and reporting history
- Publish area-specific public alerts
- Access case statistics and visual analytics

## Case Workflow

Reports move through the following states:

```text
Pending → Under Investigation → Resolved
                              ↘ Rejected
```

Each report can also be assigned a priority level:

| Level | Priority |
|------:|----------|
| 1 | Very Low |
| 2 | Low |
| 3 | Medium |
| 4 | High |
| 5 | Critical |

## Technology Stack

### Backend

- Python
- Django 5.1
- Django Authentication
- Django ORM
- MySQL

### Frontend

- HTML5
- Tailwind CSS
- JavaScript
- Django Templates

### Maps and Visualization

- Leaflet.js
- OpenStreetMap
- Nominatim reverse geocoding
- Chart.js

### Media Handling

- Pillow
- Django media storage
- Image, audio, and video uploads

## System Architecture

```text
Citizen / Police Staff
          │
          ▼
 Django Templates + JavaScript
          │
          ▼
     Django Views
          │
          ▼
 Django Models and ORM
          │
          ▼
       MySQL
```

## Data Models

| Model | Purpose |
|-------|---------|
| `Profile` | Stores additional citizen information such as phone number and address |
| `UserCrimeReport` | Stores incident details, status, priority, location, and police notes |
| `EvidencePhoto` | Stores image evidence associated with a report |
| `EvidenceAudio` | Stores audio evidence associated with a report |
| `EvidenceVideo` | Stores video evidence associated with a report |
| `Alerts` | Stores public safety alerts published by staff |
| `Notification` | Stores report updates and alert notifications for users |

## Project Structure

```text
CaseFlow-Incident-Reporting-and-Case-Workflow-Platform/
├── cr/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── main/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
├── static/
│   └── styles/
├── templates/
│   ├── Header.html
│   ├── PoliceDashboard.html
│   ├── Update_status.html
│   ├── View_report.html
│   ├── alerts.html
│   ├── edit_profile.html
│   ├── login.html
│   ├── police_analytics.html
│   ├── reporting.html
│   ├── signin.html
│   ├── staff_user_profile.html
│   └── usr_home_pg.html
├── logo.png
├── manage.py
└── requirements.txt
```

## Getting Started

### Prerequisites

Install the following:

- Python 3.10 or later
- MySQL Server
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/ajithreddy1234/CaseFlow-Incident-Reporting-and-Case-Workflow-Platform.git
cd CaseFlow-Incident-Reporting-and-Case-Workflow-Platform
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS or Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the MySQL Database

Open MySQL and run:

```sql
CREATE DATABASE CrimeTracker;
```

Update the database configuration in `cr/settings.py` with your local MySQL username and password.

A recommended environment-based configuration is:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DB_NAME", "CrimeTracker"),
        "USER": os.getenv("DB_USER", "root"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "3306"),
    }
}
```

Create a `.env` file in the project root:

```env
SECRET_KEY=replace-with-a-secure-secret-key
DB_NAME=CrimeTracker
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_HOST=localhost
DB_PORT=3306
```

Do not commit the `.env` file to GitHub.

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Create a Police Staff Account

```bash
python manage.py createsuperuser
```

Superusers and users marked as staff are redirected to the police dashboard after logging in.

### 7. Start the Development Server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

## Application Routes

| Route | Description | Access |
|-------|-------------|--------|
| `/` | Citizen or police dashboard | Authenticated users |
| `/register/` | Citizen registration | Public |
| `/login/` | User login | Public |
| `/report-crime/` | Submit an incident report | Citizens |
| `/view-report/<id>/` | View report details and evidence | Authenticated users |
| `/admin-dashboard/` | Manage all reports | Police staff |
| `/update-report/<id>/` | Update report status and notes | Police staff |
| `/analytics/` | View report analytics | Police staff |
| `/alerts/` | View or publish safety alerts | Authenticated users |
| `/view-profile/` | View personal profile | Authenticated users |
| `/edit-profile/` | Update personal information | Authenticated users |
| `/admin/` | Django administration panel | Superusers |

## Analytics Dashboard

The police analytics dashboard displays:

- Total number of reports
- Pending reports
- Reports under investigation
- Resolved and rejected reports
- Critical, high, and medium-priority reports
- Status distribution using a doughnut chart
- Priority distribution using a bar chart

## Notifications

CaseFlow creates notifications when:

- A citizen submits a new report
- Police staff update a report's status
- Police staff publish a public safety alert

Users can view recent notifications and mark individual or all notifications as read.

## Future Improvements

- Assign reports to individual investigating officers
- Maintain a complete case activity and audit log
- Add email and SMS notifications
- Implement role-based permissions beyond the staff flag
- Encrypt sensitive evidence and personal information
- Store uploaded evidence using cloud object storage
- Add advanced date and location-based analytics
- Add report export to PDF
- Add automated tests and CI/CD workflows
- Containerize the application using Docker

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/feature-name
```

3. Commit your changes:

```bash
git commit -m "Add feature description"
```

4. Push the branch:

```bash
git push origin feature/feature-name
```

5. Open a pull request.

## Author

**Ajith Reddy**

- GitHub: [@ajithreddy1234](https://github.com/ajithreddy1234)
- Repository: [CaseFlow](https://github.com/ajithreddy1234/CaseFlow-Incident-Reporting-and-Case-Workflow-Platform)

---

<div align="center">

Built to simplify incident reporting and improve case-management transparency.

</div>
