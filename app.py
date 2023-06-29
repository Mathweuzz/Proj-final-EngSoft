from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app  = Flask(__name__)
app.secret_key = "mybd"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///first.db'
db = SQLAlchemy(app)

@app.route('/')
def home():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)