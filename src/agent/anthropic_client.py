"""Anthropic API client with tool calling support."""

import json
import os
from typing import Any, Optional
import requests


class AnthropicClient:
    """Client for Anthropic API with tool calling support."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        """Initialize Anthropic client.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            model: Model identifier (default: Claude Sonnet 4)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

        self.model = model
        self.base_url = "https://api.anthropic.com/v1"
        self.headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

    def create_message(
        self,
        messages: list[dict[str, str]],
        tools: Optional[list[dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system: Optional[str] = None,
    ) -> dict[str, Any]:
        """Send a message to Anthropic with optional tool definitions.

        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool definitions
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            system: System prompt

        Returns:
            Response dict from Anthropic API
        """
        # Anthropic API requires system prompt separate from messages
        # Extract system message if present
        if not system:
            system_messages = [m for m in messages if m.get("role") == "system"]
            if system_messages:
                system = system_messages[0].get("content", "")
                messages = [m for m in messages if m.get("role") != "system"]

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if system:
            payload["system"] = system

        # Add tools if provided
        if tools:
            payload["tools"] = tools

        response = requests.post(
            f"{self.base_url}/messages",
            headers=self.headers,
            json=payload,
            timeout=120,
        )

        if response.status_code != 200:
            raise RuntimeError(f"Anthropic API error {response.status_code}: {response.text}")

        return response.json()

    def extract_tool_calls(self, response: dict[str, Any]) -> list[dict[str, Any]]:
        """Extract tool calls from API response.

        Args:
            response: Response dict from create_message

        Returns:
            List of tool call dicts with 'id', 'name', 'input'
        """
        tool_calls = []

        # Anthropic API returns tool uses in content blocks
        content = response.get("content", [])
        for block in content:
            if block.get("type") == "tool_use":
                tool_calls.append({
                    "id": block.get("id", ""),
                    "name": block.get("name", ""),
                    "input": block.get("input", {})
                })

        return tool_calls

    def get_response_text(self, response: dict[str, Any]) -> str:
        """Extract text content from API response.

        Args:
            response: Response dict from create_message

        Returns:
            Text content from the response
        """
        content = response.get("content", [])
        text_parts = []

        for block in content:
            if block.get("type") == "text":
                text_parts.append(block.get("text", ""))

        return "".join(text_parts)
