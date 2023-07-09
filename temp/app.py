from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, g, session
import secrets


secret_key = secrets.token_hex(16)


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = secret_key

db = SQLAlchemy(app)


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


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id'), nullable=False)
    answer = db.Column(db.String(500), nullable=False)

    exam = db.relationship('Exam', backref=db.backref('answers', lazy=True))
    question = db.relationship(
        'Question', backref=db.backref('answers', lazy=True))


class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    answered = db.Column(db.Boolean, nullable=False)
    questions = db.relationship(
        'Question', secondary='exam_question', backref=db.backref('exams', lazy='dynamic'))


exam_question = db.Table('exam_question',
                         db.Column('exam_id', db.Integer, db.ForeignKey(
                             'exam.id'), primary_key=True),
                         db.Column('question_id', db.Integer, db.ForeignKey(
                             'question.id'), primary_key=True)
                         )


@app.before_first_request
def seed_data():
    db.drop_all()
    db.create_all()

    pedro = User(username='pedro', email='pedro@unb.br',
                 password='asdfg', profile='professor')
    ester = User(username='ester', email='ester@unb.br',
                 password='asdfg', profile='estudante')
    db.session.add(pedro)
    db.session.add(ester)

    questao1 = Question(
        question='Qual é a capital do Brasil?', answer='Brasília')
    questao2 = Question(question='Quem descobriu o Brasil?',
                        answer='Pedro Álvares Cabral')
    db.session.add(questao1)
    db.session.add(questao2)

    exame1 = Exam(status='aberto', answered=False)
    exame1.questions.append(questao1)
    exame1.questions.append(questao2)
    db.session.add(exame1)

    exame2 = Exam(status='aberto', answered=True)
    exame2.questions.append(questao1)
    db.session.add(exame2)

    exame3 = Exam(status='agendado', answered=False)
    exame3.questions.append(questao2)
    db.session.add(exame3)

    exame4 = Exam(status='encerrado', answered=True)
    exame4.questions.append(questao1)
    exame4.questions.append(questao2)
    db.session.add(exame4)

    exame5 = Exam(status='encerrado', answered=False)
    exame5.questions.append(questao1)
    db.session.add(exame5)

    db.session.commit()

    db.create_all()


def autenticado():
    if 'usuario' in g:
        return True
    return False


@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    usuario = User.query.filter_by(username=data['usuario']).first()
    if usuario:
        return jsonify({"error": "Usuário já existe"})
    novo_usuario = User(username=data['usuario'], email=data['email'],
                        password=data['senha'], profile=data['perfil'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({"message": "Usuário registrado com sucesso"})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = User.query.filter_by(username=data['usuario']).first()
    if usuario and usuario.password == data['senha']:
        session['usuario_id'] = usuario.id
        return jsonify({"perfil": usuario.profile})
    return jsonify({"error": "Usuário ou senha inválidos"})


@app.route('/exames', methods=['POST'])
def cadastrar_exame():
    if 'usuario_id' not in session:
        return jsonify({"error": "Acesso não autorizado"})
    data = request.get_json()
    questoes = data['questoes']
    novo_exame = Exam(questoes=questoes, status='aberto', respondido=False)
    db.session.add(novo_exame)
    db.session.commit()
    return jsonify({"message": "Exame cadastrado com sucesso"})


@app.route('/exames/<int:exame_id>/responder', methods=['POST'])
def responder_exame(exame_id):
    if 'usuario_id' not in session:
        return jsonify({"error": "Acesso não autorizado"})
    exame = Exam.query.get(exame_id)
    if exame and exame.status == 'aberto' and not exame.respondido:
        data = request.get_json()
        respostas = data['respostas']
        for questao_id, resposta in respostas.items():
            nova_resposta = Answer(
                exame_id=exame_id, questao_id=questao_id, resposta=resposta)
            db.session.add(nova_resposta)
        exame.respondido = True
        db.session.commit()
        return jsonify({"message": "Exame respondido com sucesso"})
    return jsonify({"error": "Exame não encontrado ou não está aberto para resposta"})


@app.route('/exames/<int:exame_id>/relatorio', methods=['GET'])
def relatorio_exame(exame_id):
    if not autenticado():
        return jsonify({"error": "Acesso não autorizado"})

    exame = Exam.query.get(exame_id)

    if not exame:
        return jsonify({"error": "Exame não encontrado"})

    if exame.status != 'encerrado':
        return jsonify({"error": "Exame não está encerrado"})

    respostas = []
    for questao in exame.questoes:
        resposta = Answer.query.filter_by(
            exame_id=exame.id, questao_id=questao.id).first()
        if resposta:
            respostas.append({
                "pergunta": questao.pergunta,
                "resposta": resposta.resposta
            })

    return jsonify({"respostas": respostas})


if __name__ == '__main__':
    app.run(debug=True)
