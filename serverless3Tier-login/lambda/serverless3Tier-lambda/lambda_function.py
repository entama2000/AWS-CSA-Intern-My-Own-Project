import json
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table1 = event.get("table1")
    user_id = event.get("user_id")
    email = event.get("email")
    table = dynamodb.Table('serverless3Tier-table')
    
    table.put_item(
        Item={
            "table1": table1,
            "user_id": user_id,
            "email": email
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Add item to dynamodb!')
    }
