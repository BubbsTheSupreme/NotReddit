import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config():
    FLASK_APP = 'not_reddit.py'
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xd6\x03#"ge{\xc9\x12\x02\xb7A2Z\x0b\x81'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(base_dir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
