# PG Accommodation Management System

A comprehensive Hostel Management System built with Django and MySQL, designed for seamless management of PG accommodations, students, and complaints.

## 🚀 Features

### 👨‍🎓 Student Portal
- **Dashboard**: View room status (Applied/Allocated) and available rooms.
- **Room Booking**: Browse available rooms and apply for accommodation.
- **My Room**: View details of the allocated room and roommates.
- **Complaints**: Submit and track the status of complaints.
- **Profile**: (Auto-created upon registration).

### 👨‍💼 Admin Dashboard
- **Overview**: Real-time stats on tenants, rooms, occupancy, and pending requests.
- **Room Management**: Add, edit, and delete rooms.
- **Allocation Management**: Approve or reject room applications.
- **Student Management**: View list of all tenants and their assigned rooms.
- **Complaint Management**: Review and resolve student complaints.

## 🛠 Tech Stack
- **Backend**: Django 5.x, Python 3.11+
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript (Django Templates)
- **Static Files**: WhiteNoise

## ⚙️ Local Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "PG Accommodation Management System"
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure MySQL Database
1.  Open **MySQL Workbench**.
2.  Create a new schema (database) named `hostel_db`.
3.  Ensure your MySQL server is running.

### 5. Configure Environment Variables
Create a file named `.env` in the root directory and add your MySQL credentials:

```env
SECRET_KEY=django-insecure-your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=hostel_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 6. Initialize Database
Apply migrations to create tables in your MySQL database:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Admin User
```bash
python manage.py createsuperuser
```

### 8. (Optional) Populate Sample Data
To quickly fill the database with dummy rooms and students for testing:
```bash
python manage.py populate_data
```

### 9. Run the Server
```bash
python manage.py runserver
```
Access the app at: `http://127.0.0.1:8000/`

## 📂 Project Structure
- `hostel_app/`: Core application logic (Models, Views, Forms).
- `hostel_project/`: Main project settings and URL configuration.
- `templates/`: HTML templates for the frontend.
- `static/`: CSS (inter) and JavaScript files.
