import json
import boto3
import logging
import botocore

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    # ユーザプールID
    user_poolid = 'us-east-1_I2Wwu439N'
    # クライアントID
    client_id = '6j0hnhklmeaiuihphilj1enf93'
    # アカウント情報
    username = event['userId']
    userpass = event['userPassword']

    try:
        client = boto3.client('cognito-idp', region_name='us-east-1')

        response = client.admin_initiate_auth(
            UserPoolId = user_poolid,
            ClientId = client_id,
            AuthFlow = "ADMIN_USER_PASSWORD_AUTH",
            AuthParameters = {
                "USERNAME": username,
                "PASSWORD": userpass,
            }
        )

        logger.info(response["AuthenticationResult"]["AccessToken"])
        logger.info(response["AuthenticationResult"]["RefreshToken"])
        logger.info(response["AuthenticationResult"]["IdToken"])
        
        resp = {
            "IdToken": response["AuthenticationResult"]["IdToken"]
        }

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(resp)
        }

    except botocore.exceptions.ClientError as error:
        errorMsg = {
            "message": "Invalid id or password..."
        }
        if error.response['Error']['Code'] == 'NotAuthorizedException':
            logger.info('user not found.')
            return {
                'statusCode': 300,
                'body': json.dumps(errorMsg)
            }
        else:
            raise error