# Atividade 3 - Banco de Dados

## Descrição
Este é um projeto Python que implementa a Atividade 3 de Banco de dados 2, visando aplicar os conhecimentos adquiridos sobre conexão utilizando driver e conexão utilizando ORM.

## Instalação das Dependências

Siga os passos abaixo para configurar seu ambiente de desenvolvimento e instalar as dependências necessárias:

### Passo 1: Clonar o Repositório
Clone o repositório do GitHub para seu ambiente local:
```bash
git clone https://github.com/HellyNapaa/Bd2_trabalho.git
cd Bd2_trabalho
```
### Passo 2: Instalar o Psycoopg2
Instale o driver de conexão para Python e PostgreSQL
```bash
pip install psycopg2_binary
```
### Passo 3: Instalar o SQLAlchemy
Instale a biblioteca de ORM SQLAlchemy
```bash
pip install SQLAlchemy
```
### Passo 4: Instalar o sqlacodegen
Instale a ferramenta de mapeamento de modelos de banco de dados sqlacodegen
```bash
pip install sqlacodegen
```
### Passo 5: Crie os modelos a partir do banco
A partir do seu banco de dados, é possível criar a modelagem do mesmo com a ferramenta a partir do sqlacodegen e da seguinte maneira:
```bash
sqlacodegen postgresql://username:password@localhost:5432/northwind --schema northwind > models.py
```
Este comando faz a conexão com o seu banco a partir do seu usuário e senha, acessa o schema northwind dentro do banco northwind e adiciona a modelagem no arquivo models.py

## Configuração da Aplicação 

A aplicação é dividida em pastas, sendo que a pasta "config" armazena o arquivo "config.py".
Dentro deste arquivo é necessário que cada usuário altere as informações de conexão do banco seguindo o formato:
```bash
DATABASE_URL = "postgresql+psycopg2://username:password@localhost/northwind"

def get_psycopg_connection():
    return psycopg2.connect(
        dbname="northwind",
        user="username",
        password="password",
        host="localhost"
    )
```