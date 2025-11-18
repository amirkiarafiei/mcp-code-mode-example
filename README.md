# MCP Code Mode Example

**Executing MCP Tools as Code Elicits Efficient Tool-calling by LLM Agents**

This repository demonstrates the benefits of executing tools as **discoverable code** versus **traditional tool calling**. It accompanies the article [**MCP Code Mode: Context Engineering for Efficient Tool Execution in LLM Agents**](https://medium.com/@amirkiarafiei/mcp-code-mode-context-engineering-for-efficient-tool-execution-in-llm-agents-c46e1ddf80ac).

> **IMPORTANT:** This project does not use the actual Model Context Protocol (MCP). It uses local native tools (Python/TypeScript) to simulate the architecture for testing and demonstration purposes.

## 📖 The Concept

Traditional agents load *all* tool definitions into the context window upfront. This leads to:
1.  **Context Pollution:** Wasted tokens on unused tools.
2.  **Inefficient Data Transfer:** Large data (like file contents) flows through the LLM.

**Code Mode** solves this by giving the agent just 3 generic tools: `list_directory`, `read_file`, and `execute_typescript`. The agent **discovers** the tools it needs from the filesystem and **writes code** to chain them together, bypassing the LLM for data transfer.

> 📚 **Read the full explanation in [docs/medium.md](./docs/medium.md)**

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+ (for TypeScript execution)
- Google Gemini API Key (or any other supported LLM)

### Installation

1.  **Clone and Install:**
    ```bash
    git clone https://github.com/amirkiarafiei/mcp-code-mode-example.git
    cd mcp-code-mode-example
    pip install -r requirements.txt
    npm install
    ```

2.  **Configure Environment:**
    ```bash
    cp .env.example .env
    # Open .env and add your GEMINI_API_KEY
    ```

## 🧪 Running the Comparison

### 1. Traditional Approach (The "Bloated" Way)
Loads all 20 tool definitions into context upfront.
```bash
python agent_example_1.py
```

### 2. Code Mode Approach (The Efficient Way)
Loads only 3 generic tools. The agent discovers what it needs and writes code.
```bash
python agent_example_2.py
```

## 📊 Real-World Results

We compared both approaches on a task: *"Download a meeting summary from Teams and upload it to Drive"* (out of 20 available tools).

| Metric | Traditional | Code Mode | Improvement |
| :--- | :--- | :--- | :--- |
| **Initial Context** | ~10k tokens | ~600 tokens | **94% reduction** |
| **Final Context** | ~14k tokens | ~2k tokens | **86% reduction** |
| **Data Flow** | Through LLM | Direct via Code | **Faster & Cheaper** |

*Run the scripts above to see the live token usage statistics for your specific run.*

## 📂 Project Structure

- `agent_example_1.py`: Traditional agent with 20+ tools loaded.
- `agent_example_2.py`: Code Mode agent with filesystem/exec tools.
- `agent_filesystem/`: The "MCP Server" simulated as a directory of scripts.
- `tools/`: Python implementations of the tools (for Example 1).
- `docs/`: Documentation and articles.

## 🤝 Contributing

Contributions are welcome! This project is for educational purposes to demonstrate concepts from Anthropic's MCP and Cloudflare's Code Mode.
