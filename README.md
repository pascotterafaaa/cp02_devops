# CP2 DevOps - Steves Jobs e DimDim

Projeto do 2o Checkpoint de DevOps usando MySQL em container Docker e uma aplicacao Python CRUD rodando diretamente no terminal Linux da VM Azure.

RM do representante: `564928`

## Arquitetura

- Banco de dados: container Docker `db_564928`, imagem `mysql:8.0`.
- Segundo container: `adminer_564928`, imagem `adminer:latest`, usado para comprovar interacao entre containers na mesma rede Docker.
- Aplicacao: `app.py`, executada diretamente na VM com `python3 app.py`.
- Rede Docker: `rede_564928`.
- Volume nomeado do banco: `vol_db_564928`.
- Porta do MySQL: `3306`.
- Porta do Adminer: `8080`.

Importante: a aplicacao Python nao usa Dockerfile e nao roda em container. Ela roda no terminal Linux da VM Azure e acessa o MySQL pela porta publicada `3306`.

## Estrutura do projeto

```text
cp02_devops/
├── app.py
├── requirements.txt
├── mysql/
│   └── init.sql
├── scripts/
│   ├── 01_criar_infra_docker.sh
│   ├── 02_preparar_python_azure.sh
│   ├── 03_rodar_app.sh
│   └── 04_evidencias_mysql.sql
└── docs/
    └── roteiro_video.md
```

## Passo 1 - Preparar a VM Azure

Instale somente os pacotes necessarios para o projeto:

```bash
sudo apt install -y docker.io python3 python3-pip git
sudo systemctl enable docker
sudo systemctl start docker
```

Confirme o Docker:

```bash
docker --version
sudo docker ps
```

## Passo 2 - Clonar o repositorio

No seu diretorio HOME:

```bash
cd ~
git clone https://github.com/pascotterafaaa/cp02_devops.git
cd cp02_devops
```

Se voce ainda nao subiu para o GitHub, copie esta pasta `cp02_devops` para o seu repositorio e faca o push.

## Passo 3 - Criar a infraestrutura Docker do banco

Crie a rede:

```bash
sudo docker network create rede_564928
```

Crie o volume nomeado:

```bash
sudo docker volume create vol_db_564928
```

Baixe a imagem publica do MySQL:

```bash
sudo docker pull mysql:8.0
```

Suba o container MySQL:

```bash
sudo docker run \
  --name db_564928 \
  -d \
  --network rede_564928 \
  -e MYSQL_ROOT_PASSWORD=senha_564928 \
  -e MYSQL_DATABASE=dimdim_564928 \
  -e MYSQL_USER=user_564928 \
  -e MYSQL_PASSWORD=senha_564928 \
  -p 3306:3306 \
  -v vol_db_564928:/var/lib/mysql \
  -v "$(pwd)/mysql/init.sql:/docker-entrypoint-initdb.d/init.sql" \
  mysql:8.0
```

Suba o segundo container, Adminer, na mesma rede Docker:

```bash
sudo docker pull adminer:latest

sudo docker run \
  --name adminer_564928 \
  -d \
  --network rede_564928 \
  -e ADMINER_DEFAULT_SERVER=db_564928 \
  -p 8080:8080 \
  adminer:latest
```

Verifique os containers:

```bash
sudo docker ps
sudo docker logs db_564928
```

## Passo 4 - Preparar o ambiente Python

Instale a biblioteca do MySQL para Python:

```bash
python3 -m pip install --user -r requirements.txt
```

Se preferir instalar diretamente:

```bash
python3 -m pip install --user mysql-connector-python
```

## Passo 5 - Configurar variaveis de ambiente

A aplicacao le as configuracoes do banco usando `os.environ`.

```bash
export DB_HOST=127.0.0.1
export DB_PORT=3306
export DB_NAME=dimdim_564928
export DB_USER=root
export DB_PASSWORD=senha_564928
```

## Passo 6 - Executar a aplicacao Python

```bash
python3 app.py
```

Menu da aplicacao:

```text
1 - INSERT: criar transacao
2 - SELECT: listar transacoes
3 - UPDATE: atualizar transacao
4 - DELETE: remover transacao
0 - Sair
```

## Evidencias do CRUD pelo MySQL

Entre no MySQL pelo terminal:

```bash
sudo docker exec -it db_564928 mysql -u root -p
```

Senha:

```text
senha_564928
```

Dentro do MySQL:

```sql
USE dimdim_564928;
SELECT * FROM transacoes;
```

Use sempre o mesmo comando para comprovar as operacoes:

```sql
SELECT * FROM transacoes;
```

Roteiro simples para o video:

1. Faca um INSERT na aplicacao Python e rode `SELECT * FROM transacoes;` no MySQL.
2. Faca um UPDATE na aplicacao Python e rode `SELECT * FROM transacoes;` no MySQL.
3. Faca um DELETE na aplicacao Python e rode `SELECT * FROM transacoes;` no MySQL.
4. Explique que a tabela mostra a linha criada, depois alterada, e depois removida.

## Acesso ao Adminer

Se a porta 8080 estiver liberada na VM Azure, acesse:

```text
http://IP_DA_VM:8080
```

Login:

```text
Sistema: MySQL
Servidor: db_564928
Usuario: root
Senha: senha_564928
Banco: dimdim_564928
```

Esse acesso comprova o segundo container interagindo com o banco pela rede `rede_564928`.


## Limpeza do ambiente

Use apenas se precisar refazer do zero:

```bash
sudo docker rm -f db_564928 adminer_564928
sudo docker volume rm vol_db_564928
sudo docker network rm rede_564928
```
