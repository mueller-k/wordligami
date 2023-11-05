import json
import logging
import os

import boto3
import emoji
from groupy.client import Client

logger = logging.getLogger()
logger.setLevel(logging.INFO)

groupme_token_secret_arn = os.environ.get("GROUPME_TOKEN_SECRET_ARN")
table_name = os.environ.get("TABLE_NAME")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(table_name)


def handler(event, context) -> None:
    logger.info("Processing event...")
    # process_event(event)
    process_group("Banal")
    logger.info("Event processed.")
    return None


def process_group(group_name: str) -> bool:
    groupme_token = get_groupme_token()
    groupme_client = Client.from_token(groupme_token)
    wordle_group = [
        group for group in groupme_client.groups.list_all() if group.name == group_name
    ][0]
    logger.info("Processing the first 7 messages...")
    for message in wordle_group.messages.list()[:7]:
        process_message(message)

    logger.info(wordle_group)

    return True


def unicode_escape(chars, data_dict):
    return chars.encode("unicode-escape").decode()


def process_message(message) -> None:
    logger.info(f"Processing message: {message}")
    text = message.text
    if not valid_message_text(text):
        logger.info("Message is not a valid wordle submission. Ignoring message.")

    words = text.split()
    wordle_index = words.index("Wordle")
    wordle_board_number = words[wordle_index + 1]
    wordle_board_raw = words[wordle_index + 3:]

    store_board(wordle_board_raw, wordle_board_number, message.user_id)
    logger.info("Message processed.")
    return


def store_board(wordle_board: list, wordle_board_number: str, user_id: str) -> None:
    wordle_board_db_format = convert_wordle_board_to_db_format(wordle_board)

    table.put_item(
        Item={
            "board": wordle_board_db_format,
            "userBoardNumber": f"{user_id}#{wordle_board_number}",
        }
    )

    return


def convert_wordle_board_to_db_format(wordle_board_raw: list) -> str:
    wordle_board_db_format = ""
    for row in wordle_board_raw:
        row_decoded = emoji.replace_emoji(row, replace=unicode_escape)
        row_db_format = (
            row_decoded.replace("\\U0001f7e9", "g")
            .replace("\\u2b1b", "w")
            .replace("\\U0001f7e8", "y")
        )
        wordle_board_db_format = wordle_board_db_format + row_db_format
    return wordle_board_db_format


def valid_message_text(message_text: str) -> bool:
    """Validate if message text contains a Wordle result."""
    words = message_text.split()

    try:
        wordle_index = words.index("Wordle")
    except ValueError:
        return False

    return "Wordle" in words and str(words[wordle_index + 1]).isnumeric()


def get_groupme_token() -> str:
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager")
    get_secret_value_response = client.get_secret_value(
        SecretId=groupme_token_secret_arn
    )

    groupme_token_secret = get_secret_value_response["SecretString"]
    groupme_token_secret_object = json.loads(groupme_token_secret)
    return groupme_token_secret_object.get("token", "")
