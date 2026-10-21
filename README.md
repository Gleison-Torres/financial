# Financial

Sistema de gerenciamento financeiro pessoal desenvolvido com **Python, Django e PostgreSQL**.

O Financial permite que usuários gerenciem suas despesas de forma individual, incluindo compras à vista e parceladas, acompanhamento mensal de gastos e controle de pagamentos.

O projeto utiliza uma arquitetura organizada em aplicações Django, com separação de regras de negócio em serviços e testes automatizados.

## Status do projeto

🚧 **Em desenvolvimento**

O sistema já possui funcionalidades essenciais para o gerenciamento de despesas pessoais. Novas melhorias na interface e funcionalidades financeiras estão previstas.

## Tecnologias

- Python
- Django
- PostgreSQL
- HTML5
- CSS3
- JavaScript
- Pytest
- Pytest-Django
- Pytest-Cov
- Git / GitHub

## Funcionalidades

### ✅ Implementadas

#### Autenticação

- Cadastro de usuários
- Ativação de conta por e-mail
- Login por usuário ou e-mail
- Logout seguro via POST
- Recuperação de senha por e-mail
- Redefinição de senha com token

#### Perfil do usuário

- Edição dos dados do perfil
- Alteração de senha
- Alteração de e-mail com confirmação

#### Gerenciamento de despesas

- Cadastro de despesas
- Edição de despesas simples e parceladas
- Exclusão de despesas simples e parceladas
- Cadastro de compras parceladas
- Parcelamento com ou sem juros
- Geração automática das parcelas
- Organização das despesas por usuário
- Visualização das despesas por mês
- Navegação entre meses
- Identificação de despesas parceladas
- Cálculo do total de despesas pendentes do mês
- Acompanhamento do valor total e restante de compras parceladas

#### Controle de pagamentos

- Marcação de despesas como pagas
- Reversão do status para pendente
- Controle individual do pagamento de parcelas
- Atualização dos valores pendentes conforme os pagamentos
- Preservação do status de pagamento ao editar compras parceladas

#### Interface

- Layout responsivo
- Navbar e Footer
- Página de cadastro de usuário
- Página de login
- Página inicial
- Página "Esqueci minha senha"
- Página "Minhas despesas"
- Página "Nova despesa"
- Página "Meu perfil"
- Interface para edição e exclusão de despesas
- Controles para atualização do status de pagamento

#### Testes

- Testes automatizados com Pytest e Pytest-Django
- Testes de autenticação e perfil
- Testes dos serviços de despesas
- Testes das views de despesas
- Testes de controle de pagamentos
- Validação do isolamento de dados entre usuários
- **201 testes aprovados na última execução**
- **100% de cobertura de código no aplicativo `expenses`**, medida com Pytest-Cov

## 🚧 Em desenvolvimento / Planejado

- Desenvolvimento e aprimoramento da Home
- Gerenciamento de categorias
- Dashboard financeiro com gráficos e indicadores
- Melhorias na experiência do usuário

## Qualidade e organização do projeto

O desenvolvimento do Financial utiliza práticas como:

- Separação das regras de negócio em serviços
- Testes automatizados
- Uso de transações atômicas em operações financeiras
- Controle de versão com Git
- Organização das funcionalidades por GitHub Issues
- Desenvolvimento em branches específicas
- Revisão e integração de código por Pull Requests
- Padronização de mensagens com Conventional Commits

## Objetivo

O Financial está sendo desenvolvido como projeto de portfólio para aplicar conceitos de desenvolvimento **Backend com Python e Django**, persistência de dados com PostgreSQL, testes automatizados, organização de regras de negócio e boas práticas de desenvolvimento de software.

O objetivo é evoluir o projeto até uma primeira versão estável de um sistema de gerenciamento financeiro pessoal.

## Autor

**Gleison Torres**