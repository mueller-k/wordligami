import json
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
    groupme_token = get_groupme_token()
    groupme_client = Client.from_token(groupme_token)
    groups = groupme_client.groups.list()
    for group in groups.autopage():
        logger.info(group)
    return True


def process_board(board: str) -> None:
    return None


def get_groupme_token() -> str:
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager")
    get_secret_value_response = client.get_secret_value(SecretId=groupme_token_secret_arn)

    groupme_token_secret = get_secret_value_response["SecretString"]
    groupme_token_secret_object = json.loads(groupme_token_secret)
    return groupme_token_secret_object.get("token", "")
