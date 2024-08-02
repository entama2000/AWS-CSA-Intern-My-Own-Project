import json
import boto3
import logging
import botocore
import random

from emailsender import send_email

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
        
        token = response["AuthenticationResult"]["IdToken"]

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
            
    # create OTP
    otp1 = random.randint(100, 999)
    otp2 = random.randint(100, 999)
    otp = str(otp1) + str(otp2)
    print(otp)
    
    # send OPT to email
    from_email = 'xxxxxx@gmail.com'

    # メールを送る相手のアドレス
    to_email = username

    # 件名
    subject = 'entamaLogin - One Time Password'

    # 本文
    message = otp

    # アプリパスワードを設定
    # やり方 Googleのアカウント→セキュリティ→2段階認証→アプリパスワード
    smtp_password = 'xxxx xxxx xxxx xxxx'

    # メール送信関数を呼び出す
    send_email(from_email, to_email, subject, message, smtp_password)

    #DynamoDB
    dynamodb = boto3.resource('dynamodb')
    
    tableSession = dynamodb.Table('cognitoTest-sfo')
    
    tableSession.put_item(
        Item={
            "email": username,
            "otp": otp,
            "token": token
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Sent One Time Password Successfully!')
    }