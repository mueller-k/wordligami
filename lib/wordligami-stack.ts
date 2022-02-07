import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as api from 'aws-cdk-lib/aws-apigateway';

import path = require("path");
import { ApiGateway } from 'aws-cdk-lib/aws-events-targets';

export class WordligamiStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const wordligamiFunction = new lambda.Function(this, ' WordligamiFunction', {
      runtime: lambda.Runtime.NODEJS_14_X,
      handler: 'index.handler',
      code: lambda.Code.fromAsset(path.join(__dirname, "..", "src"))
    })

    const wordligamiApi = new api.LambdaRestApi(this, 'WordligamiApi', {
      handler: wordligamiFunction,
      proxy: false
    })

    const boards = wordligamiApi.root.addResource("board")
    boards.addMethod('GET');
    boards.addMethod('POST');
  }
}
