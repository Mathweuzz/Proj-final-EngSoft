from os import abort
from flask import request, jsonify, session, render_template
from flask_login import current_user
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
        question_type="dissertation", question='Qual é a capital do Brasil?', answer='Brasília', score='30')
    questao2 = Question(question_type="dissertation", question='Quanto é meia dúzia?',
                        answer='6', score='30')
    db.session.add(questao1)
    db.session.add(questao2)

    exame1 = Exam(status='aberto', answered=False, title='Exame de Geografia',
                  description='Exame de Geografia do Brasil', total_score='60')
    exame1.questions.append(questao1)
    exame1.questions.append(questao2)
    db.session.add(exame1)

    exame2 = Exam(status='aberto', answered=True, title='Exame de Matemática',
                  description='Exame de Matemática Básica', total_score='60')
    exame2.questions.append(questao1)
    db.session.add(exame2)

    exame3 = Exam(status='agendado', answered=False, title='Exame de Português',
                  description='Exame de Português Básico', total_score='60')
    exame3.questions.append(questao2)
    db.session.add(exame3)

    db.session.commit()

    db.create_all()


def autenticado():
    if 'usuario_id' in session:
        return True
    return False


def registro():
    if request.headers.get('Content-Type') == 'application/json':
        data = request.get_json()
        usuario = User.query.filter_by(username=data['usuario']).first()
        if usuario:
            return jsonify({"error": "Usuário já existe"})
        novo_usuario = User(username=data['usuario'], email=data['email'],
                            password=data['senha'], profile=data['perfil'])
        db.session.add(novo_usuario)
        db.session.commit()
        return jsonify({"message": "Usuário registrado com sucesso"})
    else:
        try:
            # Handle the form submission and create a new user
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            role = request.form['role']

            # Check if the user already exists in the database
            usuario = User.query.filter_by(username=username).first()
            if usuario:
                error = "Usuário já existe, gostaria de logar?"
                return render_template('registro.html', msg=error, css_file='styles.css')

            # Create a new user in the database
            new_user = User(username=username, email=email,
                            password=password, profile=role)
            db.session.add(new_user)
            db.session.commit()

            # Return a response or redirect to another page
            success = "Usuário registrado com sucesso"
            return render_template('registro.html', msg=success, css_file='styles.css')

        except:
            error = "Erro ao registrar usuário"
            return render_template('registro.html', msg=error, css_file='styles.css')


def login():
    if request.method == 'POST':
        data = request.form
        usuario = User.query.filter_by(username=data['usuario']).first()
        if usuario and usuario.password == data['senha']:
            session['usuario_id'] = usuario.id
            session['profile'] = usuario.profile
            if usuario.profile == 'professor':
                return render_template('dashboard.html', css_file='styles.css')
            elif usuario.profile == 'estudante':
                return render_template('aluno.html', css_file='styles.css')
        error = "Usuário ou senha inválidos"
    else:
        error = None
    return render_template('index.html', error=error)


def create_exam():
    if 'usuario_id' not in session:
        return jsonify({"error": "Acesso não autorizado"})

    data = request.get_json()
    status = data.get('status')
    title = data.get('title')
    description = data.get('description')
    questions = data.get('questions')
    total_score = data.get('total_score')

    if not status or not title or not description or not total_score:
        return jsonify({"error": "Dados incompletos"})

    if not questions or not isinstance(questions, list):
        return jsonify({"error": "Questões inválidas"})

    new_exam = Exam(status=status, answered=False, title=title, description=description,
                    total_score=total_score)
    db.session.add(new_exam)

    for question_data in questions:
        question_id = question_data.get('id')
        question = Question.query.get(question_id)
        if not question:
            return jsonify({"error": "Questão não encontrada"})
        new_exam.questions.append(question)

    db.session.commit()
    return jsonify({"success": f"Exame criado com sucesso. ID do novo exame: {new_exam.id}"})


def responder_exame(exame_id):
    if 'usuario_id' not in session:
        return jsonify({"error": "Acesso não autorizado"})

    exame = Exam.query.get(exame_id)
    if not exame:
        return jsonify({"error": "Exame não encontrado"})

    data = request.get_json()
    respostas = data.get('respostas')

    if not respostas:
        return jsonify({"error": "Nenhuma resposta fornecida"})

    user_id = session['usuario_id']  # Retrieve the user_id from the session

    for questao_id, resposta in respostas.items():
        nova_resposta = Answer(
            exame_id=exame_id,
            questao_id=int(questao_id),
            resposta=resposta,
            user_id=user_id  # Include the user_id in the nova_resposta object
        )
        db.session.add(nova_resposta)

    exame.answered = True
    db.session.commit()
    return jsonify({"success": "Exame respondido com sucesso"})


def relatorio_exame(exame_id):
    exame = Exam.query.get(exame_id)

    if not exame:
        return jsonify({"error": "O exme não foi encontrad"})

    if exame.status != 'encerrado':
        return jsonify({"error": "O exame não foi encerrado"})

    respostas = []
    for question in exame.questions:
        if current_user.profile == 'estudante':
            questao_respostas = Answer.query.filter_by(
                exame_id=exame_id, questao_id=question.id, user_id=current_user.id).all()
        else:
            questao_respostas = Answer.query.filter_by(
                exame_id=exame_id, questao_id=question.id).all()

        for resposta in questao_respostas:
            if resposta.resposta == question.answer:
                score = question.score
            else:
                score = 0
            respostas.append({
                "pergunta": question.question,
                "resposta": resposta.resposta,
                "correta": question.answer,
                "usuario": resposta.user_id,
                "pontuacao": score
            })

    return jsonify({"respostas": respostas})


def create_question():
    request_data = request.get_json()
    question_type = request_data.get('question_type')
    question_text = request_data.get('question')
    answer_text = request_data.get('answer')
    score_text = request_data.get('score')
    if not question_text or not answer_text:
        return jsonify({'error': 'Missing required fields'}), 400

    new_question = Question(question_type=question_type, question=question_text,
                            answer=answer_text, score=score_text)

    if question_type == 'multiple_choice':
        options = request_data.get('options')
        if not options:
            return jsonify({'error': 'Multiple-choice questions require at least one option'}), 400
        new_question.options = options

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


def avaliar_respostas(exame_id):
    if not autenticado():
        return jsonify({"error": "Acesso não autorizado"})

    exame = Exam.query.get(exame_id)

    if not exame:
        return jsonify({"error": "Exame não encontrado"})

    if exame.status != 'encerrado':
        return jsonify({"error": "Exame não está encerrado"})

    respostas_alunos = Answer.query.filter_by(exame_id=exame_id).all()
    pontuacao_total = 0

    for resposta in respostas_alunos:
        questao = Question.query.get(resposta.questao_id)
        if questao and resposta.resposta == questao.answer:
            resposta.pontuacao = questao.score
            pontuacao_total += questao.score

    exame.answered = True
    db.session.commit()

    return jsonify({"message": "Respostas avaliadas com sucesso", "pontuacao_total": pontuacao_total})


def visualizar_resultados():
    if not autenticado():
        return jsonify({"error": "Acesso não autorizado"})

    exame_id = request.args.get('exame_id')

    if not exame_id:
        return jsonify({"error": "Filtros não especificados"})

    if exame_id:
        exame = Exam.query.get(exame_id)
        if not exame:
            return jsonify({"error": "Exame não encontrado"})

        if not exame.status == 'encerrado':
            return jsonify({"error": "Exame ainda não encerrado"})

        alunos = User.query.filter_by(profile='estudante').all()
        resultados = []
        for aluno in alunos:
            resposta = Answer.query.filter_by(
                exame_id=exame_id, user_id=aluno.id).first()
            if resposta:
                resultados.append({
                    "aluno": aluno.username,
                    "pontuacao": resposta.pontuacao
                })

        return jsonify({"resultados": resultados})

    alunos = User.query.filter_by(profile='estudante').all()
    resultados = []
    for aluno in alunos:
        exames_respondidos = Exam.query.filter(
            Exam.id == Answer.exame_id, Answer.user_id == aluno.id, Exam.status == 'encerrado')

        pontuacao_total = sum(exame.pontuacao for exame in exames_respondidos)
        resultados.append({
            "aluno": aluno.username,
            "pontuacao_total": pontuacao_total
        })

    return jsonify({"resultados": resultados})


def avaliar_exame(exame_id):
    exame = Exam.query.get(exame_id)

    if not exame:
        return jsonify({"error": "Exame não encontrado"})

    if exame.status != 'encerrado':
        return jsonify({"error": "Exame não está encerrado"})

    resultados = []
    for aluno in User.query.filter_by(profile='estudante').all():
        pontuacao_total = 0
        for questao in exame.questions:
            resposta = Answer.query.filter_by(
                exame_id=exame_id, questao_id=questao.id, user_id=aluno.id).first()
            if resposta and resposta.resposta == questao.answer:
                pontuacao_total += questao.score

        resultados.append({
            "aluno": aluno.username,
            "pontuacao_total": pontuacao_total
        })

    return jsonify({"resultados": resultados})


def responder_exame(exame_id):
    if 'usuario_id' not in session:
        return jsonify({"error": "Acesso não autorizado"})

    exame = Exam.query.get(exame_id)
    if not exame:
        return jsonify({"error": "Exame não encontrado"})

    if exame.status == 'encerrado':
        return jsonify({"error": "O exame já foi encerrado. Não é permitido responder novamente."})

    # Verificar se o aluno já respondeu o exame anteriormente
    user_id = session['usuario_id']
    user_has_answered = Answer.query.filter_by(
        exame_id=exame_id, user_id=user_id).first()

    if user_has_answered:
        return jsonify({"error": "Você já respondeu esse exame. Não é permitido responder novamente."})

    data = request.get_json()
    respostas = data.get('respostas')

    if not respostas:
        return jsonify({"error": "Nenhuma resposta fornecida"})

    total_score = 0
    feedback = []
    for questao_id, resposta_aluno in respostas.items():
        questao = Question.query.get(int(questao_id))
        if not questao:
            return jsonify({"error": "Questão não encontrada"})

        score = 0
        if resposta_aluno == questao.answer:
            score = questao.score
            total_score += score

        feedback.append({
            "questao": questao.question,
            "resposta_aluno": resposta_aluno,
            "resposta_correta": questao.answer,
            "pontuacao": score
        })

        # Salvar as respostas do aluno no banco de dados (se necessário)
        nova_resposta = Answer(
            exame_id=exame_id,
            questao_id=int(questao_id),
            resposta=resposta_aluno,
            user_id=user_id,
            pontuacao=score
        )
        db.session.add(nova_resposta)

    # Atualizar a pontuação total do aluno para o exame no modelo Answer
    user_answers = Answer.query.filter_by(
        exame_id=exame_id, user_id=user_id).all()
    total_score_user = sum(answer.pontuacao for answer in user_answers)

    # Atualizar a pontuação total do exame no modelo Exam
    exame.total_score = total_score

    exame.answered = True
    db.session.commit()

    return jsonify({"feedback": feedback, "total_score": total_score})


def exam_report(exame_id):
    exame = Exam.query.get(exame_id)

    if not exame:
        return jsonify({"error": "O exame não foi encontrado"})

    # Retrieve the user_id from the session
    user_id = session.get('usuario_id')

    if 'professor' in session.get('profile'):
        print('teste')
        # If the user is a teacher, retrieve all exam submissions
        all_submissions = Answer.query.filter_by(exame_id=exame_id).all()

        respostas = []
        for submission in all_submissions:
            questao = Question.query.get(submission.questao_id)
            respostas.append({
                "aluno": submission.user_id,
                "questao": questao.question,
                "resposta_aluno": submission.resposta,
                "resposta_correta": questao.answer,
                "pontuacao": submission.pontuacao
            })

        return jsonify({"respostas": respostas})

    else:
        if exame.status == 'aberto':
            return jsonify({"error": "O relatório ainda não pode ser gerado, pois o exame está aberto."})
        # If the user is a student, retrieve their exam submission only
        user_submission = Answer.query.filter_by(
            exame_id=exame_id, user_id=user_id).all()

        respostas = []
        for submission in user_submission:
            questao = Question.query.get(submission.questao_id)
            respostas.append({
                "aluno": user_id,
                "questao": questao.question,
                "resposta_aluno": submission.resposta,
                "resposta_correta": questao.answer,
                "pontuacao": submission.pontuacao
            })

        return jsonify({"respostas": respostas})


def load_exam_questions(exame_id):
    exame = Exam.query.get(exame_id)

    if not exame:
        return jsonify({"error": "O exame não foi encontrado"})

    if exame.status == 'encerrado':
        return jsonify({"error": "O exame já foi encerrado. Não é permitido responder novamente."})

    questions = exame.questions
    questions_data = [{"id": question.id, "question": question.question, "question_type": question.question_type}
                      for question in questions]

    return jsonify({"questions": questions_data})


def check_exam_answered(exame_id):
    user_id = session.get('usuario_id')
    if not user_id:
        # O aluno não está logado, então ainda não respondeu
        return jsonify({"respondeu": False})

    exame_respondido = Answer.query.filter_by(
        exame_id=exame_id, user_id=user_id).first()
    if exame_respondido:
        return jsonify({"respondeu": True})  # O aluno já respondeu o exame
    else:
        # O aluno ainda não respondeu o exame
        return jsonify({"respondeu": False})
