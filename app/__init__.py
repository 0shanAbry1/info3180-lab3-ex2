from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '$&M4u;)'

from app import views
