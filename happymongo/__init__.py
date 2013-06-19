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

import pymongo
import os
import sys

try:
    import flask.app as flask_app
except ImportError:
    flask_app = None


def get_app_name():
    fn = getattr(sys.modules['__main__'], '__file__', None)
    if fn is None:
        return '__main__'
    return os.path.splitext(os.path.basename(fn))[0]


class HapPyMongo(object):

    def __new__(cls, app_or_object_or_dict):
        config = {}
        app_name = get_app_name()
        if flask_app and isinstance(app_or_object_or_dict, flask_app.Flask):
            config.update(app_or_object_or_dict.config)
            app_name = app_or_object_or_dict.name
        elif isinstance(app_or_object_or_dict, dict):
            config.update(app_or_object_or_dict)
        else:
            for name in dir(app_or_object_or_dict):
                if not name.startswith('_'):
                    config[name] = getattr(app_or_object_or_dict, name)

        kwargs = config.get('MONGO_KWARGS', {})
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
            host = config.get('MONGO_URI')

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

        if kwargs.get('replicaSet'):
            cls = pymongo.MongoReplicaSetClient
        else:
            cls = pymongo.MongoClient

        mongo = cls(**kwargs)

        db = mongo[database]
        if any(auth):
            db.authenticate(username, password)

        return mongo, db

# vim:set ts=4 sw=4 expandtab:
