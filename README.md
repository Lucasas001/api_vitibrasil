# Passos usado para criar o ambiente desenvolvimento

### Instale pyenv

Siga o passo a passo: https://medium.com/@aashari/easy-to-follow-guide-of-how-to-install-pyenv-on-ubuntu-a3730af8d7f0

### Instale pipx (Instale e execute aplicativos Python em ambientes isolados)

```
sudo apt update
sudo apt install pipx
pipx ensurepath
sudo pipx ensurepath
```

Link ref: https://github.com/pypa/pipx

### Configurando ambiente local de desenvolvimento

```
pyenv update
pyenv install 3.13:latest
```

Link ref: https://github.com/pyenv/pyenv

### Usaremos o poetry com gerenciador de pacotes e dependências para Python

```
pipx install poetry
```

Link ref: https://python-poetry.org/

### Criando projeto no poetry

```
poetry new api_vitibrasil
cd api_vitibrasil
```

### Configurando pyenv

```
pyenv local 3.13.0
```

### Editando pyproject.toml para definir versão do Python

```
[tool.poetry.dependencies]
python = "3.13.*"
```

### Inicializando ambiente virtual com Poetry e adicionando o FastAPI

```
poetry install
poetry add 'fastapi[standard]'
poetry shell # Iniciando ambiente virtual
```

### Iniciando ambiente dev FastAPI

```
fastapi dev fast_zero/app.py
```

### Adicionando ferramentas que usaremos somente no ambiente de desenvolvimento

```
poetry add --group dev pytest pytest-cov taskipy
```

- O Pytest é uma framework de testes, que usaremos para escrever e executar nossos testes.
- A ideia do Taskipy é ser um executor de tarefas (task runner) complementar em nossa aplicação.
- O ignr ajuda a criar o .gitignore

Edite pyproject.toml

```
[tool.pytest.ini_options]
pythonpath = "."
addopts = '-p no:warnings'

[tool.taskipy.tasks]
run = 'fastapi dev api_vitibrasil/app.py'
test = 'pytest -s -x --cov=api_vitibrasil -vv'
post_test = 'coverage html'
```
