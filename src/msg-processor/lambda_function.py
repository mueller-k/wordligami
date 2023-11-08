import json
import logging
import os
from typing import Tuple

import boto3
from boto3.dynamodb.conditions import Key
import emoji
from groupy.client import Client

logger = logging.getLogger()
logger.setLevel(logging.INFO)

groupme_token_secret_arn = os.environ.get("GROUPME_TOKEN_SECRET_ARN")
table_name = os.environ.get("TABLE_NAME")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(table_name)

green_square_emoji = "\\U0001f7e9"
final_row = green_square_emoji * 5


def handler(event, context) -> dict:
    logger.info("Processing event {event}...")

    message = json.loads(event.get("body", ""))
    wordligami_result = process_message(message)
    # backload_group("Banal")

    logger.info("Event processed.")
    return {"body": json.dumps(wordligami_result), "statusCode": 200}


def process_message(message: dict) -> dict:
    logger.info(f"Received message: {message}")

    message_text = message.get("text", "")
    if not message_text:
        logger.info("Message is empty. Ignoring message.")
        return {}

    decoded_message_text = decode_message(message_text)

    if not message_contains_wordle_submission(decoded_message_text):
        logger.info("Message is not a valid wordle submission. Ignoring message.")
        return {}

    wordle_board, wordle_board_number = parse_message(decoded_message_text)

    wordligami_result = get_wordligami_result(wordle_board)

    store_board(wordle_board, wordle_board_number, message.get("user_id", "000000"))
    logger.info("Message processed.")

    return wordligami_result


def get_wordligami_result(wordle_board: list) -> dict:
    result = {}
    wordle_board_db_format = convert_wordle_board_to_db_format(wordle_board)

    query_result = table.query(
        KeyConditionExpression=Key("board").eq(wordle_board_db_format)
    )

    result["wordligami"] = False if query_result.get("Count") > 0 else True
    result["matches"] = [
        {
            "board": item.get("board"),
            "board_number": item.get("userBoardNumber").split("#")[1],
            "user_id": item.get("userBoardNumber").split("#")[0],
        }
        for item in query_result.get("Items")
    ]

    logger.info("Woo! It's Wordligami!") if result["wordligami"] else logger.info(
        "Boo! No Wordligami!"
    )

    return result


def backload_group(group_name: str) -> None:
    logger.info(f"Backloading group {group_name}...")
    groupme_token = get_groupme_token()
    groupme_client = Client.from_token(groupme_token)
    wordle_group = [
        group for group in groupme_client.groups.list_all() if group.name == group_name
    ][0]
    for message in wordle_group.messages.list_all(limit=100):
        backload_message(message)

    logger.info(wordle_group)

    logger.info("Group backloaded.")
    return


def unicode_escape(chars, data_dict) -> str:
    return chars.encode("unicode-escape").decode()


def decode_message(message_text: str) -> str:
    return emoji.replace_emoji(message_text, replace=unicode_escape)


def backload_message(message) -> None:
    logger.info(f"Backloading message: {message}...")

    if not message.text:
        logger.info("Message is empty. Ignoring message.")
        return

    decoded_message_text = decode_message(message.text)

    if not message_contains_wordle_submission(decoded_message_text):
        logger.info("Message is not a valid wordle submission. Ignoring message.")
        return

    wordle_board, wordle_board_number = parse_message(decoded_message_text)

    store_board(wordle_board, wordle_board_number, message.user_id)
    logger.info("Message backloaded.")
    return


def parse_message(message) -> Tuple[list, str]:
    """Parse validated message for Wordle submission"""
    end_of_board_index = message.find(final_row) + len(final_row)

    words = message[:end_of_board_index].split()

    wordle_index = words.index("Wordle")
    wordle_board_number = words[wordle_index + 1]
    wordle_board = words[wordle_index + 3:]  # fmt: skip

    return wordle_board, wordle_board_number


def store_board(wordle_board: list, wordle_board_number: str, user_id: str) -> None:
    wordle_board_db_format = convert_wordle_board_to_db_format(wordle_board)

    table.put_item(
        Item={
            "board": wordle_board_db_format,
            "userBoardNumber": f"{user_id}#{wordle_board_number}",
        }
    )

    return


def convert_wordle_board_to_db_format(wordle_board: list) -> str:
    wordle_board_db_format = ""
    for row in wordle_board:
        row_db_format = (
            row.replace("\\U0001f7e9", "g")
            .replace("\\u2b1b", "w")
            .replace("\\u2b1c", "w")
            .replace("\\U0001f7e8", "y")
        )
        wordle_board_db_format = wordle_board_db_format + row_db_format
    return wordle_board_db_format


def message_contains_wordle_submission(message_text: str) -> bool:
    """Validate if message text contains a Wordle result."""
    if not message_text:
        return False

    words = message_text.split()

    try:
        wordle_index = words.index("Wordle")
    except ValueError:
        return False

    try:
        wordle_board_number = words[wordle_index + 1]
    except IndexError:
        return False

    return (
        "Wordle" in words
        and str(wordle_board_number).isnumeric()
        and final_row in message_text
    )


def get_groupme_token() -> str:
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager")
    get_secret_value_response = client.get_secret_value(
        SecretId=groupme_token_secret_arn
    )

    groupme_token_secret = get_secret_value_response["SecretString"]
    groupme_token_secret_object = json.loads(groupme_token_secret)
    return groupme_token_secret_object.get("token", "")
