from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from controllers import check_exam_answered, exam_report, load_exam_questions, responder_exame, seed_data, registro, login, create_exam, create_question, close_exam, avaliar_exame
from models import Question, Answer, Exam, db
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
        return render_template('index.html', error=error, css_file='styles.css')


@app.route('/exames', methods=['GET', 'POST'])
def create_exam_route():
    return create_exam()


@app.route('/questions', methods=['POST'])
def create_question_route():
    return create_question()


@app.route('/exames/<int:exame_id>/close', methods=['POST'])
def close_exam_route(exame_id):
    return close_exam(exame_id)


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
    return responder_exame(exame_id)

# Route to generate the exam report for the student


@app.route('/exames/<int:exame_id>/relatorio', methods=['GET'])
def exam_report_route(exame_id):
    return exam_report(exame_id)

# Route to load questions based on the exam ID


@app.route('/exames/<int:exame_id>/questions', methods=['GET'])
def load_exam_questions_route(exame_id):
    return load_exam_questions(exame_id)


@app.route('/exames/<int:exame_id>/respondeu', methods=['GET'])
def check_exam_answered_route(exame_id):
    return check_exam_answered(exame_id)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('usuario_id', None)
    return redirect(url_for('login_route'))


if __name__ == '__main__':
    app.run(debug=True)
