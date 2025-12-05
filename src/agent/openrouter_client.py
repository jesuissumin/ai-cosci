"""OpenRouter API client with tool calling support."""

import json
import os
from typing import Any, Optional
import requests


class OpenRouterClient:
    """Client for OpenRouter API with tool calling support."""

    def __init__(self, api_key: Optional[str] = None, model: str = "anthropic/claude-sonnet-4"):
        """Initialize OpenRouter client.

        Args:
            api_key: OpenRouter API key (defaults to OPENROUTER_API_KEY env var)
            model: Model identifier (default: Claude Sonnet 4)
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment")

        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def create_message(
        self,
        messages: list[dict[str, str]],
        tools: Optional[list[dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        top_p: float = 1.0,
    ) -> dict[str, Any]:
        """Send a message to OpenRouter with optional tool definitions.

        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool definitions
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            top_p: Nucleus sampling parameter

        Returns:
            Response dict from OpenRouter API
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
        }

        # Add tools if provided
        if tools:
            payload["tools"] = tools

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json=payload,
            timeout=120,
        )

        if response.status_code != 200:
            raise RuntimeError(f"OpenRouter API error {response.status_code}: {response.text}")

        return response.json()

    def extract_tool_calls(self, response: dict[str, Any]) -> list[dict[str, Any]]:
        """Extract tool calls from API response.

        Args:
            response: Response dict from create_message

        Returns:
            List of tool call dicts with 'id', 'name', 'input'
        """
        tool_calls = []

        if not response.get("choices"):
            return tool_calls

        message = response["choices"][0].get("message", {})

        # Handle tool_calls field (standard OpenAI format)
        if "tool_calls" in message:
            for call in message["tool_calls"]:
                if call.get("type") == "function":
                    func = call.get("function", {})
                    tool_calls.append({
                        "id": call.get("id", ""),
                        "name": func.get("name", ""),
                        "input": json.loads(func.get("arguments", "{}"))
                    })

        return tool_calls

    def get_response_text(self, response: dict[str, Any]) -> str:
        """Extract text content from API response.

        Args:
            response: Response dict from create_message

        Returns:
            Text content from the response
        """
        if not response.get("choices"):
            return ""

        message = response["choices"][0].get("message", {})
        return message.get("content", "")
