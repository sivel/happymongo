# -*- coding: utf-8 -*-
# Copyright 2013-2015 Matt Martz
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Python module for making it easy and consistent to connect to mongoDB
via PyMongo either in Flask or in a non-flask application

"""

import os
import sys
import pymongo
from happymongo import errors

# Attempt to import flask but continue on without it
try:
    import flask.app as flask_app
except ImportError:
    flask_app = None


__version__ = '1.0.0'


def get_app_name():
    """Flask like implementation of getting the applicaiton name via
    the filename of the including file

    """
    fn = getattr(sys.modules['__main__'], '__file__', None)
    if fn is None:
        return '__main__'
    return os.path.splitext(os.path.basename(fn))[0]


class HapPyMongo(object):
    """HapPyMongo class that returns a tuple of:

    (pymongo.mongo_client.MongoClient, pymongo.database.Database)

    """

    def __new__(cls, app_or_object_or_dict):
        """Creates and returns a tuple of:

        (pymongo.mongo_client.MongoClient, pymongo.database.Database)

        utilizing either a passed in Flask 'app' instance, an imported module
        object, or a dictionary of config values.

        Arguments:
        app_or_object_or_dict -- Flask app instance, and object or a dict

        """
        config = {}
        app_name = get_app_name()
        is_flask = False
        # If the object is a flask.app.Flask instance
        if flask_app and isinstance(app_or_object_or_dict, flask_app.Flask):
            config.update(app_or_object_or_dict.config)
            app_name = app_or_object_or_dict.name
            is_flask = True
        # If the object is a dict
        elif isinstance(app_or_object_or_dict, dict):
            config.update(app_or_object_or_dict)
        # Otherwise assume it is some type of object such as a module import
        else:
            for name in dir(app_or_object_or_dict):
                if not name.startswith('_'):
                    config[name] = getattr(app_or_object_or_dict, name)

        kwargs = config.get('MONGO_KWARGS', {})

        # Are we operating with a full MONGO_URI or not?
        if 'MONGO_URI' in config:
            kwargs['host'] = config.get('MONGO_URI')
            parsed = pymongo.uri_parser.parse_uri(config.get('MONGO_URI'))
            auth_callback = lambda db: True
        # Not operating with a full MONGO_URI
        else:
            parsed = {}
            config.setdefault('MONGO_HOST', 'localhost')
            config.setdefault('MONGO_PORT', 27017)
            config.setdefault('MONGO_DATABASE', app_name)

            # these don't have defaults
            config.setdefault('MONGO_USERNAME', None)
            config.setdefault('MONGO_PASSWORD', None)

            try:
                int(config.get('MONGO_PORT'))
            except ValueError:
                raise errors.HapPyMongoInvalidPort('MONGO_PORT must be an '
                                                   'integer')

            if not isinstance(config.get('MONGO_HOST'), (list, tuple)):
                config['MONGO_HOST'] = [config['MONGO_HOST']]

            kwargs['host'] = []
            for host in config.get('MONGO_HOST'):
                if ':' not in host:
                    host = '%s:%s' % (host, config.get('MONGO_PORT'))
                kwargs['host'].append(host)

            username = config.get('MONGO_USERNAME')
            password = config.get('MONGO_PASSWORD')
            auth = (username, password)

            if any(auth) and not all(auth):
                raise errors.HapPyMongoMissingAuth('Must set both USERNAME '
                                                   'and PASSWORD or neither')
            auth_callback = lambda db: getattr(db, 'authenticate')(*auth)

        database = parsed.get('database') or config.get('MONGO_DATABASE')

        mongo = pymongo.MongoClient(**kwargs)
        db = mongo[database]
        auth_callback(db)

        if is_flask:
            if not hasattr(app_or_object_or_dict, 'extensions'):
                app_or_object_or_dict.extensions = {}
            app_or_object_or_dict.extensions['happymongo'] = (mongo, db)

        # Return the tuple
        return mongo, db
