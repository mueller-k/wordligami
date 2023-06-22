import logging
import os

from groupy.client import Client

logger = logging.getLogger()
logger.setLevel(logging.INFO)

groupme_token = os.environ.get("GROUPME_TOKEN")
groupme_client = Client.from_token(groupme_token)


def handler(event, context) -> None:
    logger.info("Processing event...")
    process_event(event)
    logger.info("Event processed.")
    return None


def process_event(event: dict) -> bool:
    # write code here

    groupme_client.groups.list()
    return True


def process_board(board: str) -> None:
    return None
