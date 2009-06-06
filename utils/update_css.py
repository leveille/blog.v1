# taken directly from http://bitbucket.org/bbangert/kai/src/
from datetime import datetime
import os
import sys

import cssutils

if len(sys.argv) < 2:
    print "Must have at least 1 argument:"
    print "\tpython update_css.py CONFIG.INI"
    sys.exit(0)

here_dir = os.path.dirname(os.path.abspath(__file__))
conf_dir = os.path.dirname(here_dir)
css_dir = os.path.join(conf_dir, 'wurdig', 'public', 'css')

ini_name = sys.argv[1]
ini_file = open(os.path.join(conf_dir, ini_name)).readlines()
csslist = open(os.path.join(css_dir, 'FCSSLIST')).read()

# Combine all the CSS into one string
combined_css = ''
for f in csslist.split(' '):
    css_file = open(os.path.join(css_dir, '%s.css' % f)).readlines()
    parsed_css = ''
    for line in css_file:
        if line.startswith('@charset'):
            continue
        parsed_css += line
    combined_css += parsed_css

# Parse the CSS and turn on minification
sheet = cssutils.parseString(combined_css)
cssutils.ser.prefs.useMinified()

# Find the file we're going to write it out to
now = datetime.now()
fname = now.strftime('%m%d%Y')
file_name = fname
for x in range(1,30):
    exists = False
    file_name = 'wurdig-%s.%s-min.css' % (fname, x)
    try:
        stats = os.stat(os.path.join(css_dir, file_name))
        exists = True
    except OSError:
        pass
    if not exists:
        break

# Write it to the file
new_file = open(os.path.join(css_dir, file_name), 'w')
new_file.write(sheet.cssText)
new_file.close()

# Update the ini file to use the new minified CSS
new_ini = ''
for line in ini_file:
    if line.startswith('wurdig.minified_css ='):
        new_line = 'wurdig.minified_css = %s\n' % file_name
    else:
        new_line = line
    new_ini += new_line

nf = open(os.path.join(conf_dir, ini_name), 'w')
nf.write(new_ini)
