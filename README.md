# Agent Learning Sandbox

This repository contains two simple agent examples built for learning how agents work with tools:

1. OpenAI-powered tool-calling agent
2. Local Ollama-based agent

Both are intentionally beginner-friendly and designed to teach the basic flow of:

- understanding a user request
- deciding whether to call a tool
- executing a tool
- sending results back to the model
- returning a final answer

## Files

- [examples/weather_agent.py](examples/weather_agent.py) — OpenAI tool-calling agent
- [examples/weather-agent-ollama.py](examples/weather-agent-ollama.py) — local Ollama tool-calling agent

## 1) OpenAI weather agent

This version uses the OpenAI SDK and a custom `get_weather` tool.

### Setup

```bash
cd /Users/saikettewary/repo/ai-sandbox
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then add your API key to `.env`:

```bash
OPENAI_API_KEY=your_key_here
```

### Run

```bash
source .venv/bin/activate
python examples/weather_agent.py
```

### Notes

- This version requires OpenAI credits.
- If your account has no credit remaining, the script will show the quota issue clearly.
- This is the best example to learn the standard tool-calling pattern with a hosted model.

## 2) Local Ollama weather agent

This version runs fully locally with Ollama and does not require an API key or paid credits.

### Prerequisites

Install Ollama from the official site:

https://ollama.com/download

Then verify the CLI is available:

```bash
ollama --version
```

If it is not found, add the binary to your PATH or use the app-installed location:

```bash
export PATH="/Applications/Ollama.app/Contents/Resources:$PATH"
```

### Start Ollama and pull a model

In one terminal:

```bash
ollama serve
```

In another terminal:

```bash
ollama pull llama3.2
```

### Run

```bash
cd /Users/saikettewary/repo/ai-sandbox
source .venv/bin/activate
python examples/weather-agent-ollama.py
```

### Notes

- This version uses the local Ollama server on `http://localhost:11434`
- It still follows the same tool-calling pattern as the OpenAI version
- It is the recommended version for learning locally without paying for API usage

## Comparison

| Version | Model | Cost | Local | Good for |
|---|---|---:|---:|---|
| OpenAI agent | OpenAI hosted model | Paid | No | understanding hosted agent/tool loops |
| Ollama agent | Local model | Free | Yes | learning without quota or API key issues |

## Learning goal

The point of both examples is to understand the basic architecture behind agentic systems:

- prompt and instructions
- tool definitions
- function calling
- result injection
- final answer generation

These examples are intentionally small but realistic enough to build on for more advanced multi-agent patterns later.
