from projen.awscdk import AwsCdkPythonApp

project = AwsCdkPythonApp(
    author_email="mueller.kyle@principal.com",
    author_name="Kyle Mueller",
    cdk_version="2.1.0",
    module_name="wordligami",
    name="wordligami",
    version="0.1.0",
)

project.synth()