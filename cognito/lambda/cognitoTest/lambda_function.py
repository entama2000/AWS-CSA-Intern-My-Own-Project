import json
import boto3
import botocore

import os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')

def passChecker(password):
    if(len(password) >= 8):
        return True
    else:
        return False

def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('cognito-idp', region_name='us-east-1')
    user_poolid = 'us-east-1_I2Wwu439N'
    user_email = event['userId']
    password = event['userPassword']
    inotp = event['otp']
    tableSession = dynamodb.Table('cognitoTest-signup-otp')
    
    if not passChecker(password):
        errorMsg = {
            "message": "password format is invalid."
        }
        return {
            'statusCode': 600,
            'body': json.dumps(errorMsg)
        }
    # check if the submitted session exist
    tokenInfo = tableSession.get_item(
        Key={
            'email': user_email
        }
    )
    try:
        otp = tokenInfo['Item']['otp']
    except KeyError:
        print("Invalid email")
        errorMsg = {
            "message": "Invalid email..."
        }
        return {
            'statusCode': 300,
            'body': json.dumps(errorMsg)
        }
    
    print(otp)
    print(inotp)
        
    if int(otp) != int(inotp):
        print("Invalid One Time Password")
        errorMsg = {
            "message": "Invalid One Time Password..."
        }
        return {
            'statusCode': 301,
            'body': json.dumps(errorMsg)
        }
    
    try:
        response = client.admin_create_user(
            UserPoolId=user_poolid,
            Username=user_email,
            MessageAction='SUPPRESS',
        )
        
        response = client.admin_set_user_password(
            UserPoolId=user_poolid,
            Username=user_email,
            Password=password,
            Permanent=True,
        )
        
        loginInfo = tableSession.delete_item(
            Key={
                'email': user_email
            }
        )
    
        resp = {
            "message": "Signed up successfully!"
        }
        return {
            'statusCode': 200,
            'body': json.dumps(resp)
        }
        
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'UsernameExistsException':
            logger.info('username is already exists.')
            errorMsg = {
                "message": "username is already exists."
            }
            return {
                'statusCode': 400,
                'body': json.dumps(errorMsg)
            }
        elif error.response['Error']['Code'] == 'InvalidPasswordException':
            logger.info('invalid password.')
            errorMsg = {
                "message": "password format is invalid."
            }
            return {
                'statusCode': 401,
                'body': json.dumps(errorMsg)
            }
        else:
            raise error
