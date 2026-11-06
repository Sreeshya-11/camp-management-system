
# Camp Management System

A web-based Camp Management System developed using Django.

## Features

- Admin Dashboard
- Camp Management
- Volunteer Management
- Donor Management
- Donation Management
- Notifications
- OTP Verification
- Password Recovery
- Razorpay Payment Integration

## Technologies Used

- Python
- Django
- HTML
- CSS
- JavaScript
- SQLite
- Razorpay

## Project Structure

```text
Camp_Management_14/
│
├── Camp_Management/
│
├── apk/
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   ├── static/
│   └── migrations/
│
├── manage.py
├── loc.py
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Sreeshya-11/camp-management-system.git
cd camp-management-system
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install django
```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Run the Application

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Author

Sreeshya N R

## GitHub Repository

https://github.com/Sreeshya-11/camp-management-system
