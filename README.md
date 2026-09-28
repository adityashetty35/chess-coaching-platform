# ♟️ Chess Coaching Platform

A complete, production-ready, end-to-end web application built for professional chess coaches, academies, and private instructors.

Built with **Django**, **SQLite**, and modern **Tailwind-inspired CSS**, it combines:
1. **Public Marketing Website** – Premium landing page showcasing services, programs, achievements, testimonials, interactive FAQ, and direct enquiry/booking.
2. **Coach / Admin Management Dashboard** – Full academy operations including student rosters, batch/class scheduling, attendance tracking, fee invoicing, automated WhatsApp reminders, tournament results, and custom performance analytics.
3. **Student & Parent Portals** – Dedicated authenticated dashboards for students and parents to track upcoming classes, homework assignments, attendance history, chess skill progression, and fee receipts.

---

## 🌟 Features Overview

### 1. Public Academy Website
- **Modern Responsive Landing Page**: Hero banner, coach introduction, philosophy, coaching programs (1-on-1, Group, Tournament Prep, Online & Offline).
- **Public Enquiry Engine**: Interactive enquiry capture for prospective students/parents (rating, skill level, goals, schedule preference).
- **Floating WhatsApp Action**: Instant one-click chat button to connect with the coach.

### 2. Coach Operations & CRM
- **Executive Dashboard**: Real-time KPI metrics for active students, today's schedule, pending fees, monthly collections, new enquiries, and low-attendance alerts.
- **Enquiry Pipeline**: Pipeline workflow (`New` ➔ `Contacted` ➔ `Trial Scheduled` ➔ `Interested` ➔ `Converted` ➔ `Follow Up Later`). One-click student conversion pre-fills profiles.
- **Student Roster & Profiles**: Detailed chess dossiers with FIDE ID, Chess.com / Lichess usernames, tactical strengths, repertoire preferences, and emergency parent contacts.
- **Batches & Scheduling**: Group batches and private 1-on-1 sessions with integrated Google Meet/Zoom links, lesson topics, and coach notes.
- **Attendance Register**: Multi-student bulk attendance marking (`Present`, `Absent`, `Late`, `Excused`) with automatic percentage calculations.
- **Fee Management & Invoicing**: Custom fee plans (Monthly, Quarterly, Per Session), invoice generation, partial payment recording, and balance tracking.
- **1-Click WhatsApp Reminders**: Direct-to-WhatsApp pre-formatted payment reminder messages tailored to parents with fee balance and due date.
- **Skill Progression & Goals**: Multi-attribute skill evaluations (Tactics, Opening Repertoire, Calculation, Endgame, Time Management) and measurable student milestones.
- **Assignments & Homework**: Assign chess studies/puzzles with submission tracking and personalized coach feedback.
- **Tournament Tracker**: Record tournament performances, FIDE/National rating gains, standings, and game reviews.
- **Broadcast Announcements**: Targeted bulletin announcements for the whole academy, specific batches, or individual students.
- **Business Reporting & CSV Exports**: Financial summaries, attendance reports, and enquiry conversion analytics with instant CSV export.

### 3. Student & Parent Portals
- **Student Portal**: Upcoming class schedule with direct video call links, assigned homework, personal skill progression charts, and tournament records.
- **Parent Portal**: Multi-child switcher, class attendance records, homework status, pending fee breakdown, and historical payment receipts.

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.10+
- `pip` and virtual environment support

### 1. Clone the repository
```bash
git clone https://github.com/adityashetty35/chess-coaching-platform.git
cd chess-coaching-platform
```

### 2. Set up virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run database migrations & load demo data
```bash
python manage.py migrate
python manage.py load_demo_data
```

### 4. Start local development server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🔑 Default Demo Accounts

All demo accounts share the password: `chess123`

| Role | Username | Password | Dashboard Access |
|------|----------|----------|-------------------|
| **Coach (Admin)** | `coach` | `chess123` | Full Academy Admin (`/dashboard/`) |
| **Student** | `aarav.kumar` | `chess123` | Student Portal (`/portal/`) |
| **Student** | `ananya.sharma` | `chess123` | Student Portal (`/portal/`) |
| **Parent** | `parent.rajesh` | `chess123` | Parent Portal (`/portal/`) |

---

## 🌐 PythonAnywhere Deployment Guide

The application is optimized for free-tier hosting on **PythonAnywhere**:

1. **Upload Code**: Clone from GitHub or upload the project archive to `/home/<username>/chess-coaching-platform/`.
2. **Create Web App**: In PythonAnywhere Web tab, choose **Manual Configuration** with **Python 3.10**.
3. **Virtualenv**: Use default Python 3.10 environment (Django & Pillow pre-installed) or configure a custom venv.
4. **Configure WSGI Configuration File** (`/var/www/<username>_pythonanywhere_com_wsgi.py`):
```python
import os
import sys

path = '/home/<username>/chess-coaching-platform'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'chess_coaching.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
5. **Static & Media File Mappings**:
   - URL: `/static/` ➔ Directory: `/home/<username>/chess-coaching-platform/staticfiles/`
   - URL: `/media/` ➔ Directory: `/home/<username>/chess-coaching-platform/media/`
6. **Reload Web App**: Hit the green **Reload** button in the PythonAnywhere Web tab.

---

## 🛡️ License & Credits
Open-source under the MIT License. Built with Django and designed for professional chess mentors worldwide.
