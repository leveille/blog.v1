# borrowed heavily from  http://bitbucket.org/bbangert/kai/src/
from datetime import datetime
from jsmin import jsmin
import os
import sys

if len(sys.argv) < 2:
    print "Must have at least 1 argument:"
    print "\tpython update_js.py CONFIG.INI"
    sys.exit(0)

here_dir = os.path.dirname(os.path.abspath(__file__))
conf_dir = os.path.dirname(here_dir)
js_dir = os.path.join(conf_dir, 'wurdig', 'public', 'javascripts')

ini_name = sys.argv[1]
ini_file = open(os.path.join(conf_dir, ini_name)).readlines()
jslist = open(os.path.join(js_dir, 'FJSLIST')).read()

# Combine all the JS into one string
combined_js = ''
for f in jslist.split(' '):
    js_file = open(os.path.join(js_dir, '%s.js' % f)).readlines()
    parsed_js = ''
    for line in js_file:
        parsed_js += line
    combined_js += parsed_js

# Find the file we're going to write it out to
now = datetime.now()
fname = now.strftime('%m%d%Y')
file_name = fname
for x in range(1,30):
    exists = False
    file_name = 'wurdig-%s.%s-min.js' % (fname, x)
    try:
        stats = os.stat(os.path.join(js_dir, file_name))
        exists = True
    except OSError:
        pass
    if not exists:
        break

# Write it to the file
new_file = open(os.path.join(js_dir, file_name), 'w')
minified = jsmin(combined_js)
new_file.write(minified)
new_file.close()

# Update the ini file to use the new minified JS
new_ini = ''
for line in ini_file:
    if line.startswith('wurdig.minified_js ='):
        new_line = 'wurdig.minified_js = %s\n' % file_name
    else:
        new_line = line
    new_ini += new_line

nf = open(os.path.join(conf_dir, ini_name), 'w')
nf.write(new_ini)
