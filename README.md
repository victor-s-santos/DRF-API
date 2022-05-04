# DRF-API
Construção de uma api simples, utilizando django e django rest framework

## Como rodar

* Através de VirtualEnv
    1. Clone o repositório
        - git clone https://github.com/victor-s-santos/DRF-API.git

    2. Crie sua virtualenv
        - com o terminal na raíz do projeto, rodar python -m venv .venv

    3. Ative sua virtualenv
        - source .venv/bin/activate

    4. Instale as dependências
        - pip install -r requirements.txt

    5. Rode as migrações
        - python manage.py migrate

    6. Execute os testes
        - pytest -v

    7. Suba o servidor
        - python manage.py runserver

__OBS__: É necessário que você possua um banco de dados postgresql executando com as credenciais fornecidas no .env para que haja a conexão correta. No entanto, a chave referente ao banco de dados pode ser substituída pela chave padrão do django, e o sistema usará o sistema sqlite3, sem problemas.


* Utilizando o Docker-Compose
    1. Clone o repositório
        - git clone https://github.com/victor-s-santos/DRF-API.git
    
    2. Construa os containers (e já subir o servidor)
        - docker-compose up --build

    3. Suba o servidor
        - Após a realização do build, é necessário somente rodar: docker-compose up
    
    4. Rodar os testes
        - Com o container em execução, rodar em outro terminal:
            docker exec -it __movies_project_web_1__ pytest -v
        - O nome do container pode ser adquirido executando docker ps