from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    # User model definition...

class Question(db.Model):
    # Question model definition...

class Answer(db.Model):
    # Answer model definition...

class Exam(db.Model):
    # Exam model definition...
