# 🩸 Blood Donation Management System (BDMS)

A comprehensive, **Django-based web portal** designed to connect **donors, hospitals, blood bank staffs** to efficiently streamline the entire blood donation and distribution process.

---

## ✨ Project Overview

The Blood Donation Management System (BDMS) is a centralized platform that facilitates essential blood bank operations. It empowers:
* **Donors** to easily schedule appointments.
* **Hospitals** to submit and track urgent blood requests.
* **Nurses** to conduct preliminary health screenings.
* **Lab Technicians** to manage the storage and stock inventory.
* **Managers** to coordinate operations and oversee the entire stock.

---

## 🚀 Key Features

| Role | Actions |
| :--- | :--- |
| **🧑‍🤝‍🧑 Donors** | Register, **book donation appointments**, and view upcoming blood camps. |
| **🩺 Nurses** | **Review preliminary health check forms** submitted by donors and approve/reject appointments based on health criteria. |
| **🏥 Hospitals** | Submit specific blood requests and **track their fulfillment status**. |
| **🔬 Lab Techs** | Manage the **storage and stock inventory** (storing and tracking units). |
| **🧾 Managers** | **Approve hospital requests**, coordinate logistics, and oversee the entire inventory. |

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

Follow these steps to get the project running on your local machine. Ensure **Python 3.x** and a running **MySQL Server** are installed and available.

### Full Installation and Configuration Guide

Execute the following commands in your terminal, then complete the database configuration in `settings.py`.

```bash
# 1. Clone the repository and navigate into the project directory
git clone [https://github.com/David-T7/Blood-Donation-Management-Django.git](https://github.com/David-T7/Blood-Donation-Management-Django.git)
cd Blood-Donation-Management-Django

# 2. Install all necessary dependencies, including the MySQL adapter
# Note: Ensure the required MySQL client libraries are installed on your OS
pip install -r requirements.txt

# 3. CONFIGURE DATABASE IN settings.py (BEFORE MIGRATIONS)
# Open settings.py and replace the default DATABASES configuration 
# with your MySQL server details and credentials:

# Example MySQL Configuration (to be placed in settings.py):
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'your_database_name',       # <-- Replace with your DB name
#         'USER': 'your_mysql_username',      # <-- Replace with your MySQL username
#         'PASSWORD': 'your_mysql_password',  # <-- Replace with your MySQL password
#         'HOST': 'localhost',                # Or the IP address of your MySQL server
#         'PORT': '3306',                     # Default MySQL port
#     }
# }

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
![Donor Donation Camp Map](<screenshots//donor%20seecamp%20map%20page.png>)
![Nurse Donation Requests Page](<screenshots//nurse%20requests%20page.png>)
![Nurse Donation Request Page1](<screenshots//nurse%20request%20check%20page%201.png>)
![Nurse Donation Request Page2](<screenshots//nurse%20request%20check%20page%202.png>)
![Nurse Add Health Questions Page 1](<screenshots//nurse%20add%20health%20questions%20page.png>)
![Nurse Add Health Questions Page 2](<screenshots//nurse%20add%20health%20questions%20page2.png>)



