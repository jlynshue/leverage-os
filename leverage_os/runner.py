"""LLM runner with a swappable provider seam.

The ``invoke_model`` function preserves its existing call site in ``cli.py`` and
remains a thin wrapper over ``get_provider().invoke(prompt)``. Add new providers
by implementing the ``LLMProvider`` protocol and registering them in ``_PROVIDERS``.
"""

import json
import os
from typing import Protocol

import boto3
from rich.console import Console

console = Console()

DEFAULT_REGION = os.environ.get("AWS_REGION", "us-east-1")
DEFAULT_MODEL_ID = os.environ.get(
    "BEDROCK_MODEL_ID", "us.anthropic.claude-sonnet-4-6"
)
DEFAULT_PROVIDER = os.environ.get("LEVERAGE_OS_PROVIDER", "bedrock")


class LLMProvider(Protocol):
    """Minimal interface every analytical engine must satisfy."""

    name: str

    def invoke(self, prompt: str) -> str | None:
        ...


def get_bedrock_client(region: str | None = None):
    """Create a Bedrock Runtime client."""
    return boto3.client(
        "bedrock-runtime",
        region_name=region or DEFAULT_REGION,
    )


class BedrockProvider:
    """AWS Bedrock-backed provider — current default."""

    name = "bedrock"

    def __init__(self, model_id: str | None = None, region: str | None = None):
        self.model_id = model_id or DEFAULT_MODEL_ID
        self.region = region or DEFAULT_REGION

    def invoke(self, prompt: str) -> str | None:
        client = get_bedrock_client(self.region)

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
                modelId=self.model_id,
                contentType="application/json",
                accept="application/json",
                body=body,
            )

            response_body = json.loads(response["body"].read())
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


class ManualProvider:
    """No-AI provider: returns None so the CLI falls back to the filled prompt."""

    name = "manual"

    def __init__(self, **_kwargs):
        pass

    def invoke(self, prompt: str) -> str | None:
        return None


_PROVIDERS: dict[str, type] = {
    "bedrock": BedrockProvider,
    "manual": ManualProvider,
}


def get_provider(name: str | None = None, **kwargs) -> LLMProvider:
    """Resolve a provider by name. Falls back to ``LEVERAGE_OS_PROVIDER`` env, then ``bedrock``."""
    resolved = name or DEFAULT_PROVIDER
    if resolved not in _PROVIDERS:
        console.print(
            f"[red]Unknown provider '{resolved}'. Known: {', '.join(_PROVIDERS)}.[/red]"
        )
        console.print("[yellow]Falling back to manual (no-AI) provider.[/yellow]")
        resolved = "manual"
    return _PROVIDERS[resolved](**kwargs)


def invoke_model(prompt: str, model_id: str | None = None, region: str | None = None) -> str | None:
    """Back-compat wrapper used by ``cli.py``. Delegates to the active provider."""
    provider_name = os.environ.get("LEVERAGE_OS_PROVIDER", DEFAULT_PROVIDER)
    kwargs: dict = {}
    if provider_name == "bedrock":
        kwargs = {"model_id": model_id, "region": region}
    return get_provider(provider_name, **kwargs).invoke(prompt)
