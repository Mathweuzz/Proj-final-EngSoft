1. Register a new user:

   - Method: POST
   - URL: http://localhost:5000/registro
   - Request body (JSON):
     json
     {
     "usuario": "joao",
     "email": "joao@unb.br",
     "senha": "12345",
     "perfil": "estudante"
     }

2. Login as a user:

   - Method: POST
   - URL: http://localhost:5000/login
   - Request body (JSON):
     json
     {
     "usuario": "joao",
     "senha": "12345"
     }

3. Create an exam:

   - Method: POST
   - URL: http://localhost:5000/exames
   - Request body (JSON):
     json
     {
     "questoes": [1, 2]
     }

4. Respond to an exam:

   - Method: POST
   - URL: http://localhost:5000/exames/1/responder
   - Request body (JSON):
     json
     {
     "respostas": {
     "1": "Brasília",
     "2": "Pedro Álvares Cabral"
     }
     }

5. View a report of student answers for an exam:
   - Method: GET
   - URL: http://localhost:5000/exames/1/relatorio

Make sure to replace `localhost:5000` with the correct address and port of your Flask app. Also, ensure that the server is running before making the requests.
