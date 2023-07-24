import pytest
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Question, Exam, Answer
from controller import app, seed_data

# Configurações para o ambiente de testes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

# Inicializar o banco de dados
db.init_app(app)


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            seed_data()
            yield client
            db.session.remove()
            db.drop_all()


def login(client, username, password):
    return client.post('/login', data=dict(usuario=username, senha=password), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_register(client):
    # Teste de registro de novo usuário
    response = client.post('/registro', data=dict(
        usuario='novousuario',
        email='novousuario@example.com',
        senha='password',
        perfil='estudante'
    ), follow_redirects=True)

    assert "Usuário registrado com sucesso".encode() in response.data

    # Teste de registro de usuário já existente
    response = client.post('/registro', data=dict(
        usuario='novousuario',
        email='novousuario@example.com',
        senha='password',
        perfil='estudante'
    ), follow_redirects=True)

    assert "Usuário já existe".encode() in response.data


def test_login_logout(client):
    # Registrar um usuário para testar o login
    new_user = User(
        username='usertest',
        email='usertest@example.com',
        password='password',
        profile='estudante'
    )
    db.session.add(new_user)
    db.session.commit()

    # Teste de login com credenciais corretas
    response = login(client, 'usertest', 'password')
    assert b"dashboard_student" in response.data

    # Teste de login com credenciais incorretas
    response = login(client, 'usertest', 'senhaerrada')
    assert "Usuário ou senha inválidos".encode() in response.data

    # Teste de logout
    response = logout(client)
    assert b"login" in response.data


def test_create_exam(client):
    # Registrar um professor para testar a criação de exame
    new_user = User(
        username='professor',
        email='professor@example.com',
        password='password',
        profile='professor'
    )
    db.session.add(new_user)
    db.session.commit()

    # Realizar login como professor
    login(client, 'professor', 'password')

    # Teste de criação de exame com sucesso
    response = client.post('/exames', json=dict(
        status='aberto',
        title='Exame Teste',
        description='Descrição do exame teste',
        questions=[]
    ))
    assert response.status_code == 200
    assert b"Exame criado com sucesso" in response.data

    # Teste de criação de exame sem título
    response = client.post('/exames', json=dict(
        status='aberto',
        description='Descrição do exame teste',
        questions=[]
    ))
    assert response.status_code == 400
    assert b"Dados incompletos" in response.data

    # Teste de criação de exame com questões inválidas
    response = client.post('/exames', json=dict(
        status='aberto',
        title='Exame Teste',
        description='Descrição do exame teste',
        questions='invalid-questions'
    ))
    assert response.status_code == 400
    assert "Questões inválidas".encode() in response.data


def test_responder_exame(client):
    # Registrar um estudante para testar as respostas do exame
    new_user = User(
        username='estudante',
        email='estudante@example.com',
        password='password',
        profile='estudante'
    )
    db.session.add(new_user)
    db.session.commit()

    # Registrar um exame para testar a resposta
    new_exam = Exam(
        status='aberto',
        answered=False,
        title='Exame Teste',
        description='Descrição do exame teste'
    )
    db.session.add(new_exam)

    # Registrar uma questão para o exame
    new_question = Question(
        question='Questão Teste',
        answer='Resposta Teste',
        score=10
    )
    db.session.add(new_question)
    new_exam.questions.append(new_question)
    db.session.commit()

    # Realizar login como estudante
    login(client, 'estudante', 'password')

    # Teste de resposta do exame
    response = client.post(f'/exames/{new_exam.id}/responder', json=dict(
        respostas={new_question.id: 'Resposta Teste'}
    ))
    assert response.status_code == 200
    assert b"Exame respondido com sucesso" in response.data

    # Teste de resposta repetida do exame
    response = client.post(f'/exames/{new_exam.id}/responder', json=dict(
        respostas={new_question.id: 'Resposta Teste'}
    ))
    assert response.status_code == 200
    assert "Você já respondeu esse exame".encode() in response.data


def test_exam_report(client):
    # Registrar um estudante para testar o relatório do exame
    new_user = User(
        username='estudante',
        email='estudante@example.com',
        password='password',
        profile='estudante'
    )
    db.session.add(new_user)
    db.session.commit()

    # Registrar um exame para testar o relatório
    new_exam = Exam(
        status='encerrado',
        answered=True,
        title='Exame Teste',
        description='Descrição do exame teste'
    )
    db.session.add(new_exam)

    # Registrar uma questão para o exame
    new_question = Question(
        question='Questão Teste',
        answer='Resposta Teste',
        score=10
    )
    db.session.add(new_question)
    new_exam.questions.append(new_question)
    db.session.commit()

    # Registrar a resposta do estudante para a questão
    new_answer = Answer(
        user_id=new_user.id,
        exam_id=new_exam.id,
        question_id=new_question.id,
        answer='Resposta Teste',
        score=10
    )
    db.session.add(new_answer)
    db.session.commit()

    # Realizar login como estudante
    login(client, 'estudante', 'password')

    # Teste de relatório do exame para estudante
    response = client.get(f'/exames/{new_exam.id}/relatorio')
    assert response.status_code == 200
    assert "Questão Teste".encode() in response.data
    assert "Resposta Teste".encode() in response.data
    assert "Resposta Correta".encode() in response.data
    assert "Pontuação".encode() in response.data

    # Realizar login como professor
    new_user.profile = 'professor'
    db.session.commit()
    login(client, 'estudante', 'password')

    # Teste de relatório do exame para professor
    response = client.get(f'/exames/{new_exam.id}/relatorio')
    assert response.status_code == 200
    assert "Questão Teste".encode() in response.data
    assert "Resposta Teste".encode() in response.data
    assert "Resposta Correta".encode() in response.data
    assert "Pontuação".encode() in response.data


def test_load_exam_questions(client):
    # Registrar um exame para testar o carregamento de questões
    new_exam = Exam(
        status='aberto',
        answered=False,
        title='Exame Teste',
        description='Descrição do exame teste'
    )
    db.session.add(new_exam)

    # Registrar questões para o exame
    question1 = Question(
        question='Questão 1',
        answer='Resposta 1',
        score=10
    )
    db.session.add(question1)
    new_exam.questions.append(question1)

    question2 = Question(
        question='Questão 2',
        answer='Resposta 2',
        score=20
    )
    db.session.add(question2)
    new_exam.questions.append(question2)

    db.session.commit()

    # Teste de carregamento de questões do exame
    response = client.get(f'/exames/{new_exam.id}/questions')
    assert response.status_code == 200
    assert "Questão 1".encode() in response.data
    assert "Questão 2".encode() in response.data


def test_check_exam_answered(client):
    # Registrar um estudante para testar a resposta do exame
    new_user = User(
        username='estudante',
        email='estudante@example.com',
        password='password',
        profile='estudante'
    )
    db.session.add(new_user)
    db.session.commit()

    # Registrar um exame para testar a resposta do exame
    new_exam = Exam(
        status='aberto',
        answered=False,
        title='Exame Teste',
        description='Descrição do exame teste'
    )
    db.session.add(new_exam)

    # Realizar login como estudante
    login(client, 'estudante', 'password')

    # Teste de resposta do exame
    response = client.post(f'/exames/{new_exam.id}/responder', json=dict(
        respostas={}
    ))
    assert response.status_code == 200
    assert b"Exame respondido com sucesso" in response.data

    # Teste de verificação de resposta do exame para o estudante
    response = client.get(f'/exames/{new_exam.id}/respondeu')
    assert response.status_code == 200
    assert b"true" in response.data

    # Realizar logout
    logout(client)

    # Teste de verificação de resposta do exame para o estudante não logado
    response = client.get(f'/exames/{new_exam.id}/respondeu')
    assert response.status_code == 200
    assert b"false" in response.data
