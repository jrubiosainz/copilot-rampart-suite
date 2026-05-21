"""
Thin RAMPART adapter for GitHub Copilot custom agents.

Connects to either:
- A live Copilot Extensions API endpoint
- A local mock that simulates agent responses
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

import httpx


@dataclass
class CopilotAgentAdapter:
    """RAMPART-compatible adapter that sends prompts to a Copilot agent."""

    base_url: str = field(
        default_factory=lambda: os.environ.get(
            "COPILOT_AGENT_URL", "http://localhost:8321"
        )
    )
    token: str = field(
        default_factory=lambda: os.environ.get("COPILOT_AGENT_TOKEN", "mock-token")
    )
    timeout: float = 30.0

    def send(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        """Send a conversation to the agent and return the response."""
        payload = {"messages": messages}
        if tools:
            payload["tools"] = tools

        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(
                f"{self.base_url}/agent",
                json=payload,
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            )
            resp.raise_for_status()
            return resp.json()

    def get_last_text(self, response: dict) -> str:
        """Extract the assistant's text from the response."""
        choices = response.get("choices", [])
        if not choices:
            return ""
        return choices[0].get("message", {}).get("content", "")

    def get_tool_calls(self, response: dict) -> list[dict]:
        """Extract tool calls from the response."""
        choices = response.get("choices", [])
        if not choices:
            return []
        return choices[0].get("message", {}).get("tool_calls", [])
