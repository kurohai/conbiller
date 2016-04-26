import os

try:
    from secrets.database_details import database_uri
except ImportError as e:
    # make sqlite database
    from secrets.database_details_template import database_uri
    print 'You need to update your database connection details in settings.py.'


appname = 'ConBiller'
appnamed = 'conbiller'

# Change this for production!
secret_key = 'ReallBigPassphraseWithRandomStringenydM2ANhdcoKwdVa0jWvEsbPFuQpMjf'

session_protection = 'strong'
pwd = os.path.abspath(os.curdir)

dburi = database_uri
