from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from controllers import seed_data, registro, login, create_exam, responder_exame, relatorio_exame, create_question, close_exam, visualizar_resultados, avaliar_exame
from models import User, Question, Answer, Exam, db  
import secrets


secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = secret_key


@app.before_first_request
def create_tables():
    seed_data()


@app.route('/')
def index():
    return render_template('index.html', css_file='styles.css')


@app.route('/registro', methods=['GET', 'POST'])
def register_route():
    if request.method == 'POST':
        return registro()
    else:
        error = None
        return render_template('registro.html', error=error, css_file='styles.css')


@app.route('/login', methods=['POST', 'GET'])
def login_route():
    if request.method == 'POST':
        return login()
    else:
        error = None
        return render_template('login.html', error=error, css_file='styles.css')


@app.route('/exames', methods=['GET', 'POST'])
def create_exam_route():
    return create_exam()

@app.route('/questions', methods=['POST'])
def create_question_route():
    return create_question()


@app.route('/exames/<int:exame_id>/close', methods=['POST'])
def close_exam_route(exame_id):
    return close_exam(exame_id)


@app.route('/visualizar_resultados')
def visualizar_resultados_route():
    return visualizar_resultados()


@app.route('/exames/<int:exame_id>/avaliar', methods=['POST'])
def evaluate_exam_route(exame_id):
    return avaliar_exame(exame_id)

CORS(app, resources={r"/get_questions": {"origins": "*"}})

# Rota para obter as questões em formato JSON
@app.route('/get_questions', methods=['GET', 'POST'])
def get_questions():
    try:
        if request.method == 'GET':
            questions = Question.query.all()
            questions_data = [
                {'id': question.id, 'question': question.question}
                for question in questions
            ]
            return jsonify(questions_data)
        elif request.method == 'POST':
            # Handle the POST request if needed
            pass
    except Exception as e:
        return jsonify({'error': str(e)}), 500
 
# Route to render the student dashboard
@app.route('/dashboard_student')
def student_dashboard():
    return render_template('aluno.html', css_file='aluno.css')


# Route to answer individual questions in an exam
@app.route('/exames/<int:exame_id>/responder', methods=['POST'])
def responder_exame_route(exame_id):
    if 'usuario_id' not in session:
        return jsonify({"error": "Acesso não autorizado"})

    exame = Exam.query.get(exame_id)
    if not exame:
        return jsonify({"error": "Exame não encontrado"})

    data = request.get_json()
    respostas = data.get('respostas')

    if not respostas:
        return jsonify({"error": "Nenhuma resposta fornecida"})

    user_id = session['usuario_id']

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
    user_answers = Answer.query.filter_by(exame_id=exame_id, user_id=user_id).all()
    total_score_user = sum(answer.pontuacao for answer in user_answers)

    # Atualizar a pontuação total do exame no modelo Exam
    exame.total_score = total_score

    exame.answered = True
    db.session.commit()

    return jsonify({"feedback": feedback, "total_score": total_score})


# Route to generate the exam report for the student
@app.route('/exames/<int:exame_id>/relatorio', methods=['GET'])
def exam_report_route(exame_id):
    exame = Exam.query.get(exame_id)

    if not exame:
        return jsonify({"error": "O exame não foi encontrado"})

    user_id = session.get('usuario_id')  # Retrieve the user_id from the session

    if 'professor' in session.get('profile'):
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


# Route to load questions based on the exam ID
@app.route('/exames/<int:exame_id>/questions', methods=['GET'])
def load_exam_questions(exame_id):
    exame = Exam.query.get(exame_id)

    if not exame:
        return jsonify({"error": "O exame não foi encontrado"})

    questions = exame.questions
    questions_data = [{"id": question.id, "question": question.question} for question in questions]

    return jsonify({"questions": questions_data})

if __name__ == '__main__':
    app.run(debug=True)
