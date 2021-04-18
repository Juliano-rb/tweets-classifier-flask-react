# tweets-classifier-flask-react
Classificador de tweets com um serviço flask e frontend em react.js.

Aplicação criada para a disciplina Sistemas Suportados Por Aprendizagem de máquina do curso de Bacharelado em Informática da Universidade Federal de Alagoas.
Para a criação do sistema, foi utilizado como base o repositório https://github.com/intelligentagents/aprendizagem-supervisionada/tree/master/ml-apps/movies-classifier-flask-react que faz a classificação de reviews de filmes.

![Aplicação](./img/app.png)

# Iniciando o projeto:
```bash
docker-compose build && docker-compose up
```

Se você for iniciar a aplicação em um servidor web, você vai precisar criar um arquivo `.env` no mesmo diretório do arquivo `docker-compose.yml` com a URL do serviço (api) que o frontend deve consumir, conforme exemplo abaixo:
```bash
API_URL=your-server-url:5000
```

Dessa forma, o `docker-compose` se responsabiliza de configurar a url do servidor definida ao invés de localhost para a aplicação React.
