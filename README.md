# flask-daily-diet-api

Repositório criado para armazenar o código da API de controle de alimentação diário de uma dieta.

Desenvolvido utilizando o framework Flask com utilização de banco de dados PostgreSQL em container.

Contem arquivo api_collection.json para importação em aplicações como postman, insomnia, etc.

## Inicialização do banco (temporário)
Executar o seguinte comando no terminal:
```
docker compose up -d
```

Iniciar o serviço e após isos, executar seguinte comando no terminal:
```
flask shell
```

Após a abertura do shell, executar os seguintes comandos:
```
db.create_all()
db.session.commit()
exit()
```
