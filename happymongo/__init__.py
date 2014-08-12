# -*- coding: utf-8 -*-
# Copyright 2013 Matt Martz
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
import pymongo.errors

# Attempt to import flask but continue on without it
try:
    import flask.app as flask_app
except ImportError:
    flask_app = None


__version__ = '1.0.0'


class HapPyMongoNoHost(pymongo.errors.ConfigurationError):
    """Raised when MONGO_HOST is configured incorrectly"""


def get_app_name():
    """Flask like implementation of getting the applicaiton name via
    the filename of the including file

    """
    fn = getattr(sys.modules['__main__'], '__file__', None)
    if fn is None:
        return '__main__'
    return os.path.splitext(os.path.basename(fn))[0]


class HapPyMongo(object):
    """HapPyMongo class that returns a tuple of either:

    (pymongo.mongo_client.MongoClient, pymongo.database.Database)

    or

    (pymongo.mongo_replica_set_client.MongoReplicaSetClient,
     pymongo.database.Database)

    """

    def __new__(cls, app_or_object_or_dict):
        """Creates and returns a tuple of either:

        (pymongo.mongo_client.MongoClient, pymongo.database.Database)

        or

        (pymongo.mongo_replica_set_client.MongoReplicaSetClient,
         pymongo.database.Database)

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
        args = []

        # Are we operating with a full MONGO_URI or not?
        if 'MONGO_URI' in config:
            # bootstrap configuration from the URL
            parsed = pymongo.uri_parser.parse_uri(config.get('MONGO_URI'))
            if 'database' not in parsed:
                raise ValueError('MongoDB URI does not contain database name')
            config['MONGO_DATABASE'] = parsed['database']
            config['MONGO_USERNAME'] = parsed['username']
            config['MONGO_PASSWORD'] = parsed['password']
            for option, value in parsed['options'].iteritems():
                kwargs.setdefault(option, value)

            # we will use the URI for connecting instead of HOST/PORT
            config.pop('MONGO_HOST', None)
            config.pop('MONGO_PORT', None)
            #host = config.get('MONGO_URI')
            args.append(config.get('MONGO_URI'))
        # Not operating with a full MONGO_URI
        else:
            config.setdefault('MONGO_HOST', 'localhost')
            config.setdefault('MONGO_PORT', 27017)
            config.setdefault('MONGO_DATABASE', app_name)

            # these don't have defaults
            config.setdefault('MONGO_USERNAME', None)
            config.setdefault('MONGO_PASSWORD', None)

            try:
                port = int(config.get('MONGO_PORT'))
            except ValueError:
                raise TypeError('MONGO_PORT must be an integer')

            host = '%s:%s' % (config.get('MONGO_HOST'),
                              config.get('MONGO_PORT'))

        username = config.get('MONGO_USERNAME')
        password = config.get('MONGO_PASSWORD')
        auth = (username, password)

        if any(auth) and not all(auth):
            raise Exception('Must set both USERNAME and PASSWORD or neither')

        database = config.get('MONGO_DATABASE')

        kwargs['host'] = host

        # Instantiate the correct pymongo client for replica sets or not
        if kwargs.get('replicaSet'):
            if (isinstance(config.get('MONGO_HOST'), (list, tuple)) and
                    not args):
                del kwargs['host']
                hosts = []
                for host in config.get('MONGO_HOST'):
                    if ':' not in host:
                        host = '%s:%s' % (host, config.get('MONGO_PORT'))
                    hosts.append(host)
                args.append('%s' % ','.join(hosts))
            cls = pymongo.MongoReplicaSetClient
        else:
            if (isinstance(config.get('MONGO_HOST'), (list, tuple)) and
                    not args):
                raise HapPyMongoNoHost
            cls = pymongo.MongoClient

        # Instantiate the class using the kwargs obtained from and set
        # in MONGO_KWARGS
        mongo = cls(*args, **kwargs)

        db = mongo[database]

        # Auth with the DB if username and password were provided
        if any(auth):
            db.authenticate(username, password)

        if is_flask:
            if not hasattr(app_or_object_or_dict, 'extensions'):
                app_or_object_or_dict.extensions = {}
            app_or_object_or_dict.extensions['happymongo'] = (mongo, db)

        # Return the tuple
        return mongo, db

# vim:set ts=4 sw=4 expandtab:
