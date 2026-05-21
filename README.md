# copilot-rampart-suite

A ready-to-use RAMPART test suite for GitHub Copilot custom agents. Write prompt injection and safety tests for your `.agent.md` agents and run them in CI with a single `pytest` command.

## What it does

1. Defines a thin adapter that connects RAMPART to any Copilot agent via the Copilot Extensions API (or a local mock).
2. Ships 5 pre-built test scenarios covering the most common attack vectors:
   - Cross-prompt injection via code comments
   - Indirect injection via issue/PR body
   - Tool-call hijacking (MCP sandbox escape)
   - Exfiltration through markdown links
   - Instruction override via system prompt leak
3. Outputs standard pytest results. Plug into GitHub Actions and block merges on failure.

## Quick start

```bash
pip install -r requirements.txt
# Run against the included mock agent
pytest tests/ -v

# Run against a real Copilot agent endpoint
export COPILOT_AGENT_URL=https://your-agent.example.com
export COPILOT_AGENT_TOKEN=ghp_xxx
pytest tests/ -v --live
```

## Project structure

```
copilot-rampart-suite/
├── README.md
├── requirements.txt
├── conftest.py              # pytest fixtures + RAMPART adapter
├── adapter/
│   └── copilot_adapter.py  # Thin adapter for Copilot Extensions API
├── agents/
│   └── sample.agent.md     # Sample agent definition for testing
├── tests/
│   ├── test_cross_prompt_injection.py
│   ├── test_indirect_injection.py
│   ├── test_tool_hijack.py
│   ├── test_exfiltration.py
│   └── test_instruction_override.py
└── .github/
    └── workflows/
        └── rampart.yml     # CI workflow
```

## How to adapt for your agents

1. Replace `agents/sample.agent.md` with your own agent definition.
2. Set `COPILOT_AGENT_URL` to your agent endpoint.
3. Add domain-specific scenarios in `tests/` following the existing patterns.

## Requirements

- Python 3.11+
- RAMPART (`pip install rampart-ai`)
- A Copilot agent endpoint or the included mock

## License

MIT
