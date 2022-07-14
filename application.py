# -*- coding: utf-8 -*-
from flask import Flask
#from SBert import *
from Spacy import *

res = process_spacy("Why talk about what we want? That is childish. Absurd. Of course, you are interested in what you want. You are eternally interested in it. But no one else is. The rest of us are just like you: we are interested in what we want.")
# print a nice greeting.
def say_hello(username = "World"):
    return '<p>Hello %s!</p>\n' % res

# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This is a RESTful web service! Append a username
    to the URL (for example: <code>/Marble</code>) to say hello to
    someone specific.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
    say_hello() + instructions + footer_text))

# add a rule when the page is accessed with a name appended to the site
# URL.
application.add_url_rule('/<username>', 'hello', (lambda username:
    header_text + say_hello(username) + home_link + footer_text))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    # IMPORTANT
    application.debug = True
    application.run()
