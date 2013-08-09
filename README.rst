HapPyMongo
==========

Python module for making it easy and consistent to connect to MongoDB
via PyMongo either in Flask or in a non-flask application

Usage
-----

config.py as referenced below
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    MONGO_HOST = 'localhost'
    MONGO_PORT = '27017'
    MONGO_USERNAME = 'user'
    MONGO_PASSWORD = 'password'

Flask
~~~~~

::

    from flask import Flask
    from happymongo import HapPyMongo

    # Our apps config.py
    import config

    app = Flask(__name__)
    app.config.from_object(config)
    mongo, db = HapPyMongo(app)

Python from import
~~~~~~~~~~~~~~~~~~

::

    from happymongo import HapPyMongo

    # Our apps config.py
    import config
    mongo, db = HapPyMongo(config)

Python from dict
~~~~~~~~~~~~~~~~

::

    from happymongo import HapPyMongo

    config = {
        'MONGO_HOST': 'localhost'
    }

    mongo, db = HapPyMongo(config)

Config directives
-----------------

+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Directive         | Description                                                                                                                                                                       |
+===================+===================================================================================================================================================================================+
| MONGO\_URI        | A `MongoDB URI <http://www.mongodb.org/display/DOCS/Connections#Connections-StandardConnectionStringFormat>`_ which is used in preference of the other configuration variables.   |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| MONGO\_HOST       | The host name or IP address of your MongoDB server. Default: “localhost”.                                                                                                         |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| MONGO\_PORT       | The port number of your MongoDB server. Default: 27017.                                                                                                                           |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| MONGO\_DATABASE   | The database name to make available as the db attribute. Default: app.name for Flask or the filename of the including file without the .py extension                              |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| MONGO\_USERNAME   | The user name for authentication. Default: None                                                                                                                                   |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| MONGO\_PASSWORD   | The password for authentication. Default: None                                                                                                                                    |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| MONGO\_KWARGS     | A dictionary of keyword arguments to send to `pymongo.MongoClient <http://api.mongodb.org/python/current/api/pymongo/mongo_client.html>`_                                         |
+-------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

