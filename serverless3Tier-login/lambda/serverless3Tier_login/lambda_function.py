import json
import hashlib
import datetime
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    email = event.get("email")
    inputpswd = event.get("password")
    tableLogin = dynamodb.Table('serverless3Tier_login')
    tableSession = dynamodb.Table('serverless3Tier_login_session')
    
    loginInfo = tableLogin.get_item(
        Key={
            'email': email
        }
    )
    
    try:
        pswd = loginInfo['Item']['password']
    except KeyError:
        print("Invalid User")
        return {
            'statusCode': 300,
            'body': json.dumps('Invalid User')
        }
    
    # print(pswd)
    if pswd != inputpswd:
        print("Invalid Password")
        return {
            'statusCode': 301,
            'body': json.dumps('Invalid Password')
        }
        
    #check if the session already exists
    # sessionInfo = tableSession.get_item(
    #     Key={
    #         'email': email
    #     }
    # )
    # print(sessionInfo)
        
    # make hash for the session token
    dt_now = datetime.datetime.now()
    session_id = hashlib.md5(email.encode() + dt_now.isoformat().encode())
    print("hash", session_id.hexdigest())
    
    ttl = dt_now + datetime.timedelta(hours=1)
    
    # save session on the database
    tableSession.put_item(
        Item={
            "session_id": session_id.hexdigest(),
            "email": email,
            "ttl": ttl.strftime('%Y/%m/%d %H:%M:%S')
        }
    )
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Logined Successfully!'),
        'session_id': session_id.hexdigest()
    }
