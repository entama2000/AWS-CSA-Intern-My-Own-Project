import json
import boto3
import logging
import botocore

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# CognitoIdentityProviderクライアント（Using Amazon Cognito user pools API）
idp_client = boto3.client('cognito-idp')

# CognitoIdentityクライアント（Using Amazon Cognito Federated Identities）
identity_client = boto3.client('cognito-identity')

# 設定情報
account_id = '637423523595'
region = 'us-east-1'
user_pool_id = 'us-east-1_I2Wwu439N'
identity_pool_id = 'us-east-1:ffc1e381-4921-4a15-94ce-0c2fca351a34'
client_id = '6j0hnhklmeaiuihphilj1enf93'
auth_flow = "ADMIN_NO_SRP_AUTH"
logins_key = f"cognito-idp.{region}.amazonaws.com/{user_pool_id}"

def get_id(id_token):
    response = identity_client.get_id(
        AccountId = account_id,
        IdentityPoolId = identity_pool_id,
        Logins={
            logins_key: id_token
        }
    )
    return response
    
def get_credentials_for_identity(identity_id, id_token):
    response = identity_client.get_credentials_for_identity(
        IdentityId = identity_id,
        Logins = {
            logins_key: id_token
        }
    )
    return response

def lambda_handler(event, context):
    try:
        # Access to bedrock
        id_token = event.get("IdToken")
        
        # アイデンティティIDを取得
        id_response = get_id(id_token)
        identity_id = id_response['IdentityId']
        
        # Bedrockにアクセスするクレデンシャルを取得
        credentials_response = get_credentials_for_identity(identity_id, id_token)
        Credentials = credentials_response['Credentials']
        access_key_id = Credentials['AccessKeyId']
        secret_access_key = Credentials['SecretKey']
        session_token = Credentials['SessionToken']
        
        # Bedrockにアクセス
        bedrock_runtime = boto3.client('bedrock-runtime',
                    region_name="us-east-1",
                    aws_access_key_id=access_key_id,
                    aws_secret_access_key=secret_access_key,
                    aws_session_token=session_token
                )
    
    
        # Bedrock
        user_message = {"role": "user", "content": event.get("prompt")}
        messages = [user_message]
        
        model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
        system_prompt = "このjsonはuserとassistantの会話です。最後のuserの言葉に答えなさい。"
        #system_prompt = "Answer in one sentence"
        #system_prompt = ""
        max_tokens = 1000
        
        accept = 'application/json'
        contentType = 'application/json'
        
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "system": system_prompt,
                "messages": messages
            }  
        )
    
        response = bedrock_runtime.invoke_model(body=body, modelId=model_id)
        
        # APIレスポンスからBODYを取り出す
        response_body = response.get('body')
        if response_body is not None:
            response_body = json.loads(response_body.read())
        else:
            errorMsg = {
                "message": "Something Wrong when invoking bedrock..."
            }
            return {
                'statusCode': 500,
                'body': json.dumps(errorMsg)
            }
    
        resp = {
            "answer": response_body["content"][0]["text"]
        }
        return {
            'statusCode': 200,
            'body': json.dumps(resp)
        }
    except botocore.exceptions.ClientError as error:
        errorMsg = {
            "message": "Invalid Token..."
        }
        if error.response['Error']['Code'] == 'NotAuthorizedException':
            logger.info('Invalid Token...')
            return {
                'statusCode': 300,
                'body': json.dumps(errorMsg)
            }
        else:
            raise error
