from flask import Flask
from models import db
from views import app

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
