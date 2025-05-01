# MongoDB Study Environment

## Bancos NoSQL

Bancos de dados **NoSQL** (Not Only SQL) surgiram para atender às demandas de aplicações modernas que exigem alta escalabilidade, flexibilidade de esquema e desempenho em grandes volumes de dados. Diferentemente dos bancos relacionais (SQL), que utilizam tabelas rígidas e esquemas predefinidos, os bancos NoSQL oferecem modelos de dados variados, como documentos, chave-valor, colunas ou grafos, permitindo estruturas dinâmicas e adaptáveis.

Os principais benefícios do NoSQL incluem:
- **Flexibilidade**: Suporte a dados heterogêneos sem esquemas fixos.
- **Escalabilidade**: Facilidade de distribuição em clusters para lidar com grandes cargas.
- **Desempenho**: Otimizado para operações específicas, como leitura ou escrita intensiva.
- **Adequação a Casos de Uso**: Ideal para aplicações web, IoT, big data, e cenários com dados não estruturados.

Entre os tipos de bancos NoSQL, o modelo de **documentos** é amplamente adotado por sua simplicidade e capacidade de armazenar dados em formatos semelhantes a JSON ou BSON, facilitando a integração com aplicações modernas.

## MongoDB: Um Banco de Dados de Documentos

O **MongoDB** é um banco de dados NoSQL de código aberto baseado em documentos, projetado para armazenar, consultar e gerenciar dados em coleções de documentos BSON (Binary JSON). Cada documento é um objeto autônomo, semelhante a um JSON, que pode conter campos variados, permitindo esquemas dinâmicos. Suas principais características incluem:
- **Modelo de Documentos**: Dados organizados em coleções (análogas a tabelas) e documentos (análogas a linhas), mas com flexibilidade de estrutura.
- **Consultas Poderosas**: Suporte a consultas ricas, agregações, índices e operações CRUD (Create, Read, Update, Delete).
- **Escalabilidade Horizontal**: Fácil distribuição de dados em clusters com sharding e replicação.
- **Integração Simples**: Compatibilidade com linguagens modernas via drivers oficiais.
- **Ferramentas**: Inclui o shell `mongosh`, o utilitário `mongoimport`, e interfaces gráficas como o MongoDB Compass.

O MongoDB é amplamente utilizado em aplicações que requerem flexibilidade, como e-commerce, redes sociais, e análises de dados em tempo real.

## Objetivo do Repositório

Este repositório tem como objetivo criar um **ambiente de estudos** para aprendizado e prática com o MongoDB, utilizando **Docker** para configuração do banco de dados e um **Makefile** para automação de tarefas. O ambiente é projetado para ser simples, portátil e eficiente, permitindo que desenvolvedores iniciantes e experientes explorem as funcionalidades do MongoDB sem complicações.

### Componentes do Ambiente
- **Docker Compose**: Define um serviço MongoDB (imagem `mongo:7.0`) com um banco de dados chamado `testdb`, configurado com usuário `admin` e senha `admin123`. O Compose mapeia volumes para persistência (`mongo_data`) e importação de dados (`./dados`).
- **Makefile**: Automatiza tarefas comuns, como iniciar/parar o container, acessar o shell `mongosh`, importar arquivos JSON, e visualizar logs, reduzindo a necessidade de comandos manuais longos.
- **Banco de Dados `testdb`**: Criado automaticamente pelo MongoDB durante a inicialização, serve como espaço para criar coleções de teste, como a coleção `series`, usada para praticar operações CRUD.
- **Arquivo de Dados**: O diretório `./dados` contém arquivos JSON (ex.: `series.json`) que podem ser importados para a coleção `series` no banco `testdb`, fornecendo dados reais para exercícios.

O repositório é ideal para:
- Aprender operações CRUD no MongoDB.
- Explorar consultas, índices, e agregações.
- Testar importação de dados JSON.
- Usar ferramentas como `mongosh` e MongoDB Compass em um ambiente controlado.

## Estrutura do Repositório
- **`docker-compose.yml`**: Configura o serviço MongoDB com persistência, autenticação, e mapeamento de portas.
- **`Makefile`**: Contém comandos para gerenciar o ambiente (ex.: `make up`, `make mongo-shell`, `make import-json FILE=series.json`).
- **`dados/`**: Diretório para arquivos JSON (ex.: `series.json`) a serem importados.
- **`series_collection.md`**: Documento com exercícios práticos de CRUD, usando a coleção `series` no banco `testdb`.

## Pré-requisitos
- **Docker** e **Docker Compose** instalados.
- **Make** instalado (para usar o Makefile).
- Diretório `./dados` criado no mesmo nível do `docker-compose.yml`, contendo `series.json` ou outros arquivos JSON para importação.

## Configuração e Uso
1. **Clone o Repositório**:
   ```bash
   git clone https://github.com/esscova/testdrive.git
   cd testdrive/mongoDB
   ```

2. **Crie o Diretório de Dados**:
   ```bash
   mkdir dados
   ```
   - Coloque o arquivo `series.json` (ou outros JSONs) em `./dados`.

3. **Inicie o Ambiente**:
   ```bash
   make up
   ```
   - Isso inicia o container MongoDB com o banco `testdb`.

4. **Importe Dados**:
   ```bash
   make import-json FILE=series.json
   ```
   - Importa `series.json` para a coleção `series` no banco `testdb`.

5. **Acesse o Shell do MongoDB**:
   ```bash
   make mongo-shell
   ```
   - Abre o `mongosh` para executar comandos no banco `testdb`.

6. **Pratique CRUD**:
   - Consulte o arquivo [series_collection.md](./series_collection.md) para exercícios práticos de CRUD na coleção `series`.

7. **Visualize Logs** (se necessário):
   ```bash
   make logs
   ```

8. **Pare o Ambiente**:
   - Para parar sem remover dados:
     ```bash
     make down
     ```
   - Para limpar tudo, incluindo o volume `mongo_data`:
     ```bash
     make down-v
     ```

## Banco de Dados `testdb`
O banco `testdb` é criado automaticamente pelo MongoDB, configurado via a variável `MONGO_INITDB_DATABASE` no `docker-compose.yml`. Ele serve como um espaço para experimentação, onde você pode:
- Criar coleções (ex.: `series`) para testes.
- Importar dados de arquivos JSON do diretório `./dados`.
- Executar operações CRUD, consultas, e agregações.
- Testar índices e outras funcionalidades do MongoDB.

A coleção `series`, gerada a partir de `series.json`, é usada como base para os exercícios em [series_collection.md](./series_collection.md), mas você pode criar outras coleções importando diferentes arquivos JSON.

## Conexão com MongoDB Compass
Para visualizar e manipular os dados graficamente, conecte-se ao MongoDB Compass usando:
```
mongodb://admin:admin123@localhost:27017/testdb?authSource=admin
```

## Comandos Úteis do Makefile
- `make up`: Inicia o container MongoDB.
- `make down`: Para o container, preservando dados.
- `make down-v`: Para o container e remove o volume `mongo_data`.
- `make mongo-shell`: Acessa o shell `mongosh` no banco `testdb`.
- `make import-json FILE=<nome>.json`: Importa um arquivo JSON para uma coleção.
- `make logs`: Exibe os logs do container.
- `make help`: Lista todos os comandos disponíveis.

## Exercícios de Estudo
Para praticar operações CRUD e explorar o MongoDB, consulte o arquivo [series_collection.md](./series_collection.md). Ele contém exercícios detalhados usando a coleção `series`, cobrindo:
- Criação de documentos (`insertOne`, `insertMany`).
- Consultas (`find`, filtros, projeções, ordenação).
- Atualizações (`updateOne`, `updateMany`).
- Exclusões (`deleteOne`, `deleteMany`).
- Operações avançadas, como agregações e índices.

