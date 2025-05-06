#
# Exemplo de script de consulta interativa com MongoDB em Python
# Autor: Wellington M Santos
#

# --- Bibliotecas ---
import sys
import json
import logging
from pymongo import MongoClient, errors
from pprint import pprint
import os
from datetime import datetime

# --- Configuração de Logs ---
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_filename = os.path.join(log_dir, f"mongodb_query_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# logger principal
logger = logging.getLogger("mongodb_script")
logger.setLevel(logging.INFO)

# console - INFO e superiores
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(levelname)s: %(message)s')
console_handler.setFormatter(console_format)

# arquivo - ERROR e superiores (serão salvos em arquivo)
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.ERROR)
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_format)

# handlers ao logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# --- Configurações de Conexão ---
MONGO_URI = "mongodb://admin:admin123@localhost:27017/"
DB_NAME = "testdb"
COLLECTION_NAME = "series"
SERVER_TIMEOUT = 3000  # 3 segundos


def connect_to_mongodb(uri, db_name, collection_name):
    """
    Tenta conectar ao MongoDB e retorna o objeto da coleção e o cliente.
    Retorna (None, None) em caso de falha.
    """
    client = None
    collection = None
    try:
        logger.info(f"Tentando conectar ao MongoDB em {uri}...")
        client = MongoClient(
            uri,
            serverSelectionTimeoutMS=SERVER_TIMEOUT 
        )
        client.server_info()
        logger.info("Conexão com MongoDB estabelecida com sucesso!")

        # banco de dados
        db = client[db_name]
        logger.info(f"Banco de dados '{db_name}' selecionado.")

        # coleção
        collection = db[collection_name]
        logger.info(f"Coleção '{collection_name}' selecionada.")
        return client, collection

    except errors.ServerSelectionTimeoutError as err:
        logger.error(f"Erro de Timeout: Não foi possível conectar ao servidor MongoDB em {uri}. Detalhes: {err}")
        if client:
            client.close()
        return None, None
    except errors.ConnectionFailure as err:
        logger.error(f"Erro de Conexão: Falha ao conectar ao MongoDB em {uri}. Verifique se o servidor MongoDB está rodando e acessível. Detalhes: {err}")
        if client:
            client.close()
        return None, None
    except Exception as e:
        logger.error(f"Ocorreu um erro inesperado durante a conexão: {e}", exc_info=True)
        if client:
            client.close()
        return None, None


def query_loop(collection):
    """
    Inicia um loop infinito para receber e executar consultas do usuário.
    """
    print("\n--- Iniciando Loop de Consultas ---")
    print("\nDigite sua consulta MongoDB no formato JSON (ex: {\"finalizada\": true})")
    print("Digite 'quit' ou pressione Ctrl+C para sair.")

    while True:
        try:
            query_str = input("\nConsulta> ")

            if query_str.strip().lower() == 'quit':
                logger.info("Saindo do loop de consultas.")
                break

            if not query_str.strip():  # continua mesmo entrada vazia
                continue

            # str -> dict
            try:
                query_dict = json.loads(query_str)
                if not isinstance(query_dict, dict):
                    logger.warning("A entrada JSON deve ser um objeto (dicionário). Ex: {}")
                    continue
            except json.JSONDecodeError as e:
                logger.warning(f"Formato JSON inválido. Detalhes: {e}")
                print("Exemplo válido: {\"anoLancamento\": {\"$gte\": 2020}}")
                continue

            # find (str -> dict)
            try:
                # logger.info(f"Executando consulta: {query_dict}")
                cursor = collection.find(query_dict)
                results = list(cursor)  # lista para poder contar

                if not results:
                    logger.info("Nenhum documento encontrado para esta consulta.")
                else:
                    print(f"--- {len(results)} Documento(s) Encontrado(s) ---\n")
                    for doc in results:
                        pprint(doc)
                        print("-" * 50)  

            except errors.PyMongoError as mongo_err:
                logger.error(f"Erro durante a execução da consulta MongoDB: {mongo_err}")
                print(f"Erro durante a execução da consulta. Verifique os logs para detalhes.")
            except Exception as e:
                logger.error(f"Erro inesperado durante a execução da consulta: {e}", exc_info=True)
                print(f"Erro inesperado. Verifique os logs para detalhes.")

        except KeyboardInterrupt:
            logger.info("\nSaindo do loop de consultas (Ctrl+C pressionado).")
            break
        except EOFError:  # redireciona CTRL+D para sair
            logger.info("\nFim da entrada detectado. Saindo.")
            break


# --- bloco principal ---

if __name__ == '__main__':
    print("\n=== Script de Consulta Interativa MongoDB ===\n")
    mongo_client = None  

    try:
        # 1. conectar ao banco de dados
        mongo_client, series_collection = connect_to_mongodb(MONGO_URI, DB_NAME, COLLECTION_NAME)

        # 2. conectou?
        if series_collection is not None and mongo_client is not None:
            query_loop(series_collection)
        else:
            logger.error("Não foi possível estabelecer conexão com o MongoDB. O script não pode continuar sem uma conexão ativa.")
            print("\nNão foi possível estabelecer conexão com o MongoDB.")
            print("O script não pode continuar sem uma conexão ativa.")
            sys.exit(1)  # quebra com erro

    except Exception as e:
        logger.critical(f"Ocorreu um erro crítico no script: {e}", exc_info=True)
        print(f"\nOcorreu um erro crítico no script. Verifique os logs para detalhes.")

    finally:
        # 3. forçar fechamento da conexão
        if mongo_client is not None:
            logger.info("Fechando a conexão com o MongoDB...")
            mongo_client.close()
            logger.info("Conexão fechada.")
            print("\nConexão com MongoDB fechada.")
        else:
            logger.info("Nenhuma conexão ativa para fechar.")

    logger.info("=== Script Finalizado ===")
    print("\n=== Script Finalizado ===\n")