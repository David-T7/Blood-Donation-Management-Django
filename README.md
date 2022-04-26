# Blood-Donation-Mangement

## HOW TO RUN THIS PROJECT
- Install Python(2.7.18) (Dont Forget to Tick Add to Path while installing Python)
- Download This Project Zip Folder and Extract it
- Move to project folder in Terminal. Then run following Commands :


```
# to insatll requirments 
pip install -r requirements.txt 
```


```
# set up mysql connection in settings.py
set the database name 
set the password


# set the email setting in settings.py
EMAIL_HOST_USER = 'youremailaddress'
EMAIL_HOST_PASSWORD = 'yourapppassword' 


# to make migrations 
python manage.py makemigrations
python manage.py migrate

# to create a super user
python manage.py createsuperuser

# to run the project
python manage.py runserver
```
- Now enter following URL in Your Browser Installed On Your Pc

http://127.0.0.1:8000/
