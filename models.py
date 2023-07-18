from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    profile = db.Column(db.String(50), nullable=False)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(500), nullable=False)
    score = db.Column(db.Integer, nullable=False)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    exame_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    questao_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    resposta = db.Column(db.String(500), nullable=False)
    pontuacao = db.Column(db.Integer, nullable=False, default=0)

    exam = db.relationship(
        'Exam', backref=db.backref('answers', lazy='dynamic'))
    question = db.relationship('Question')


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False, default='aberto')
    answered = db.Column(db.Boolean, nullable=False)
    questions = db.relationship(
        'Question', secondary='exam_question', backref=db.backref('exams', lazy='dynamic'))
    title = db.Column(db.String(200))
    description = db.Column(db.String(500))
    total_score = db.Column(db.Integer, nullable=False, default=0)
    turma = db.Column(db.String(100))
    disciplina = db.Column(db.String(100))
    periodo = db.Column(db.String(100))


exam_question = db.Table('exam_question',
                         db.Column('exam_id', db.Integer, db.ForeignKey(
                             'exam.id'), primary_key=True),
                         db.Column('question_id', db.Integer, db.ForeignKey(
                             'question.id'), primary_key=True)
                         )
