from flask import jsonify, request
from models import db, User, Exam, Question, Answer

def register_user(request):
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    profile = data.get('profile')

    if not username or not email or not password or not profile:
        return jsonify({'error': 'Missing required fields'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 409

    new_user = User(username=username, email=email, password=password, profile=profile)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

def login_user(request):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return jsonify({'profile': user.profile}), 200

    return jsonify({'error': 'Invalid username or password'}), 401

def create_exam(request):
    data = request.get_json()
    status = data.get('status')
    answered = data.get('answered')
    question_ids = data.get('question_ids')

    if not status or not answered or not question_ids:
        return jsonify({'error': 'Missing required fields'}), 400

    questions = Question.query.filter(Question.id.in_(question_ids)).all()
    if len(questions) != len(question_ids):
        return jsonify({'error': 'Invalid question IDs'}), 400

    new_exam = Exam(status=status, answered=answered)
    new_exam.questions.extend(questions)
    db.session.add(new_exam)
    db.session.commit()

    return jsonify({'message': 'Exam created successfully'}), 201

def submit_exam(request, exam_id):
    data = request.get_json()
    answers = data.get('answers')

    if not answers:
        return jsonify({'error': 'No answers provided'}), 400

    exam = Exam.query.get(exam_id)
    if not exam or exam.status != 'aberto' or exam.answered:
        return jsonify({'error': 'Invalid exam or exam is not open for submission'}), 400

    for question_id, answer in answers.items():
        question = Question.query.get(question_id)
        if question:
            new_answer = Answer(exam_id=exam_id, question_id=question_id, answer=answer)
            db.session.add(new_answer)

    exam.answered = True
    db.session.commit()

    return jsonify({'message': 'Exam submitted successfully'}), 200

def get_exam_report(exam_id):
    exam = Exam.query.get(exam_id)

    if not exam:
        return jsonify({'error': 'Exam not found'}), 404

    if exam.status != 'encerrado':
        return jsonify({'error': 'Exam is not closed'}), 400

    answers = Answer.query.filter_by(exam_id=exam.id).all()

    response = []
    for answer in answers:
        question = Question.query.get(answer.question_id)
        response.append({
            'question': question.question,
            'answer': answer.answer
        })

    return jsonify({'respostas': response}), 200
