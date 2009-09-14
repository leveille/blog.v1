# Wurdig: My Pylons Powered Blog #

* [Project Description](http://jasonleveille.com/2009/02/graduate-school-independent-study/ "Project Description")
* In short, Wurdig represents my ongoing effort to learn [Pylons](http://pylonshq.com/ "Pylons").  The learning process has taken the shape of [my current blog](http://jasonleveille.com "my current blog")

## Current Release ##

There currently is no official release of my blog software.  I have a number of tickets I want to get through before delivering my first official beta release.  Because I do not have an official release, I am only providing general instructions for myself.  Installation will look like the following (for *nix ... modify to fit your needs):

* wget http://pylonsbook.com/virtualenv.py
* python virtualenv.py --no-site-packages env
* source env/bin/activate
* sudo apt-get install python-dev libc6-dev
* download and install wurdig from http://github.com/leveille/wurdig (click the downloads button)
* cd wurdig/installation
* sudo apt-get install tidy
* python setup.py develop
* paster make-config "Wurdig" development.ini
* edit development.ini
* paster setup-app development.ini
* paster serve --reload development.ini
* admin login - un: admin pw: admin

It's important to note that this will set up your development environment, however your setup for a production environment will vary.  For example (among other things), you do not want to deploy your application with admin/admin as your login.  If you are attempting to get Wurding up and running, it is stronly recommended that you spend some time looking at [The Pylons Book](http://pylonsbook.com/ "The Pylons Book").

## Links ##

* [Issue Tracking](http://leveille.lighthouseapp.com/projects/28382-wurdig/overview "Issue Tracking")
* [The Pylons Book](http://pylonsbook.com/ "The Pylons Book")

## Licenses ##

Wudrig admin public assets (wudig/public/admin) are subject to the GPL license.  I do not own these assets.  Thankfully, my employer has allowed me to use them, provided others do not gain commercial advantage from their use:

* [GPL](http://github.com/leveille/wurdig/blob/master/GPL-LICENSE.txt "GPL")

Unless otherwise noted in source, Wurdig is currently available for use in all personal or commercial projects under both MIT and GPLv3 licenses. This means that you can choose the license that best suits your project, and use it accordingly:

* [GPL](http://github.com/leveille/wurdig/blob/master/GPL-LICENSE.txt "GPL")
* [MIT](http://github.com/leveille/wurdig/blob/master/MIT-LICENSE.txt "MIT")
