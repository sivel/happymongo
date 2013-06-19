# happymongo

## Usage

### Flask

```python
from flask import Flask
from happymongo import HapPyMongo

# Our apps config.py
import config

app = Flask(__name__)
app.config.from_object(config)
mongo, db = HapPyMongo(app)
```

### Python from import

```python
from happymongo import HapPyMongo

# Our apps config.py
import config
mongo, db = HapPyMongo(config)
```

### Python from dict

```python
from happymongo import HapPyMongo

config = {
    'MONGO_HOST': 'localhost'
}

mongo, db = HapPyMongo(config)
```

## Config directives

| Directive      | Description |
| -------------- | ----------- |
| MONGO_URI      | A [MongoDB URI](http://www.mongodb.org/display/DOCS/Connections#Connections-StandardConnectionStringFormat) which is used in preference of the other configuration variables. |
| MONGO_HOST     | The host name or IP address of your MongoDB server. Default: “localhost”. |
| MONGO_PORT     | The port number of your MongoDB server. Default: 27017. |
| MONGO_DATABASE | The database name to make available as the db attribute. Default: app.name for Flask or the filename of the including file without the .py extension |
| MONGO_USERNAME | The user name for authentication. Default: None |
| MONGO_PASSWORD | The password for authentication. Default: None |
| MONGO_KWARGS   | A dictionary of keyword arguments to send to [pymongo.MongoClient](http://api.mongodb.org/python/current/api/pymongo/mongo_client.html) |