"""LLM runner using AWS Bedrock."""

import json
import os

import boto3
from rich.console import Console

console = Console()

DEFAULT_REGION = os.environ.get("AWS_REGION", "us-east-1")
DEFAULT_MODEL_ID = os.environ.get(
    "BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0"
)


def get_bedrock_client(region: str | None = None):
    """Create a Bedrock Runtime client."""
    return boto3.client(
        "bedrock-runtime",
        region_name=region or DEFAULT_REGION,
    )


def invoke_model(prompt: str, model_id: str | None = None, region: str | None = None) -> str:
    """Send a prompt to Claude via AWS Bedrock and return the response text."""
    client = get_bedrock_client(region)
    mid = model_id or DEFAULT_MODEL_ID

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "temperature": 0.7,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }
    )

    try:
        response = client.invoke_model(
            modelId=mid,
            contentType="application/json",
            accept="application/json",
            body=body,
        )

        response_body = json.loads(response["body"].read())
        # Claude response format
        if "content" in response_body:
            return "".join(
                block["text"]
                for block in response_body["content"]
                if block.get("type") == "text"
            )
        return str(response_body)

    except Exception as e:
        console.print(f"[red]Error calling Bedrock: {e}[/red]")
        console.print("[yellow]Returning filled prompt without LLM analysis.[/yellow]")
        return None
