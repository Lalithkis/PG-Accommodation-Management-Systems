# PG Accommodation Management System

A comprehensive Hostel Management System built with Django and PostgreSQL (Supabase), designed for seamless management of PG accommodations, students, and complaints.

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
- **Database**: PostgreSQL (via Supabase)
- **Frontend**: HTML5, CSS3, JavaScript (Django Templates)
- **Deployment**: Configured for Vercel
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

### 4. Configure Environment Variables
Create a file named `.env` in the root directory and add the following keys.
**Note:** The project uses Supabase. You need your Supabase connection string.

```env
DATABASE_URL=postgres://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
SECRET_KEY=django-insecure-your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,.vercel.app
```

### 5. Initialize Database
Apply migrations to create tables in the Supabase database:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Admin User
```bash
python manage.py createsuperuser
```
*(Default admin created in this project: Username: `admin`, Password: `adminpassword`)*

### 7. (Optional) Populate Sample Data
To quickly fill the database with dummy rooms and students for testing:
```bash
python manage.py populate_data
```

### 8. Run the Server
```bash
python manage.py runserver
```
Access the app at: `http://127.0.0.1:8000/`

## 🚀 Deployment (Vercel)

This project is configured for deployment on Vercel.

1.  **Push to GitHub**: Upload this project to a GitHub repository.
2.  **Import in Vercel**: Connect your GitHub account and import the repo.
3.  **Environment Variables**: In Vercel Project Settings, add the variables from your `.env` file (`DATABASE_URL`, `SECRET_KEY`, etc.).
4.  **Deploy**: Vercel will automatically build and deploy using `vercel.json` and `build_files.sh`.

## 📂 Project Structure
- `hostel_app/`: Core application logic (Models, Views, Forms).
- `hostel_project/`: Main project settings and URL configuration.
- `templates/`: HTML templates for the frontend.
- `static/`: CSS (inter) and JavaScript files.
- `staticfiles/`: Collected static files for production (auto-generated).
