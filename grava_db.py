import json
import boto3
import os
import logging
from decimal import Decimal

# Configurar o logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Configurar o endpoint dinamicamente
dynamodb_endpoint = os.getenv('DYNAMODB_ENDPOINT', None)
dynamodb = boto3.resource('dynamodb', endpoint_url=dynamodb_endpoint)

# Conectar à tabela DynamoDB
table = dynamodb.Table('NotasFiscais')

def lambda_handler(event, context):
    logger.info(f"Evento recebido: {json.dumps(event)}")

    # Verificar se é uma consulta (GET)
    if event.get("httpMethod") == "GET":
        return consultar_registros(event)

    # Inserção de registros (POST)
    if event.get("httpMethod") == "POST":
        return inserir_registros(event)

    return {
        'statusCode': 400,
        'body': json.dumps('Erro: Método HTTP não suportado.')
    }

# --- Funções Auxiliares ---

def consultar_registros(event):
    try:
        # Realizar a consulta no DynamoDB
        response = table.scan() # Aqui você pode ajustar a consulta, se necessário
        logger.info(f"Consulta realizada com sucesso. Total de registros: {response['Count']}")

        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'], default=str)
        }
    except Exception as e:
        logger.error(f"Erro ao consultar registros no DynamoDB: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Erro ao consultar registros.')
        }


def inserir_registros(event):
    try:
        # O body vem do API Gateway
        body = json.loads(event['body'])
        logger.info(f"Processando inserção de registro: {body}")

        # Validação básica do registro
        if not all(key in body for key in ["id", "cliente", "valor", "data_emissao"]):
            return {
                'statusCode': 400,
                'body': json.dumps('Erro: Campos obrigatórios faltando.')
            }

        # Inserir o registro no DynamoDB
        # Converte 'valor' para Decimal, que é o tipo nativo do DynamoDB para números
        body['valor'] = Decimal(str(body['valor']))
        table.put_item(Item=body)

        return {
            'statusCode': 200,
            'body': json.dumps('Registro inserido com sucesso!')
        }

    except Exception as e:
        logger.error(f"Erro ao inserir registro no DynamoDB: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Erro ao inserir registro.')
        }