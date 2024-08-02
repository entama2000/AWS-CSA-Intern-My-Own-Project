import json
import datetime
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    token = event.get("token")
    tableSession = dynamodb.Table('serverless3Tier_login_session')
    
    # check if the submitted session exist
    tokenInfo = tableSession.get_item(
        Key={
            'session_id': token
        }
    )
    
    try:
        email = tokenInfo['Item']['email']
        ttlstr = tokenInfo['Item']['ttl']
    except KeyError:
        print("Invalid Token")
        return {
            'statusCode': 300,
            'body': json.dumps('Invalid Token')
        }
    
    dt_now = datetime.datetime.now()
    s_format = '%Y/%m/%d %H:%M:%S'
    ttl = datetime.datetime.strptime(ttlstr, s_format)
    if dt_now > ttl:
        print("token expired")
        return {
            'statusCode': 300,
            'body': json.dumps('Token Expired')
        }
    
    print(email)
    
    return {
        'statusCode': 200,
        'email': email,
        'body': json.dumps('Logined Successfully using token!')
    }
