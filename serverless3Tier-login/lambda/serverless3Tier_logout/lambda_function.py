import json
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    inputtoken = event.get("token")
    tableSession = dynamodb.Table('serverless3Tier_login_session')
    
    # check if the submitted session exist
    tokenInfo = tableSession.get_item(
        Key={
            'session_id': inputtoken
        }
    )
    
    try:
        otp = tokenInfo['Item']['email']
    except KeyError:
        print("Invalid token")
        errorMsg = {
            "message": "Invalid token..."
        }
        return {
            'statusCode': 300,
            'body': json.dumps(errorMsg)
        }
    
    # save session on the database
    resp = tableSession.delete_item(
        Key={
            "session_id": inputtoken
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Logout Successfully!')
    }
