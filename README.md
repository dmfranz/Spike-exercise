# Spike-exercise
To run the django server.

Python should be installed.
Django should be installed.
Django-crispy_forms should be installed.

If there are database issues, delete all the files except __init__.py from the migrations folder, delete db.sqlite3, and run:
  python manage.py makemigrations
  python manage.py migrate
  
1) Start the server with "python manage.py runserver"
3) pip install -r requirements.txt

# Notes
I think using bootstrap will be the easiest way to style this and linking any page to base.html will include everything needed to use it.
