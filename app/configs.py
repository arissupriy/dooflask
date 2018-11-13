from flask import Flask
from mongoengine import connect
from . import errors
import os, configparser

BASE = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

CONF = configparser.ConfigParser()
CONF.read(os.path.join(BASE, 'dooflask.conf'))

class Config:
    def __init__(self):
        self.project_name = self.ConfigParser('project').get('name', 'app')
        
        os.environ['FLASK_ENV'] = self.ConfigParser('project').get('status', 'development')
        os.environ['FLASK_APP'] = self.project_name
        os.environ['DOOFLASK_PORT'] = self.ConfigParser('project').get('port', 5000)
        os.environ['DOOFLASK_HOST'] = self.ConfigParser('project').get('host', 'localhost')
    
    def ConfigParser(self, section):
        dict1 = {}
        options = CONF.options(section)
        for option in options:
            try:
                dict1[option] = CONF.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    @property
    def database(self):
        if 'database' not in CONF.sections():
            raise errors.ConfigError('database config not found in project.conf')
        
        DB = self.ConfigParser('database')

        return connect(
            db=DB['name'],
            username=DB.get('username'),
            password=DB.get('password'),
            host=DB.get('host'),
            port=int(DB.get('port')) if DB.get('port') is not None else None
        )
    
    def init_app(self):
        return Flask(
            self.project_name
        )
