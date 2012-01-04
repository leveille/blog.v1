## Current Release ##

There currently is no official release of my blog software.  I have a number of tickets I want to get through before delivering my first official beta release.  Because I do not have an official release, I am only providing general instructions for myself.  Installation will look like the following (for *nix ... modify to fit your needs):

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
