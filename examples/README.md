# Weather Agent Examples

This folder contains two beginner-friendly agent examples for learning how tool-calling agents work.

## Files

- `weather_agent.py` — OpenAI-based agent using the hosted API
- `weather-agent-ollama.py` — local agent using Ollama and your own machine

## 1) OpenAI weather agent

File: `weather_agent.py`

This version uses the OpenAI Python SDK and a custom `get_weather` tool. It demonstrates the basic workflow of an agent:

- understand the user request
- decide whether a tool is needed
- call the function
- send the result back to the model
- produce the final answer

### Setup

```bash
cd /Users/saikettewary/repo/ai-sandbox
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then add your key to `.env`:

```bash
OPENAI_API_KEY=your_key_here
```

### Run

```bash
source .venv/bin/activate
python examples/weather_agent.py
```

### Notes

- Requires an OpenAI account with available credits.
- If you have no remaining quota, the script will fail with an API billing error.
- Good example for learning the standard hosted-model tool-calling pattern.

## 2) Local Ollama weather agent

File: `weather-agent-ollama.py`

This version runs locally with Ollama and does not need an API key or paid credits. It follows the same pattern as the OpenAI agent but uses a local model instead of a hosted cloud model.

### Setup

1. Install Ollama from https://ollama.com/download
2. Verify that the CLI is available:

```bash
ollama --version
```

If it is not found, add the app bundle path to your shell PATH:

```bash
export PATH="/Applications/Ollama.app/Contents/Resources:$PATH"
```

### Start Ollama

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

- Uses the local Ollama server on `http://localhost:11434`
- Works without API keys or billing
- Best option for learning locally and experimenting without external quota issues

## Learning outcome

Both agents teach the same core agent pattern:

1. receive a prompt
2. decide if a tool is needed
3. call the tool
4. use the tool result
5. produce the final answer

This is the foundation for moving from single-agent scripts to more advanced multi-agent and workflow-based systems.
