from flask import request, jsonify, session, render_template
from models import db, User, Question, Answer, Exam


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
    questao2 = Question(question='Quanto é meia dúzia?',
                        answer='6')
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
    # Example logic to check if the user is authenticated
    # You should replace this with your own authentication logic
    if 'usuario_id' in session:
        return True
    return False


def index():
    return render_template('index.html')


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


def login():
    data = request.get_json()
    usuario = User.query.filter_by(username=data['usuario']).first()
    if usuario and usuario.password == data['senha']:
        session['usuario_id'] = usuario.id
        return jsonify({"perfil": usuario.profile})
    return jsonify({"error": "Usuário ou senha inválidos"})


def create_exam():
    if 'usuario_id' not in session:
        return jsonify({"error": "Acesso não autorizado"})

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    questions = data.get('questions')
    total_score = data.get('total_score')

    if not title or not description or not total_score:
        return jsonify({"error": "Dados incompletos"})

    if not questions or not isinstance(questions, list):
        return jsonify({"error": "Questões inválidas"})

    new_exam = Exam(title=title, description=description, total_score=total_score, answered=False)
    db.session.add(new_exam)

    for question_data in questions:
        question_id = question_data.get('id')
        question_score = question_data.get('score')
        question = Question.query.get(int(question_id))
        if question:
            new_exam.questions.append(question)
            question.score = question_score

    db.session.commit()

    return jsonify({"message": "Exame criado com sucesso"}), 201


def responder_exame(exame_id):
    if 'usuario_id' not in session:
        return jsonify({"error": "Acesso não autorizado"})

    exame = Exam.query.get(exame_id)
    if exame and exame.status == 'aberto' and not exame.answered:
        data = request.get_json()
        respostas = data.get('respostas')

        if not respostas:
            return jsonify({"error": "Nenhuma resposta fornecida"})

        for questao_id, resposta in respostas.items():
            nova_resposta = Answer(
                exame_id=exame_id,
                questao_id=int(questao_id),
                resposta=resposta
            )
            db.session.add(nova_resposta)

        exame.answered = True
        db.session.commit()
        return jsonify({"message": "Exame respondido com sucesso"})

    return jsonify({"error": "Exame não encontrado ou não está aberto para resposta"})


def relatorio_exame(exame_id):
    if not autenticado():
        return jsonify({"error": "Acesso não autorizado"})

    exame = Exam.query.get(exame_id)

    if not exame:
        return jsonify({"error": "Exame não encontrado"})

    if exame.status != 'encerrado':
        return jsonify({"error": "Exame não está encerrado"})

    respostas = []
    for question in exame.questions:
        resposta = Answer.query.filter_by(
            exame_id=exame_id, questao_id=question.id).first()
        if resposta:
            respostas.append({
                "pergunta": question.question,
                "resposta": resposta.resposta,
                "correta": question.answer
            })
        else:
            respostas.append({
                "pergunta": question.question,
                "resposta": None,
                "correta": question.answer
            })

    return jsonify({"respostas": respostas})


def create_question():
    request_data = request.get_json()
    question_text = request_data.get('question')
    answer_text = request_data.get('answer')
    if not question_text or not answer_text:
        return jsonify({'error': 'Missing required fields'}), 400

    new_question = Question(question=question_text, answer=answer_text)
    db.session.add(new_question)
    db.session.commit()

    return jsonify({'message': 'Question created successfully'}), 201


def close_exam(exame_id):
    if not autenticado():
        return jsonify({"error": "Acesso não autorizado"})

    exame = Exam.query.get(exame_id)

    if not exame:
        return jsonify({"error": "Exame não encontrado"})

    exame.status = "encerrado"
    db.session.commit()

    return jsonify({"message": "Exame encerrado com sucesso"})
