# Collection Series
## Exercícios Práticos de CRUD com MongoDB

Este documento apresenta uma série de exercícios práticos para dominar as operações **CRUD** (Create, Read, Update, Delete) no MongoDB, utilizando o banco de dados `testdb` e a coleção `series` configurados neste projeto. A coleção `series` contém documentos importados do arquivo `series.json`, com informações sobre séries como título, ano de lançamento, temporadas, gêneros, entre outros.

**Objetivo**: Praticar operações básicas e intermediárias no MongoDB, aprendendo a manipular dados de forma eficiente e explorar recursos como filtros, projeções, ordenação, e índices.

**Pré-requisitos**:
- **Ambiente Configurado**:
  - Docker e Docker Compose instalados.
  - Container MongoDB rodando (`mongo:7.0`, configurado via `docker-compose.yml`).
  - Arquivo `series.json` no diretório `./dados`.
- **Comandos Iniciais**:
  - Inicie o ambiente:
    ```bash
    make up
    ```
  - Importe o arquivo `series.json` para criar a coleção `series` no banco `testdb`:
    ```bash
    make import-json FILE=series.json
    ```
    Isso executa:
    ```bash
    docker exec mongodb mongoimport --uri "mongodb://admin:admin123@localhost:27017/testdb?authSource=admin" --collection series --file /dados/series.json --jsonArray
    ```
- **Acesse o Shell**:
  - Abra o terminal e execute:
    ```bash
    make mongo-shell
    ```
    O prompt mudará para `testdb>`. Todos os comandos a seguir devem ser executados neste shell (`mongosh`).

**Validação Inicial**:
- Confirme que a coleção `series` foi criada:
  ```javascript
  use testdb
  db.series.find()
  ```
  - Deve retornar 8 documentos (como `Stranger Things`, `The Witcher`, etc.).
- Verifique o total de documentos:
  ```javascript
  db.series.countDocuments()
  ```
  - Esperado: `8`.

**Dica**: Use o MongoDB Compass para visualizar os dados graficamente, conectando-se com:
```
mongodb://admin:admin123@localhost:27017/testdb?authSource=admin
```

---

## CREATE (Criar Documentos)

### `insertOne()`
Adicione um único documento à coleção.

1. **Adicionar uma nova série**
   - **Descrição**: Insira um documento para a série "Arcane".
   - **Comando**:
     ```javascript
     db.series.insertOne({
       titulo: "Arcane",
       anoLancamento: 2021,
       temporadas: 1,
       finalizada: false,
       generos: ["Animação", "Ação", "Aventura", "Fantasia", "Sci-Fi"],
       criadores: ["Christian Linke", "Alex Yee"],
       sinopse: "Uma história animada no universo de League of Legends, explorando as cidades de Piltover e Zaun.",
       plataforma: "Netflix",
       avaliacaoIMDB: 9.0,
       baseadoEm: "League of Legends"
     })
     ```
   - **Validação**:
     ```javascript
     db.series.findOne({ titulo: "Arcane" })
     ```
     - Deve retornar o documento inserido com um `_id` gerado.
   - **Aprendizado**: Entenda como o MongoDB gera automaticamente o campo `_id` (ObjectId) e como `insertOne` retorna o `_id` do documento criado.

2. **Adicionar uma série com menos campos**
   - **Descrição**: Insira uma série minimalista para testar documentos heterogêneos.
   - **Comando**:
     ```javascript
     db.series.insertOne({
       titulo: "The Crown",
       anoLancamento: 2016,
       plataforma: "Netflix"
     })
     ```
   - **Validação**:
     ```javascript
     db.series.findOne({ titulo: "The Crown" })
     ```
     - Verifique que apenas os campos especificados aparecem.
   - **Aprendizado**: Explore a flexibilidade do esquema do MongoDB, que permite documentos com estruturas diferentes na mesma coleção.

### `insertMany()`
Adicione múltiplos documentos de uma vez.

3. **Adicionar múltiplas séries**
   - **Descrição**: Insira documentos para "The Boys" e "Succession".
   - **Comando**:
     ```javascript
     db.series.insertMany([
       {
         titulo: "The Boys",
         anoLancamento: 2019,
         temporadas: 4,
         finalizada: false,
         generos: ["Ação", "Comédia", "Crime", "Drama", "Sci-Fi"],
         criadores: ["Eric Kripke"],
         sinopse: "Um grupo de vigilantes enfrenta super-heróis corruptos em um mundo onde o poder corrompe.",
         plataforma: "Amazon Prime Video",
         avaliacaoIMDB: 8.7
       },
       {
         titulo: "Succession",
         anoLancamento: 2018,
         temporadas: 4,
         finalizada: true,
         generos: ["Drama", "Comédia"],
         criadores: ["Jesse Armstrong"],
         sinopse: "A família Roy luta pelo controle de um império midiático em meio a intrigas e traições.",
         plataforma: "HBO",
         avaliacaoIMDB: 8.9
       }
     ])
     ```
   - **Validação**:
     ```javascript
     db.series.find({ titulo: { $in: ["The Boys", "Succession"] } })
     db.series.countDocuments()
     ```
     - Deve retornar os dois documentos e um total de `11` documentos (8 iniciais + 3 inserções).
   - **Aprendizado**: Compare `insertOne` e `insertMany`, e entenda como `insertMany` lida com erros (como duplicatas).

---

## READ (Ler/Consultar Documentos)

### `find()` (Básico e Filtros)
Consulte documentos usando diferentes critérios.

4. **Listar todas as séries**
   - **Descrição**: Exiba todos os documentos da coleção.
   - **Comando**:
     ```javascript
     db.series.find()
     ```
   - **Validação**:
     ```javascript
     db.series.countDocuments()
     ```
     - Esperado: `11` (após as inserções).
   - **Aprendizado**: Use `pretty()` para formatação legível.

5. **Encontrar séries da HBO**
   - **Descrição**: Busque séries cuja plataforma seja "HBO".
   - **Comando**:
     ```javascript
     db.series.find({ plataforma: "HBO" })
     ```
   - **Validação**:
     ```javascript
     db.series.countDocuments({ plataforma: "HBO" })
     ```
     - Esperado: Pelo menos `2` (`Game of Thrones`, `Succession`).
   - **Aprendizado**: Pratique consultas simples com igualdade.

6. **Encontrar séries finalizadas**
   - **Descrição**: Busque séries onde `finalizada` seja `true`.
   - **Comando**:
     ```javascript
     db.series.find({ finalizada: true })
     ```
   - **Validação**:
     ```javascript
     db.series.countDocuments({ finalizada: true })
     ```
     - Esperado: Pelo menos `4` (`Breaking Bad`, `Fleabag`, `Game of Thrones`, `Succession`).
   - **Aprendizado**: Trabalhe com campos booleanos.

7. **Encontrar séries com avaliação IMDB maior ou igual a 9.0**
   - **Descrição**: Liste séries com alta avaliação.
   - **Comando**:
     ```javascript
     db.series.find({ avaliacaoIMDB: { $gte: 9.0 } })
     ```
   - **Validação**:
     ```javascript
     db.series.countDocuments({ avaliacaoIMDB: { $gte: 9.0 } })
     ```
     - Esperado: Pelo menos `2` (`Breaking Bad`, `Arcane`).
   - **Aprendizado**: Use operadores de comparação (`$gte`, `$gt`, `$lte`, `$lt`).

8. **Encontrar séries de "Comédia" OU "Aventura"**
   - **Descrição**: Use o operador `$or` para buscar séries com gêneros específicos.
   - **Comando**:
     ```javascript
     db.series.find({ $or: [ { generos: "Comédia" }, { generos: "Aventura" } ] })
     ```
   - **Validação**:
     ```javascript
     db.series.countDocuments({ $or: [ { generos: "Comédia" }, { generos: "Aventura" } ] })
     ```
     - Esperado: Pelo menos `5` (como `Fleabag`, `Ted Lasso`, `The Witcher`, `The Mandalorian`, `Succession`).
   - **Aprendizado**: Explore operadores lógicos (`$or`, `$and`).

9. **Encontrar séries que SÃO de "Drama" E lançadas APÓS 2018**
   - **Descrição**: Combine condições com AND implícito.
   - **Comando**:
     ```javascript
     db.series.find({ generos: "Drama", anoLancamento: { $gt: 2018 } })
     ```
   - **Validation**:
     ```javascript
     db.series.countDocuments({ generos: "Drama", anoLancamento: { $gt: 2018 } })
     ```
     - Esperado: Pelo menos `2` (`The Witcher`, `Succession`).
   - **Aprendizado**: Entenda o AND implícito em objetos de consulta.

10. **Buscar séries com sinopse específica**
    - **Descrição**: Encontre séries cuja sinopse contenha a palavra "misterioso" (case-insensitive).
    - **Comando**:
      ```javascript
      db.series.find({ sinopse: { $regex: "misterioso", $options: "i" } })
      ```
    - **Validação**:
      ```javascript
      db.series.countDocuments({ sinopse: { $regex: "misterioso", $options: "i" } })
      ```
      - Esperado: Pelo menos `1` (`Stranger Things`).
    - **Aprendizado**: Use `$regex` para buscas baseadas em padrões.

### `find()` (Projeção, Ordenação, Limite)
Controle a saída das consultas.

11. **Listar apenas títulos e anos de lançamento**
    - **Descrição**: Mostre apenas `titulo` e `anoLancamento`, excluindo `_id`.
    - **Comando**:
      ```javascript
      db.series.find({}, { titulo: 1, anoLancamento: 1, _id: 0 })
      ```
    - **Validação**:
      - Deve retornar todos os documentos com apenas os campos especificados.
    - **Aprendizado**: Use projeção para limitar campos retornados (`1` para incluir, `0` para excluir).

12. **Listar todas as séries ordenadas por título (A-Z)**
    - **Descrição**: Ordene alfabeticamente por `titulo`.
    - **Comando**:
      ```javascript
      db.series.find().sort({ titulo: 1 })
      ```
    - **Validação**:
      - Verifique se os títulos estão em ordem alfabética (ex.: `Arcane`, `Breaking Bad`, etc.).
    - **Aprendizado**: Use `sort` (`1` para ascendente, `-1` para descendente).

13. **Listar as 3 séries com maior avaliação IMDB**
    - **Descrição**: Ordene por `avaliacaoIMDB` descendente e limite a 3 resultados.
    - **Comando**:
      ```javascript
      db.series.find().sort({ avaliacaoIMDB: -1 }).limit(3)
      ```
    - **Validação**:
      ```javascript
      db.series.find().sort({ avaliacaoIMDB: -1 }).limit(3).count()
      ```
      - Esperado: `3` (como `Breaking Bad`, `Game of Thrones`, `Arcane`).
    - **Aprendizado**: Combine `sort` e `limit` para consultas paginadas.

14. **Listar séries que NÃO são da Netflix, mostrando apenas título e plataforma**
    - **Descrição**: Use `$ne` para excluir a Netflix e projeção para campos específicos.
    - **Comando**:
      ```javascript
      db.series.find({ plataforma: { $ne: "Netflix" } }, { titulo: 1, plataforma: 1, _id: 0 })
      ```
    - **Validation**:
      ```javascript
      db.series.countDocuments({ plataforma: { $ne: "Netflix" } })
      ```
      - Esperado: Pelo menos `7` (excluindo `Stranger Things`, `The Witcher`, `Arcane`, `The Crown`).
    - **Aprendizado**: Combine `$ne` com projeção.

---

## UPDATE (Atualizar Documentos)

### `updateOne()`
Atualize um único documento.

15. **Corrigir/Atualizar temporadas de "The Mandalorian"**
    - **Descrição**: Atualize o campo `temporadas` para 4 (supondo uma nova temporada).
    - **Comando**:
      ```javascript
      db.series.updateOne(
        { titulo: "The Mandalorian" },
        { $set: { temporadas: 4 } }
      )
      ```
    - **Validação**:
      ```javascript
      db.series.findOne({ titulo: "The Mandalorian" })
      ```
      - Deve mostrar `temporadas: 4`.
    - **Aprendizado**: Use `$set` para atualizar campos específicos.

16. **Adicionar "Dark Comedy" aos gêneros de "Fleabag"**
    - **Descrição**: Use `$addToSet` para evitar duplicatas.
    - **Comando**:
      ```javascript
      db.series.updateOne(
        { titulo: "Fleabag" },
        { $addToSet: { generos: "Dark Comedy" } }
      )
      ```
    - **Validação**:
      ```javascript
      db.series.findOne({ titulo: "Fleabag" })
      ```
      - O campo `generos` deve incluir "Dark Comedy".
    - **Aprendizado**: Use `$addToSet` para manipular arrays.

17. **Incrementar a avaliação de "Severance" em 0.1**
    - **Descrição**: Aumente `avaliacaoIMDB` com `$inc`.
    - **Comando**:
      ```javascript
      db.series.updateOne(
        { titulo: "Severance" },
        { $inc: { avaliacaoIMDB: 0.1 } }
      )
      ```
    - **Validação**:
      ```javascript
      db.series.findOne({ titulo: "Severance" })
      ```
      - Deve mostrar `avaliacaoIMDB: 8.8`.
    - **Aprendizado**: Use `$inc` para operações aritméticas.

18. **Adicionar sinopse a "Game of Thrones"**
    - **Descrição**: Inclua uma sinopse para a série.
    - **Comando**:
      ```javascript
      db.series.updateOne(
        { titulo: "Game of Thrones" },
        { $set: { sinopse: "Lutas pelo trono de Westeros em um mundo de fantasia medieval cheio de intrigas políticas." } }
      )
      ```
    - **Validação**:
      ```javascript
      db.series.findOne({ titulo: "Game of Thrones" })
      ```
      - Deve mostrar o campo `sinopse`.
    - **Aprendizado**: Combine `$set` com campos novos.

### `updateMany()`
Atualize múltiplos documentos.

19. **Adicionar campo `assistido: false` a todas as séries**
    - **Descrição**: Inclua um campo em todos os documentos.
    - **Comando**:
      ```javascript
      db.series.updateMany(
        {},
        { $set: { assistido: false } }
      )
      ```
    - **Validação**:
      ```javascript
      db.series.find({ assistido: { $exists: true } }).count()
      ```
      - Esperado: Total de documentos na coleção.
    - **Aprendizado**: Use filtro vazio (`{}`) para afetar todos os documentos.

20. **Renomear o campo `criadores` para `showrunners`**
    - **Descrição**: Altere o nome do campo em todos os documentos.
    - **Comando**:
      ```javascript
      db.series.updateMany(
        {},
        { $rename: { "criadores": "showrunners" } }
      )
      ```
    - **Validação**:
      ```javascript
      db.series.find({ showrunners: { $exists: true } })
      db.series.find({ criadores: { $exists: true } }).count()
      ```
      - Esperado: Documentos com `showrunners`, `0` com `criadores`.
    - **Aprendizado**: Use `$rename` para reestruturar documentos.

21. **Incrementar temporadas de séries não finalizadas**
    - **Descrição**: Aumente `temporadas` em 1 para séries com `finalizada: false`.
    - **Comando**:
      ```javascript
      db.series.updateMany(
        { finalizada: false },
        { $inc: { temporadas: 1 } }
      )
      ```
    - **Validação**:
      ```javascript
      db.series.find({ finalizada: false })
      ```
      - Verifique o aumento em séries como `Stranger Things`, `The Witcher`, etc.
    - **Aprendizado**: Combine filtros com `$inc`.

---

## DELETE (Excluir Documentos)
**Atenção**: Sempre valide o filtro com `find()` antes de executar comandos de exclusão para evitar remover documentos indesejados.

### `deleteOne()`
Remova um único documento.

22. **Excluir a série "Arcane"**
    - **Descrição**: Remova a série inserida no exercício 1.
    - **Comando**:
      ```javascript
      // Verificar primeiro
      db.series.find({ titulo: "Arcane" })
      // Executar se correto
      db.series.deleteOne({ titulo: "Arcane" })
      ```
    - **Validação**:
      ```javascript
      db.series.findOne({ titulo: "Arcane" })
      ```
      - Deve retornar `null`.
    - **Aprendizado**: Use `deleteOne` para remoções precisas.

23. **Excluir uma série por plataforma**
    - **Descrição**: Remova a primeira série da "Apple TV+".
    - **Comando**:
      ```javascript
      // Verificar
      db.series.find({ plataforma: "Apple TV+" })
      // Executar
      db.series.deleteOne({ plataforma: "Apple TV+" })
      ```
    - **Validação**:
      ```javascript
      db.series.countDocuments({ plataforma: "Apple TV+" })
      ```
      - Esperado: Reduzido em 1 (ex.: de 2 para 1).
    - **Aprendizado**: Teste `deleteOne` com filtros mais amplos.

### `deleteMany()`
Remova múltiplos documentos.

24. **Excluir séries lançadas antes de 2010**
    - **Descrição**: Remova séries antigas.
    - **Comando**:
      ```javascript
      // Verificar MUITO CUIDADOSAMENTE
      db.series.find({ anoLancamento: { $lt: 2010 } })
      // Executar apenas se tiver certeza
      db.series.deleteMany({ anoLancamento: { $lt: 2010 } })
      ```
    - **Validação**:
      ```javascript
      db.series.countDocuments({ anoLancamento: { $lt: 2010 } })
      ```
      - Deve retornar `0`.
    - **Aprendizado**: Use `deleteMany` com filtros cautelosos.

25. **Excluir séries com baixa avaliação**
    - **Descrição**: Remova séries com `avaliacaoIMDB` menor que 8.5.
    - **Comando**:
      ```javascript
      // Verificar
      db.series.find({ avaliacaoIMDB: { $lt: 8.5 } })
      // Executar
      db.series.deleteMany({ avaliacaoIMDB: { $lt: 8.5 } })
      ```
    - **Validação**:
      ```javascript
      db.series.countDocuments({ avaliacaoIMDB: { $lt: 8.5 } })
      ```
      - Deve retornar `0`.
    - **Aprendizado**: Combine `deleteMany` com operadores de comparação.

---

## Exercícios Avançados
Combine operações CRUD e explore recursos adicionais.

26. **Fluxo CRUD Completo**
    - **Descrição**: Insira uma série, consulte-a, atualize-a, e delete-a.
    - **Comando**:
      ```javascript
      // Create
      db.series.insertOne({
        titulo: "Westworld",
        anoLancamento: 2016,
        temporadas: 4,
        finalizada: true,
        generos: ["Ficção Científica", "Drama", "Mistério"],
        plataforma: "HBO",
        avaliacaoIMDB: 8.5
      });

      // Read
      db.series.find({ titulo: "Westworld" });

      // Update
      db.series.updateOne(
        { titulo: "Westworld" },
        { $set: { sinopse: "Um parque temático futurista onde androides ganham consciência." } }
      );

      // Delete
      db.series.deleteOne({ titulo: "Westworld" });
      ```
    - **Validação**:
      ```javascript
      db.series.findOne({ titulo: "Westworld" })
      db.series.countDocuments()
      ```
      - Após o delete, deve retornar `null` e o total original.
    - **Aprendizado**: Simule um fluxo real de gerenciamento de dados.

27. **Consulta com Agregação**
    - **Descrição**: Calcule a média de `avaliacaoIMDB` por plataforma.
    - **Comando**:
      ```javascript
      db.series.aggregate([
        { $group: { _id: "$plataforma", mediaIMDB: { $avg: "$avaliacaoIMDB" } } },
        { $sort: { mediaIMDB: -1 } }
      ])
      ```
    - **Validação**:
      - Verifique se plataformas como HBO têm médias altas (ex.: devido a `Game of Thrones`, `Succession`).
    - **Aprendizado**: Introdução ao pipeline de agregação com `$group` e `$sort`.

28. **Criar e Testar um Índice**
    - **Descrição**: Crie um índice no campo `titulo` e teste sua eficiência.
    - **Comando**:
      ```javascript
      db.series.createIndex({ titulo: 1 });
      db.series.find({ titulo: "Stranger Things" }).explain("executionStats");
      ```
    - **Validação**:
      - O `explain` deve indicar que a consulta usa o índice (`IXSCAN`).
    - **Aprendizado**: Entenda como índices melhoram a performance de consultas.

---

## Dicas para Prática
- **Use o Compass**: Após cada operação, atualize a visualização no MongoDB Compass para confirmar as mudanças graficamente.
- **Teste Erros**: Tente inserir documentos com campos inválidos (ex.: `avaliacaoIMDB: "invalido"`) para entender mensagens de erro.
- **Automatize com Scripts**:
  - Crie um arquivo `crud.js` em `./dados` com os comandos acima e execute:
    ```bash
    make run-script SCRIPT=crud.js
    ```
    - Adicione ao Makefile:
      ```makefile
      run-script:
      	@if [ -z "$(SCRIPT)" ]; then \
      		echo "Erro: Defina o script com SCRIPT=<nome>. Ex: make run-script SCRIPT=crud.js"; \
      		exit 1; \
      	fi
      	@if ! docker ps -q -f name=$(MONGO_CONTAINER) | grep -q .; then \
      		echo "Erro: O container $(MONGO_CONTAINER) não está rodando. Execute 'make up' primeiro."; \
      		exit 1; \
      	fi
      	docker exec $(MONGO_CONTAINER) mongosh "$(MONGO_URI)" --file /dados/$(SCRIPT)
      ```
- **Explore Mais Operadores**:
  - `$in`, `$nin` para listas.
  - `$exists` para verificar a presença de campos.
  - `$elemMatch` para arrays complexos.
- **Backup dos Dados**:
  - Antes de operações destrutivas, exporte a coleção:
    ```bash
    docker exec mongodb mongoexport --uri "mongodb://admin:admin123@localhost:27017/testdb?authSource=admin" --collection series --out /dados/series_backup.json
    ```

---

## Resolução de Problemas
- **Erro de Autenticação**:
  - Verifique a URI: `mongodb://admin:admin123@localhost:27017/testdb?authSource=admin`.
  - Reinicie o ambiente se necessário:
    ```bash
    make down-v
    make up
    ```
- **Container Não Rodando**:
  - Execute `make up` antes de `make mongo-shell`.
- **Dados Não Aparecem**:
  - Confirme a importação com `make import-json FILE=series.json`.
  - Verifique logs: `make logs`.
- **Comportamento Inesperado**:
  - Use `db.series.find()` após cada operação para inspecionar o estado.

---

