sudo apt-get install python-virtualenv
sudo apt-get install python-pip


virtual env
=================
virtualenv venv
python manage.py syncdb
source venv/bin/activate

pip install django

python manage.py runserver

http://127.0.0.1:8000/admin/

