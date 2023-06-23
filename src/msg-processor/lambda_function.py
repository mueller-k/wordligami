import logging
import os
import boto3

from groupy.client import Client

logger = logging.getLogger()
logger.setLevel(logging.INFO)

groupme_token_secret_arn = os.environ.get("GROUPME_TOKEN_SECRET_ARN")


def handler(event, context) -> None:
    logger.info("Processing event...")
    process_event(event)
    logger.info("Event processed.")
    return None


def process_event(event: dict) -> bool:
    # write code here
    groupme_token = get_secret(groupme_token_secret_arn)
    groupme_client = Client.from_token(groupme_token)
    groupme_client.groups.list()
    return True


def process_board(board: str) -> None:
    return None


def get_secret(secret_id: str) -> str:
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager")

    get_secret_value_response = client.get_secret_value(SecretId=secret_id)
    return get_secret_value_response["SecretString"]
