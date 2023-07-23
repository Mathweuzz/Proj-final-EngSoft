# Proj-final-EngSoft

Repositório do projeto
https://github.com/Mathweuzz/Proj-final-EngSoft

Participantes

Eduardo Marques Pereira - 211021004

Gabriel Amaro Baxto - 190087331

Mateus Gomes de Araújo - 202014440

Yan Tavares de Oliveira - 202014323

# Relatório da Entrega 2

O objetivo da Entrega 2 foi realizar as tarefas planejadas de acordo com o documento "Doc. de Especificação". Durante a interação, foram definidos os seguintes itens:

## O que foi planejado no início da interação:

1. Implementar o sistema de autenticação de usuários.
2. Desenvolver a funcionalidade de criação de questões.
3. Adicionar a capacidade de criação de exames com base em questões selecionadas.
4. Implementar a funcionalidade de resposta a exames.
5. Adicionar a opção de gerar relatórios com base nas respostas aos exames.
6. Implementar o encerramento de exames.

## O que foi concluído:

1. Issue #1: Implementação do sistema de autenticação de usuários.
2. Issue #2: Desenvolvimento da funcionalidade de criação de questões.
3. Issue #3: Adição da capacidade de criação de exames com base em questões selecionadas.
4. Issue #4: Implementação da funcionalidade de resposta a exames.
5. Issue #5: Adição da opção de gerar relatórios com base nas respostas aos exames.
6. Issue #6: Implementação do encerramento de exames.

## O que voltou para o backlog:

N/A

## Estado atual do projeto:

Até o momento, os seguintes requisitos já foram atendidos:

- Sistema de autenticação de usuários implementado.
- Funcionalidade de criação de questões desenvolvida.
- Capacidade de criar exames com base em questões selecionadas adicionada.
- Funcionalidade de resposta a exames implementada.
- Opção de gerar relatórios com base nas respostas aos exames adicionada.
- Encerramento de exames foi implementado.

## O que será desenvolvido na próxima iteração:

1. Melhorias na interface do usuário para uma experiência mais intuitiva.
2. Implementação de notificações para usuários sobre ações importantes.
3. Adição de testes automatizados para garantir a qualidade do código.
4. Melhorias de desempenho e otimização da aplicação.
5. Refatoração do código para melhor organização e legibilidade.

## Sprint Review:

O que foi bem =)

- O sistema de autenticação de usuários foi implementado de forma segura e funcional.
- As funcionalidades de criação de questões e exames foram concluídas conforme o planejado.
- A resposta a exames e geração de relatórios estão funcionando corretamente.

O que foi mal =(

- Houve um atraso na implementação do encerramento de exames, causando um pequeno atraso na entrega.

## Pontos a melhorar:

- Melhorar a comunicação entre a equipe para evitar atrasos e garantir um fluxo de trabalho mais eficiente.
- Aumentar a cobertura de testes automatizados para garantir a estabilidade e qualidade do código.
- Realizar uma revisão mais detalhada antes da entrega para evitar problemas de última hora.

# Relatório da Entrega 3

O objetivo da Entrega 2 foi finalizar todas as tarefas planejadas de acordo com o documento "Doc. de Especificação". Durante a interação, foram definidos os seguintes itens:

## O que foi planejado no início da interação:

1. Implementar dashboards funccionais para aluno e professor.
2. Desenvolver a funcionalidade de correção automática de provas e relatórios mais detalhados.
3. Implementação de diferentes tipos de questão (Múltipla esocolha e Verdadeiro ou Falso).
4. Criação de um design limpo e responsivo para o site.
5. Adição de testes automatizados para garantir a qualidade do código.
6. Refatoração do código para melhor organização e legibilidade.

## O que foi concluído:

1. Issue #7: Implementação de dashboards funccionais para aluno e professor.
2. Issue #8: Desenvolvimento da funcionalidade de correção automática de provas e relatórios mais detalhados.
3. Issue #9: Implementação de diferentes tipos de questão (Múltipla ecolha e Verdadeiro ou Falso).
4. Issue #10: Criação de um design limpo e responsivo para o site.
5. Issue #11: Adição de testes automatizados para garantir a qualidade do código.
6. Issue #12: Refatoração do código para melhor organização e legibilidade.

Também conseguimos garantir a implementação das user stories descritas no arquivo UserStory.md.

## O que voltou para o backlog:

N/A

## Estado atual do projeto:

O projeto já é funcional e atende a todos os requisitos descritos no documento "Doc. de Especificação". Além disso, mudanças no sesign do site garantem uma experiência mais intuitiva e agradável para o usuário. As funções implementadas são:

- RA.01 - O sistema deve fornecer meios para autenticação de usuários com perfis de Professores e Estudantes.
- RP.01 - Cadastrar questões do tipo múltipla escolha.
- RP.02 - Cadastrar questões do tipo verdadeiro ou falso.
- RP.03 - Cadastrar questões com resposta do tipo valor numérico.
- RP.04 - Cadastrar um exame contendo um número arbitrário de questões.
- RP.06 - Atribuir um valor a cada questão presente no exame. Este valor deve ser considerado ao atribuir a nota a nota do aluno.
- RP.07 - A qualquer momento deve possibilitar a visualização de um relatório com as respostas dos estudantes a um exame.
- RP.08 - A qualquer momento deve possibilitar a visualização de um relatório com as nota obtida por cada estudante que respondeu a um dado exame.
- RE.01 - Realizar um exame, respondendo as questões definidas para este exame e concluindo ao final. Um exame concluído não pode ser editado.
- RE.02 - Visualizar a nota de um exame executado após este ser encerrado.
- RE.03 - Para um exame realizado e já encerrado, visualizar as questões acertada e erradas.
- RE.04 - Listar e visualizar dados de exames.
- RE.06 - Um exame em realização deve ser automaticamente concluído no momento de encerramento. Não permitindo a edição da resposta pelos estudantes.
- RG.01 - O sistema deve fornecer uma interface amigável e intuitiva para facilitar a interação dos usuários.
- RG.02 - O sistema deve ser responsivo, ou seja, adaptar-se a diferentes dispositivos (como computadores, tablets e smartphones) para oferecer uma experiência consistente.
- RG.03 - O sistema deve ser capaz de armazenar e recuperar dados de forma confiável, garantindo a integridade das informações. Deve ser utilizado um banco de dados.
- RD.01 - Para facilitar os testes, o sistema deve ser possível executar o sistema com SQLLite. O projeto deve incluir dados pre-carregado (seed) com seguintes as seguintes informações:
  usuário: “pedro”, email: “pedro@unb.br”, senha: “asdfg”, perfil: professor
  usuário: “ester”, email: “ester@unb.br” senha: “asdfg”, perfil: estudante
  algumas questões
  alguns exames em abertos e não respondidos pela ester
  alguns exames em abertos e já respondidos pela ester
  alguns exame agendados
  alguns exames encerrados, e já respondidos pela ester
  alguns exames encerrados, e não respondidos pela ester
- RQ.01 - O sistema deve seguir a arquitetura MVC
- RQ.02 - O sistema deve seguir a terminologia descrita nessa especificação quando aplicável, tanto na interface do usuário quanto no código do projeto.
- RQ.03 - O sistema deve seguir princípios DRY quanto aos templates (camada view)
- RQ.04 - O sistema deve seguir princípios DRY quanto aos controladores. Rotas devem seguir o padrão restful.
- RQ.05 - O sistema deve seguir princípios DRY quanto aos modelos.

## O que será desenvolvido na próxima iteração:

Na próxima iteração, pretendemos realizar as seguintes tarefas:

- Adição de verificação de data e hora para exames agendados
- Melhorias finais de design da aplicação
- Correção de bugs e melhorias.

As tarefas relacionadas à data podem ser encontradas no documento "Doc. de Especificação" seções RP.05, RE.05

## Sprint Review:

O que foi bem =)

- Todos os requisitos principais foram antendidos e o projeto pôde ser entregue dentro do prazo.
- Houve uma melhor comunicação entre os membros da equipe.
- O design foi facilitado devido ao uso da biblioteca Boostrap.
- Todas as funcionalidades estão devidamente testatas

O que foi mal =(

- Ainda há pequenos bugs que precisam ser corrigidos e serão sanados na próxima iteração.
- Embora haja melhorado, há falhas de comunicação que prejudicaram o andamento do projeto.

## Pontos a melhorar:

- Melhor organização da equipe com os quadros Kanban.
- Melhorar a comunicação entre a equipe para evitar atrasos e garantir um fluxo de trabalho mais eficiente.
- Implementar a metodologia Scrum à risca para garantir uma entrega mais eficiente.
