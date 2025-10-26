import boto3
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import response, cors_headers

bedrock = boto3.client(
    'bedrock-runtime',
    region_name='us-east-1',
    aws_access_key_id=os.getenv("key_id"),
    aws_secret_access_key=os.getenv("access_key")
)

MODEL_ID = 'anthropic.claude-3-5-sonnet-20240620-v1:0'

def parse_body(event):
    b = event.get("body")
    if b is None:
        return {}
    if isinstance(b, str):
        try:
            return json.loads(b or "{}")
        except:
            return {}
    if isinstance(b, dict):
        return b
    return {}

def handler(event, context):
    # --- CORS preflight ---
    method = (event.get("requestContext", {}).get("http", {}).get("method")
              or event.get("httpMethod", "GET"))
    if method == "OPTIONS":
        return {"statusCode": 204, "headers": cors_headers(), "body": ""}

    # Parse body
    body = parse_body(event)
    description = body.get("description", "").strip()

    if not description:
        return response(400, {"message": "description is required"})

    try:
        # Create prompt
        content = f"I am a teacher trying to email my student. Do not include any extra phrases or wording unrelated to the email, just respond with the body of the template email. Can you generate a short and concise email for me to send based on this description of what I want to talk about: {description}"
        
        bedrock_body = json.dumps({
            "messages": [
                {"role": "user", "content": content}
            ],
            "max_tokens": 250,
            "temperature": 0.5,
            "anthropic_version": "bedrock-2023-05-31"
        })

        # Call Bedrock
        bedrock_response = bedrock.invoke_model(
            modelId=MODEL_ID,
            contentType='application/json',
            accept='application/json',
            body=bedrock_body
        )

        response_body = json.loads(bedrock_response['body'].read())
        generated_text = response_body['content'][0]['text']
        print(generated_text)

        return response(200, {"email_content": generated_text})

    except Exception as e:
        print(f"Bedrock Error: {str(e)}")
        return response(500, {"message": f"Failed to generate email: {str(e)}"})
    