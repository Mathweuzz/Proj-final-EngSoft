from flask import Flask, request
from view import register_user, login_user, create_exam, submit_exam, get_exam_report, create_question
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Replace with your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite3:///database.db'
db = SQLAlchemy(app)


@app.route('/registro', methods=['POST'])
def registro():
    return register_user(request)


@app.route('/login', methods=['POST'])
def login():
    return login_user(request)


@app.route('/exames', methods=['POST'])
def cadastrar_exame():
    return create_exam(request)


@app.route('/exames/<int:exame_id>/responder', methods=['POST'])
def responder_exame(exame_id):
    return submit_exam(request, exame_id)


@app.route('/exames/<int:exame_id>/relatorio', methods=['GET'])
def relatorio_exame(exame_id):
    return get_exam_report(exame_id)


@app.route('/questions', methods=['POST'])
def create_question_endpoint():
    return create_question(request)


if __name__ == '__main__':
    app.run(debug=True)
