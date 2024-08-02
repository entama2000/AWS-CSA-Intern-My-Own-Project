import json
import boto3
import logging
import botocore
import random

from emailsender import send_email

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    # アカウント情報
    username = event['email']
            
    # create OTP
    otp1 = random.randint(100, 999)
    otp2 = random.randint(100, 999)
    otp = str(otp1) + str(otp2)
    print(otp)
    
    # send OPT to email
    from_email = 'xxxxx@gmail.com'

    # メールを送る相手のアドレス
    to_email = username

    # 件名
    subject = 'entama AI Register - One Time Password'

    # 本文
    message = "Thank you for registering entama AI Chat.\nThis below is the one time password. Don't share it.\n\n" + otp

    # アプリパスワードを設定
    # やり方 Googleのアカウント→セキュリティ→2段階認証→アプリパスワード
    smtp_password = 'xxxx xxxx xxxx xxxx'

    # メール送信関数を呼び出す
    send_email(from_email, to_email, subject, message, smtp_password)

    #DynamoDB
    dynamodb = boto3.resource('dynamodb')
    
    tableSession = dynamodb.Table('cognitoTest-signup-otp')
    
    tableSession.put_item(
        Item={
            "email": username,
            "otp": otp
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Sent One Time Password Successfully!')
    }