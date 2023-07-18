# Rodando a aplicação

Após realizar todos os passos descritos no arquivo [run.md], basta abrir um navegador e acessar o endereço http://localhost:5000. A aplicação estará rodando e pronta para uso.

# Página inicial

Na página inicial há duas opções: login e registro. No login, usa-se o nome de usuario e senha cadastrados para acessar a aplicação. No registro, é necessário informar um nome de usuario, senha e se o usuario é professor ou aluno.

# Página do professor

Ao logar, o professor é apresentado à uma página de dashboard com as opções de criar uma nova questão, criar uma nova prova com as questões criadas, gerar relatórios e corrigir provas. Basta clicar na opção desejada e informar o id da prova desejada, se necessário. O relatório (se o usuário logado é um professor) mostra a resposta de todos os alunos, enquanto para um aluno mostra apenas as suas respostas. Para criar uma questão, basta informar o enunciado, a resposta e a pontuação. Para criar uma prova, basta informar os campos de nome da prova e o id das questões que a compõem.

# Página do aluno

Ao logar, o aluno é apresentado à uma página de dashboard com as opções de realizar uma prova e ver o gabarito de uma prova já realizada. Basta clicar na opção desejada e informar o id da prova desejada, se necessário. Para realizar um exame, deve-se inserir o id da prova e responder as questões no formato JSON

```json
{
    "1": "resposta1",
    "2": "resposta2",
    "3": "resposta3",
    ...
}
```

Após a prova ser fechada, o aluno poderá ver um relatório com o resultado da prova, o gabarito para cada questão e sua pontuação em cada uma delas.

# Dados predefinidos

Alguns usuários predefinidos são

```bash
usuario: pedro
senha: asdfg
tipo: professor
```

```bash
usuario: ester
senha: asdfg
tipo: estudante
```

Há 5 testes pré definidos, com id de 1 à 5. Cada uma delas possui 2 questões, com id de 1 à 2. As respostas corretas são

```py
{
  questao1 = Question(question='Qual é a capital do Brasil?', answer='Brasília', score='30')
  questao2 = Question(question='Quanto é meia dúzia?', answer='6', score='30')
}
```
