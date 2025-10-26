import boto3
import json
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import response, now_iso

bedrock = boto3.client(
        'bedrock-runtime',
        region_name='us-east-1',
        aws_access_key_id=os.getenv("key_id"),
        aws_secret_access_key=os.getenv("access_key"))
model_id = 'anthropic.claude-3-5-sonnet-20240620-v1:0'





def prompt(event, context):
    description = (event.get("body") or {}).get("input_description")
    content = f"I am a teacher trying to email my student. Can you generate a short and concise email for me to send based on this description of what I want to talk about: {description}"
    body = json.dumps({
    "messages":[
        {"role": "user", "content": content},
    ],
    "max_tokens": 250,
    "temperature": 0.5,
    "anthropic_version": "bedrock-2023-05-31",
})

    response = bedrock.invoke_model(
        modelId=model_id,
        contentType='application/json',
        accept='application/json',
        body=body
    )
    response_body = json.loads(response['body'].read())

    generated_text = response_body['content'][0]['text']

    print(generated_text)

prompt()