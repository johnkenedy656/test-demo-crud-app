import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('product')

def lambda_handler(event, context):
    

    response = {
        "statusCode": 500,
        "body": "An error occured" 
    }
    
    if event['httpMethod'] == 'POST':

        post_str = event['body']
        post = json.loads(post_str)
        
    
        response = table.put_item(Item=post)
        
        # If creation is successful
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            response = {
                "statusCode": 201,
                "body":json.dumps({"message":"creation success"})
                
             } 
            
    if event['httpMethod'] == 'GET' and event['resource'] == '/producttest':
        
        result = table.scan()
        response = {
            "statusCode": 200,
            "body":json.dumps(result['Items'])
        }
        
    if event['httpMethod'] == 'GET' and event['resource'] == '/producttest/{productId}':
        
        get_response = get(event,context)
        
        response = {
            "statusCode": 200,
            "body":json.dumps(get_response['Items'])
        }
        
             
    if event['httpMethod'] == 'DELETE' and event['resource'] == '/producttest/{productId}':
        
        get_response = get(event,context)
        
        if get_response['ScannedCount'] <= 0:
            response = {
                    "statusCode": 200,
                    "body":json.dumps({"message":"item not found"})
                    
            }
            
            return response
            
        
        productId = event['pathParameters']['productId']
        result = table.delete_item(
                Key={
                    'productId':productId
                })
                
        if result['ResponseMetadata']['HTTPStatusCode'] == 200:
            response = {
                    "statusCode": 200,
                    "body":json.dumps({"message":"deletion successful"})
                    
            }
         
    if event['httpMethod'] == 'PATCH' and event['resource'] == '/producttest/{productId}':
        
        get_response = get(event,context)
        
        post_str = event['body']
        post = json.loads(post_str)
        
        response = table.update_item(
            Key = {'productId':post['productId']},
            UpdateExpression="set price=:p,features=:a,locan=:l",
            ExpressionAttributeValues={
            ':p': post['price'],
            ':a': post['features'],
            ':l': post['locan']
        
        },
        )
        response = {'statusCode' :200,'body':json.dumps({"message":"updated_succesfull"})}
    
    return response
    
    
def get(event,context):
    
    productId = event['pathParameters']['productId']
    
    print(productId)
    result = table.query(
            KeyConditionExpression=Key('productId').eq(productId)
            )
            
    print(result)
            
    return result
    