import json
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    email = event.get("email")
    inotp = event.get("otp")
    tableSession = dynamodb.Table('cognitoTest-signup-otp')
    
    # check if the submitted session exist
    tokenInfo = tableSession.get_item(
        Key={
            'email': email
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
        
    loginInfo = tableSession.delete_item(
        Key={
            'email': email
        }
    )
    
    resp = {
        "message": "Correct One-time password"
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