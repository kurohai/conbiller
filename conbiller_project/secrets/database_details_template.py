import os


# SQLite Template
pwd = os.path.abspath(os.curdir)

dbpath = '{dir}/{app}.db'\
    .format(
        dir=pwd,
        app='test',
    )

database_uri = 'sqlite:///{db}'.format(db=dbpath)

# MySQL Template
# database_uri = 'mysql://{user}:{password}@{host}:{port}/{database}'\
#     .format(
#         username=None,
#         password=None,
#         host=None,
#         port=None, # default is 3306
#         database=None,
#     )
