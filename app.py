import os

from aws_cdk import App, Environment

from wordligami.main import DnsStack, AppStack

# for development, use account/region from cdk cli
dev_env = Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
)

app = App()
dns_stack = DnsStack(app, "wordligami-dns-dev", env=dev_env)
AppStack(
    app, "wordligami-dev", dns_stack.hosted_zone, dns_stack.certificate, env=dev_env
)

# MyStack(app, "wordligami-prod", env=prod_env)

app.synth()
