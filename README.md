# Projeto de Disciplina: Redes de Computadores
# *Monitorador de Recursos de Sistema*

## Do quê se trata?

Trata-se de uma aplicação que, por meio de um servidor intermediário, permite com que haja o compartilhamento de recursos de um computador cadastrado na aplicação e, também, visualização dos dados compartilhados por algum computador "on-line".

## Como rodar?

### Linux 🐧:

#### 1. Instalar python (se não já tiver instalado):
```
sudo apt update
sudo apt install python3 python3-pip
```

#### 2. Instalar os requisitos do projeto (bibliotecas Python):
```
pip3 install -r requirements.txt
```

#### 3. Instalar os requisitos adicionais:
```
sudo apt install curl git unzip xz-utils zip libglu1-mesa
```

#### 4. Rodar o projeto:
```
python3 client.py
```
### Windows 🪟:

#### 1. Instalar python (se não já tiver instalado):
Instalador Python do [Site Oficial](https://www.python.org/downloads/).

#### 2. Instalar os requisitos do projeto (bibliotecas Python):
```
pip3 install -r requirements.txt
```

#### 3. Instalar os requisitos adicionais:
```
choco install git
```

#### 4. Rodar o projeto:
```
python3 client.py
```

## Como utilizar?

- Na primeira janela, entrar o IP do servidor
- Escolher o tipo de usuário que será
- Caso seja o usuário compartilhador, precisa inserir um nome de usuário nome
- Caso seja o usuário visualizador, precisa inserir o nome do usuário que quer visualizar os dados

