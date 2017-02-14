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


Issues:
1. Data: Content van Koppen in type                 OK
2. Data: QUestions in type                          OK
3. Enable/Disable Questions en Reactions in type    OK
4. Rating voor text-version-question                OK


1. star-rating voor anonymous users                 OK
2. gebruik slug voor brief waarderen                OK
3. multi site (NiceToHave)                          OK
4. email address as user!!
5. Autorisaties per site
6. Register as admin for site (sitename based on email host)
   -- else confirm via admin proces
7. Create invitation for site -- other user -- enable self-registration for email-domain
8. create demo-domain for other users..

1. Export csv van waarderingen   
2. Export mailadressen voor responses

1. style: brief in blok tonen                       OK
2. Iframe include mechanisme
3. Citizenline LOGO                                 OK

1. Testcases voor improvetext

1. improvetext module in Git                        OK
2. Deploy improvetext naar citizenline              OK
3. Use Postgress database


Andere Epics:
- Website voor citizeline
- Automated deployments
- Vagrant of docker box voor testing
- Automate testing



Maak gebruik van iframe include.

Als alternatief ook een API bieden met:

css
javascript die zelf gebruikt kan worden
API calls voor ophalen / tonen van content, ratings en comments

                {% render_question_list for blog.post object_pk as comment_list %}
                {% for comment in comment_list %}
                <p>Posted by: {{ comment.user_name }} on {{ comment.submit_date }}</p>
                ...
                <p>Comment: {{ comment.comment }}</p>
                ...
                {% endfor %}
                
                
                
            {%
                def items(self):
        qs = django_comments.get_model().objects.filter(
            site__pk=self.site.pk,
            is_public=True,
            is_removed=False,
        )
        return qs.order_by('-submit_date')[:40]
 %}
 
 
 frontend public
  bind *:80
  acl is_websocket hdr_end(host) -i ws.example.com
  use_backend ws if is_websocket
  default_backend www

backend www
  timeout server 30s
  server www1 127.0.0.1:8080

backend ws
  timeout server 600s
  server ws1 127.0.0.1:8000
  
  
  
  yum install haproxy
  vi /etc/firewalld/services/haproxy.xml
  setsebool -P haproxy_connect_any=true
  systemctl start haproxy
  systemctl status haproxy
  vi /etc/haproxy/haproxy.cfg
  systemctl status haproxy -l
  systemctl stop haproxy -l
  chkconfig haproxy on
  
  systemctl restart  haproxy.service
  
  
  
  