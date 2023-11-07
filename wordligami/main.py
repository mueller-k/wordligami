import os

from aws_cdk import (BundlingOptions, Duration, SecretValue, Stack,
                     aws_apigatewayv2_alpha,
                     aws_apigatewayv2_integrations_alpha, aws_dynamodb,
                     aws_iam, aws_lambda, aws_route53, aws_secretsmanager)
from constructs import Construct

NAME_OF_THE_GAME = "wordligami"


class DnsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        aws_route53.HostedZone(self, "hosted-zone", zone_name=f"{NAME_OF_THE_GAME}.com")


class MyStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        NAME_OF_THE_GAME = "wordligami"

        test_identity = aws_iam.Role(
            self, "test-role", assumed_by=aws_iam.AccountPrincipal(self.account)
        )

        groupme_secret_token = aws_secretsmanager.Secret(
            self,
            "groupme-token-secret",
            secret_name=f"{NAME_OF_THE_GAME}-groupme-token",
            secret_object_value={"token": SecretValue.unsafe_plain_text("replace-me")},
        )

        groupme_secret_token.grant_read(test_identity)

        api = aws_apigatewayv2_alpha.HttpApi(
            self, "http-api", api_name=NAME_OF_THE_GAME
        )

        msg_proc_function = aws_lambda.Function(
            self,
            "msg-proc-function",
            runtime=aws_lambda.Runtime.PYTHON_3_10,
            handler="lambda_function.handler",
            code=aws_lambda.Code.from_asset(
                os.path.join("src", "msg-processor"),
                bundling=BundlingOptions(
                    image=aws_lambda.Runtime.PYTHON_3_10.bundling_image,
                    command=[
                        "bash",
                        "-c",
                        "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output",
                    ],
                ),
                exclude=["tests", "requirements*", "README.md"],
            ),
            memory_size=500,
            environment={
                "GROUPME_TOKEN_SECRET_ARN": groupme_secret_token.secret_arn,
                "TABLE_NAME": NAME_OF_THE_GAME,
            },
            timeout=Duration.minutes(15),
        )

        groupme_secret_token.grant_read(msg_proc_function)

        api.add_routes(
            path="/message",
            methods=[aws_apigatewayv2_alpha.HttpMethod.POST],
            integration=aws_apigatewayv2_integrations_alpha.HttpLambdaIntegration(
                "post-message-integration", msg_proc_function
            ),
        )

        board_table = aws_dynamodb.Table(
            self,
            "game-boards-table",
            table_name=NAME_OF_THE_GAME,
            partition_key=aws_dynamodb.Attribute(
                name="board", type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name="userBoardNumber", type=aws_dynamodb.AttributeType.STRING
            ),
        )

        board_table.grant_read_write_data(msg_proc_function)
