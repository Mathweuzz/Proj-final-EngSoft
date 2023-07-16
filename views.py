from flask import Flask, render_template
from controllers import seed_data, registro, login, create_exam, responder_exame, relatorio_exame, create_question, close_exam, visualizar_resultados
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
    return render_template('index.html')


@app.route('/registro', methods=['POST'])
def register():
    return registro()


@app.route('/login', methods=['POST'])
def login_route():
    return login()


@app.route('/exames', methods=['POST'])
def create_exam_route():
    return create_exam()


@app.route('/exames/<int:exame_id>/responder', methods=['POST'])
def answer_exam_route(exame_id):
    return responder_exame(exame_id)


@app.route('/exames/<int:exame_id>/relatorio', methods=['GET'])
def exam_report_route(exame_id):
    return relatorio_exame(exame_id)


@app.route('/questions', methods=['POST'])
def create_question_route():
    return create_question()


@app.route('/exames/<int:exame_id>/close', methods=['POST'])
def close_exam_route(exame_id):
    return close_exam(exame_id)


@app.route('/visualizar_resultados')
def visualizar_resultados_route():
    return visualizar_resultados()


if __name__ == '__main__':
    app.run(debug=True)
