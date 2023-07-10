from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    profile = db.Column(db.String(50), nullable=False)

    def __init__(self, username, email, password, profile):
        self.username = username
        self.email = email
        self.password = password
        self.profile = profile

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'profile': self.profile
        }

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(500), nullable=False)

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer
        }

class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    answer = db.Column(db.String(500), nullable=False)

    exam = db.relationship('Exam', backref=db.backref('answers', lazy=True))
    question = db.relationship('Question', backref=db.backref('answers', lazy=True))

    def __init__(self, exam_id, question_id, answer):
        self.exam_id = exam_id
        self.question_id = question_id
        self.answer = answer

    def to_dict(self):
        return {
            'id': self.id,
            'exam_id': self.exam_id,
            'question_id': self.question_id,
            'answer': self.answer
        }

class Exam(db.Model):
    __tablename__ = 'exams'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    answered = db.Column(db.Boolean, nullable=False)

    def __init__(self, status, answered):
        self.status = status
        self.answered = answered

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'answered': self.answered
        }
