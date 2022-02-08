const AWS = require('aws-sdk');
const HTTPS = require('https');

const dynamo = new AWS.DynamoDB.DocumentClient();


/**
 * Provide an event that contains the following keys:
 *
 *   - operation: one of the operations in the switch statement below
 *   - tableName: required for operations that interact with DynamoDB
 *   - payload: a parameter to pass to the operation being performed
 */
exports.handler = async (event, context) => {
    console.log('Received event:', JSON.stringify(event, null, 2));

    const request = JSON.parse(event.body)

    if(request.text && containsBoard(request.text)) {
        console.log('We got a board.');

        const result = await postMessage();

        console.log("Submission result is ", result);
    } else {
        console.log('Ignoring message that does not contain a Wordle board.');
    }

    return {
        statusCode: 200,
        headers: {'Content-Type': 'application/json'}
      };
};

function containsBoard(messageText) {
    return true;
}

function postMessage() {
    botId = "b332332e1682058d050b9ba4cd"
    botResponse = "Hey it's me, the bot."

    const options = {
        hostname: "api.groupme.com",
        path: "/v3/bots/post",
        method: "POST"
    }

    body = {
        "bot_id": botId,
        "text": botResponse
    }

    console.log("Sending " + botResponse + " to " + botId)

    return new Promise((resolve, reject) => {
        const req = HTTPS.request(options, res => {
          let rawData = '';
    
          res.on('data', chunk => {
            rawData += chunk;
          });
    
          res.on('end', () => {
            try {
              resolve(JSON.parse(rawData));
            } catch (err) {
              reject(new Error(err));
            }
          });
        });
    
        req.on('error', err => {
          reject(new Error(err));
        });
    
        req.write(JSON.stringify(body));
        req.end();
      });
    }