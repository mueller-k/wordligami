import os

from aws_cdk import (
    Duration,
    SecretValue,
    Stack,
    aws_dynamodb,
    aws_lambda,
    aws_secretsmanager,
)
from constructs import Construct


class MyStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        name_of_the_game = "wordligami"

        groupme_secret_token = aws_secretsmanager.Secret(
            self,
            "groupme-token-secret",
            secret_name=f"{name_of_the_game}-groupme-token",
            secret_object_value={"token": SecretValue.unsafe_plain_text("replace-me")},
        )
        msg_proc_function = aws_lambda.Function(
            self,
            "msg-proc-function",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.handler",
            code=aws_lambda.Code.from_asset(
                os.path.join("src", "msg-processor"),
                exclude=["tests", "requirements*", "README.md"],
            ),
            environment={"GROUPME_TOKEN_SECRET_ARN": groupme_secret_token.secret_arn},
            timeout=Duration.minutes(1),
        )

        groupme_secret_token.grant_read(msg_proc_function)

        board_table = aws_dynamodb.Table(
            self,
            "game-boards-table",
            table_name=name_of_the_game,
            partition_key=aws_dynamodb.Attribute(
                name="board", type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name="userBoardNumber", type=aws_dynamodb.AttributeType.STRING
            ),
        )

        board_table.grant_read_write_data(msg_proc_function)
