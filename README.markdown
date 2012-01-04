* wget http://pylonsbook.com/virtualenv.py
* python virtualenv.py --no-site-packages env
* source env/bin/activate
* sudo apt-get install python-dev libc6-dev
* download and install wurdig from http://github.com/leveille/jasonleveille.com (click the downloads button)
* cd wurdig/installation
* sudo apt-get install tidy
* python setup.py develop
* paster make-config "Wurdig" development.ini
* edit development.ini
* paster setup-app development.ini
* paster serve --reload development.ini
* admin login - un: admin pw: admin
