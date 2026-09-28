# Grandmaster Chess Coaching Platform

A complete, production-ready, lightweight web application built for professional chess coaches. It features a modern public-facing website and an extensive, role-protected coach management system and student/parent portal.

Built with **Django 4.2+** and **SQLite**, styled with a clean modern UI inspired by executive coaching platforms (such as BetterUp, CoachHub, EZRA, and Torch), designed to be easily deployed on **PythonAnywhere** or any standard Linux VPS.

---

## 🌟 Key Features

### 1. Public-Facing Website
- **Modern Hero Section**: High-converting tagline, call-to-action buttons, and social proof.
- **About the Coach**: Highlights FIDE rating, coaching credentials, arbitership, and experience.
- **Comprehensive Services Showcase**:
  - Personal 1-on-1 Coaching
  - Group Coaching Batches
  - Beginner, Intermediate, and Advanced / Tournament Training
  - Online & In-person / Offline Training
  - Opening Preparation, Middlegame Strategy, Endgame Technique, Tactical Calculation, Game Analysis
  - Kids Coaching & Adult Programs
- **Structured Coaching Packages**: Pricing tiers with feature comparison and popularity badges.
- **Social Proof**: Testimonials with star ratings and student tournament achievements.
- **Interactive FAQ Accordion**: Common questions about schedules, equipment, and prerequisites.
- **Public Trial / Enquiry Booking**: Clean, validated modal form.
- **Direct WhatsApp Float Button**: Instant chat launcher with pre-configured greeting.
- **Dynamic Content**: Coach can edit all landing page content directly from the admin dashboard without writing code.

---

### 2. Lead & Enquiry Management
- Visitors can submit enquiries specifying chess level, rating, mode preference, age, and schedule.
- **Status Lifecycle Tracking**: `New` ➔ `Contacted` ➔ `Trial Scheduled` ➔ `Interested` ➔ `Converted` ➔ `Not Interested` ➔ `Follow Up Later`.
- Follow-up timeline with notes and scheduled next contact dates.
- **1-Click Conversion to Student**: Seamlessly transforms an enquiry into an active student profile (and links parent info).

---

### 3. Coach & Admin Management Dashboard
- **Key Metrics at a Glance**: Active students, new leads, today's schedule, pending fees, monthly fee collection, low-attendance alerts.
- **Quick Action Bar**: 1-click shortcuts to add a student, schedule a class, create an invoice, log a payment, post homework, or send an announcement.
- **Classes & Calendar**: Today's schedule and upcoming sessions with online/offline indicators.
- **Financial Health**: Overdue fee alerts and recent payment receipts.

---

### 4. Student & Parent Management
- **Detailed Profiles**: FIDE ID/rating, Chess.com and Lichess handles, strengths, weaknesses, preferred openings, and target goals.
- **Parent Relationships**: Multiple guardians per student and multi-child families with preferred communication methods.
- **1-Click Portal Account Generation**: Auto-creates Django user credentials for student and parent logins.

---

### 5. Classes, Batches & Attendance
- **Batch Management**: Group batches (e.g. *Beginners Batch A*, *Intermediate Rapid*) with capacity limits and schedules.
- **Flexible Scheduling**: Group or 1-on-1 sessions, online meeting links or classroom locations.
- **Batch Attendance Marking**: Quick attendance grid (`Present`, `Late`, `Absent`, `Excused`) updating student attendance percentages automatically.
- **Calendar View**: Monthly interactive class schedule grid.

---

### 6. Fees, Invoices & Payment Reminders
- **Fee Plans**: Monthly, quarterly, annual, or per-session packages.
- **Invoices**: Due dates, balance tracking, status tracking (`Pending`, `Partially Paid`, `Paid`, `Overdue`).
- **Partial & Multi-Method Payments**: Record cash, UPI, bank transfer, or card with transaction references.
- **Ready-to-Send WhatsApp Reminders**: Generates a pre-filled WhatsApp message for the parent:
  > *"Hello {parent_name}, this is a friendly reminder that the chess coaching fee of ₹{amount} for {student_name} is pending. Due date: {due_date}. Thank you."*
- **Scheduled Reminders**: View upcoming scheduled reminders and cancellation controls.

---

### 7. Chess Progress Tracking & Goals
- **8 Core Chess Skill Metrics**: Tactics, Openings, Middlegame, Endgame, Calculation, Positional Understanding, Time Management (1-10 rating scale).
- **Progress History**: Evolution over time, rating increments, and coach commentary.
- **Student Goals**: Milestone tracking with progress percentages (e.g. *Reach 1400 FIDE*, *Master Lucena Position*).

---

### 8. Homework & Assignments
- Assign worksheets, tactical puzzles, or master game analysis to whole batches or individual students.
- Track submission status and provide personalized coach feedback.

---

### 9. Tournament Results
- Record tournament name, date, rank, score (e.g. `5.5/7`), performance rating, and calculate rating change (`+35`).

---

### 10. Student & Parent Portals
- **Role-Based Access**:
  - **Students** view their upcoming schedule, attendance percentage, pending homework, goals, and announcements.
  - **Parents** view all their linked children's classes, attendance, homework, and pending fee invoices with balance breakdown.
- Strict data isolation: students and parents only ever see their own records.

---

### 11. Reports & CSV Export
- Financial reports (invoiced vs. collected vs. pending).
- Student roster and demographic reports.
- Attendance compliance and low-attendance alerts.
- Enquiry funnel & conversion rate analytics.
- 1-click **CSV export** for all reports.

---

## 💻 Tech Stack

- **Backend**: Python 3.10+, Django 4.2 LTS
- **Database**: SQLite (zero-config, high performance for single-coach businesses, easily backed up)
- **Frontend**: Bootstrap 5.3.2, Bootstrap Icons, Google Fonts (Inter)
- **Image Processing**: Pillow 10.0+
- **Currency**: INR (₹) by default (customizable in Site Settings)

---

## 🚀 Local Development Setup

### 1. Clone & Enter Directory
```bash
cd /home/neural/workarea/personal/projects/chessCoaching
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Load Demo Data (Optional but Recommended)
Populates realistic students, classes, attendances, invoices, payments, enquiries, and demo accounts:
```bash
python manage.py load_demo_data
```

### 6. Run the Development Server
```bash
python manage.py runserver
```
Visit **http://127.0.0.1:8000/** in your browser.

---

## 🔑 Demo Login Credentials

The `load_demo_data` command generates pre-configured accounts:

| Role | Username | Password | Access Area |
| :--- | :--- | :--- | :--- |
| **Coach (Admin)** | `coach` | `chess123` | Full Admin Dashboard (`/dashboard/`) |
| **Student** | `aarav.kumar` | `chess123` | Student Portal (`/portal/`) |
| **Parent** | `parent.rajesh` | `chess123` | Parent Portal (`/portal/`) |

---

## 🌐 PythonAnywhere Deployment Guide

Hosting this project on [PythonAnywhere](https://www.pythonanywhere.com/) (free or paid) takes less than 5 minutes:

### Step 1: Open a Bash Console on PythonAnywhere
Sign in to PythonAnywhere, go to the **Consoles** tab, and open a **Bash** console.

### Step 2: Clone or Upload Your Code
```bash
cd ~
git clone <your-repository-url> chessCoaching
# Or upload as a zip file and extract
cd ~/chessCoaching
```

### Step 3: Create Virtual Environment and Install Requirements
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Run Migrations and Load Demo Data
```bash
python manage.py migrate
python manage.py load_demo_data
```
*(Or create your own admin with `python manage.py createsuperuser`)*

### Step 5: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 6: Configure the Web App in PythonAnywhere
1. Go to the **Web** tab in PythonAnywhere dashboard.
2. Click **Add a new web app**.
3. Choose **Manual configuration** and select **Python 3.10**.
4. Set the **Virtualenv path**:
   ```
   /home/<your-username>/chessCoaching/venv
   ```
5. Set the **Source code path**:
   ```
   /home/<your-username>/chessCoaching
   ```
6. Set **Working directory**:
   ```
   /home/<your-username>/chessCoaching
   ```

### Step 7: Configure the WSGI File
Click on the **WSGI configuration file** link on the Web tab, delete the default contents, and paste:

```python
import os
import sys

path = '/home/<your-username>/chessCoaching'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'chess_coaching.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
*(Replace `<your-username>` with your actual PythonAnywhere username)*. Save the file.

### Step 8: Configure Static and Media Mappings
In the **Static files** section of the Web tab, add these two entries:

| URL | Directory |
| :--- | :--- |
| `/static/` | `/home/<your-username>/chessCoaching/staticfiles` |
| `/media/` | `/home/<your-username>/chessCoaching/media` |

### Step 9: Configure `ALLOWED_HOSTS`
In `chess_coaching/settings.py`, add your domain:
```python
ALLOWED_HOSTS = ['<your-username>.pythonanywhere.com', 'localhost', '127.0.0.1']
```

### Step 10: Reload Web App
Click the green **Reload <your-username>.pythonanywhere.com** button at the top of the Web tab.
Your chess coaching platform is now live!

---

## 🔒 Security Best Practices for Production

1. Set `DEBUG = False` in `chess_coaching/settings.py`.
2. Generate a fresh `SECRET_KEY` and store it in an environment variable.
3. Keep `db.sqlite3` backed up periodically (you can download it directly from PythonAnywhere's Files tab).
4. Run `python manage.py check --deploy` to verify production settings.
