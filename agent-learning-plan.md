# AI Agent Learning Plan

This repository is a learning sandbox for building agents and multi-agent systems.

## Step 1: Create a simple agent with one custom tool

Goal: understand the core agent loop:
- model decides when to call a tool
- tool runs in Python
- tool result returns to the model
- model writes the final answer

Files to use:
- `examples/step1_simple_agent.py`
- `.env.example`
- `requirements.txt`

### What to learn
- how to define a tool schema
- how to expose custom functions to the model
- how to handle tool-call responses
- how to build a simple loop around an LLM

## Step 2: Add real-world tools and memory

Goal: create a more realistic agent with:
- multiple tools
- memory or conversation context
- validation and error handling

Possible examples:
- travel planner agent
- research assistant
- task runner agent

## Step 3: Create a multi-agent app

Goal: move from a single agent to a system with multiple specialized agents:
- planner agent
- researcher agent
- coder agent
- verifier agent

Learn how to:
- route tasks between agents
- coordinate work
- share state and results
- add human approval / guardrails

## Practical order

1. Run the simple agent locally
2. Add 2-3 tools
3. Add memory
4. Split roles across multiple agents
5. Add orchestration and observability

## Notes

Start with a single agent before building multi-agent systems. The first step is the most important foundation.
