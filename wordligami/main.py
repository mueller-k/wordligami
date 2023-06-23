import os
from aws_cdk import Stack, SecretValue, aws_lambda, aws_secretsmanager
from constructs import Construct


class MyStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        groupme_secret_token = aws_secretsmanager.Secret(
            self,
            "groupme-token-secret",
            secret_name="groupme-token",
            secret_object_value={"token": SecretValue.unsafe_plain_text("replace-me")},
        )
        msg_proc_function = aws_lambda.Function(
            self,
            "msg-proc-function",
            runtime=aws_lambda.Runtime.PYTHON_3_10,
            handler="lambda_function.handler",
            code=aws_lambda.Code.from_asset(
                os.path.join("src", "msg-processor"), exclude=["tests", "requirements*", "README.md"]
            ),
            environment={"GROUPME_TOKEN_SECRET_ARN": groupme_secret_token.secret_arn},
        )

        groupme_secret_token.grant_read(msg_proc_function)
