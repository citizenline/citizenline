# citizenline

Open source project for citizen participation tools

    sudo su -
    yum update
    yum -y install python-virtualenv
    yum -y install python-virtualenvwrapper
    yum install numpy scipy python-matplotlib ipython python-pandas sympy python-nose

    nohup python ./manage.py runserver &

## Getting started

    virtualenv citizenline

clone repo
Add in ".bash_profile":

    source /webapps/citizenline/bin/activate
    export DJANGO_SETTINGS_MODULE=citizenline.settings.production

    pip install -r requirements/dev.txt
    ./manage.py migrate

    ./manage.py createsuperuser

or create test text and default admin user:

    ./manage.py populatetext

    ./manage.py runserver

## Watch and build javascript and css

    npm install

    npm run-script watch-js
    npm run-script watch-scss

    npm run-script build-js
    npm run-script build-scss

## Migrate database

    export DJANGO_SETTINGS_MODULE=citizenline.settings.production
    python manage.py migrate

## Language

    manage.py makemessages
    - update po files
    manage.py compilemessages
