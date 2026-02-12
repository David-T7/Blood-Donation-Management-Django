<img width="956" height="502" alt="lab tech bloods updated" src="https://github.com/user-attachments/assets/144f47f4-3725-4f9c-bc25-cb9389d6bdb3" /># 🩸 Blood Donation Management System (BDMS)

A comprehensive, **Django-based web portal** designed to connect **donors, hospitals, blood bank staffs** to efficiently streamline the entire blood donation and distribution process.

---

## ✨ Project Overview

The Blood Donation Management System (BDMS) is a centralized platform that facilitates essential blood bank operations. It empowers:
* **Donors** to easily schedule appointments.
* **Hospitals** to submit and track urgent blood requests.
* **Nurses** to conduct preliminary health screenings.
* **Lab Technicians** to manage the storage and stock inventory.
* **BloodBankManagers** to coordinate operations and oversee the entire stock.

---

## 🚀 Key Features

| Role | Actions |
| :--- | :--- |
| **🧑‍🤝‍🧑 Donors** | Register, **book donation appointments**, and view upcoming blood camps. |
| **🩺 Nurses** | **Review preliminary health check forms** submitted by donors and approve/reject appointments based on health criteria. |
| **🏥 Hospitals** | Submit specific blood requests and **track their fulfillment status**. |
| **🔬 Lab Techs** | Manage the **storage and stock inventory** (storing and tracking units). |
| **🧾 BloodBankManagers** | **Approve hospital requests**, coordinate logistics, and oversee the entire inventory. |

---

## 🛠️ Technology Stack

| Component | Technology | Notes |
| :--- | :--- | :--- |
| **Backend** | **Django** (Python) | High-level Python web framework. |
| **Frontend** | HTML, CSS, **Bootstrap** | Responsive and modern user interface. |
| **Database** | **MySQL** | Used for **Production** environment. |
| **Database (Dev)** | **SQLite** | Used for **Development** and local testing. |
| **Authentication** | Django Built-in | Secure and reliable user management. |

---

## ⚙️ Setup & Local Run Instructions

Follow these steps to get the project running on your local machine. Ensure **Python 3.10+** , a running **MySQL Server (If using production settings)** and **Git** are installed and available.

### Full Installation and Configuration Guide

Execute the following commands in your terminal, then complete the database configuration in `settings.py`.

```bash
# Clone the repository
git clone https://github.com/David-T7/Blood-Donation-Management-Django.git
cd Blood-Donation-Management-Django

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Database Configuration
By default, Django is configured for SQLite (great for a quick start). To use MySQL, update the DATABASES object in settings.py:

# Example MySQL Configuration (to be placed in settings.py):
# DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'your_database_name',       # <-- Replace with your DB name
         'USER': 'your_mysql_username',      # <-- Replace with your MySQL username
         'PASSWORD': 'your_mysql_password',  # <-- Replace with your MySQL password
         'HOST': 'localhost',                # Or the IP address of your MySQL server
         'PORT': '3306',                     # Default MySQL port
     }
 }

# 4. Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create an administrative superuser
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```
## 📸 Project Preview
All screenshots are stored in the `screenshots` folder at the root of this repository.

![Home Page](<screenshots//global%20home%20page.png>)
![Login Page](<screenshots/login%20page.png>)
![Donor Registeration Page](<screenshots//registration%20page%20for%20donor.png>)
![Donor Registeration Page2](<screenshots//registration%20page%20for%20donor%202.png>)
![Donor Home page](<screenshots//donor%20home.png>)
![Donor Donation Request Page 1](<screenshots//donor%20donation%20request%20page1.png>)
![Donor Donation Request Page 2](<screenshots//donor%20donation%20request%20page2.png>)
![Donor Appointments Page](<screenshots//donor%20appointments%20page.png>)
![Donor Appointment Selection Page](<screenshots//donor%20appointment%20data%20selection.png>)
![Donor Donation Camps Page](<screenshots//donor%20camps%20page.png>)
![Donor Donation Camp Map page](<screenshots//donor%20seecamp%20map%20page.png>)
![Nurse Donation Requests Page](<screenshots//nurse%20requests%20page.png>)
![Nurse Donation Request Page1](<screenshots//nurse%20request%20check%20page%201.png>)
![Nurse Donation Request Page2](<screenshots//nurse%20request%20check%20page%202.png>)
![Nurse Add Health Questions Page 1](<screenshots//nurse%20add%20health%20questions%20page.png>)
![Nurse Add Health Questions Page 2](<screenshots//nurse%20add%20health%20questions%20page2.png>)
![Nurse Add Health Questions Page 2](<screenshots//nurse%20add%20health%20questions%20page2.png>)
![Nurse Donation Appointment Requests Page](<screenshots//nurse%20appointment%20requests%20page.png>)
![Nurse Pre Donation Questions Page1](<screenshots//pre%20donation%20questions%20page%201.png>)
![Nurse Pre Donation Questions Page1](<screenshots//pre%20donation%20questions%20page%201.png>)
![Lab Technician Donation Result Page](<screenshots//labtech%20requests%20result%20page.png>)
![Lab Technician Add Blood Page](<screenshots//lab%20tech%20add%20blood.png>)
![Lab Technician Bloods Page](<screenshots//lab%20tech%20bloods%20updated.png>)
![Hospital Representative Dashboard](<screenshots//hospitalrep%20dashboard.png>)
![Hospital Representative Blood Requests Page](<screenshots//hospitalrep%20blood%20requests%20page.png>)
![Hospital Representative Blood Request Page](<screenshots//hospitalrep%20blood%20request.png>)
![Blood Manager Dashboard page](<screenshots//bbmanager%20dashboard.png>)
![Blood Manager Bloods History Page ](<screenshots//bbmanager%20blood%20history%20page .png>)
![Blood Manager Bloods Request Page ](<screenshots//bbmanager%20blood%20request%20page.png>)
![Admin Page1](<screenshots//admin%20page%201.png>)
![Admin Page2](<screenshots//admin%20page%202.png>)



