# MCP Code Mode Example

**Executing MCP Tools as Code Elicits Efficient Tool-calling by LLM Agents**

This repository demonstrates the benefits of executing MCP (Model Context Protocol) tools as code versus traditional tool calling approaches. It includes a comprehensive Medium article explaining the concepts and working code examples comparing both approaches.

## 📖 Overview

When building LLM agents with many tools, two key problems emerge:

1. **Context Pollution**: All tool definitions get loaded into the agent's context upfront, wasting precious tokens
2. **Inefficient Data Transfer**: Large intermediate results flow through the expensive LLM instead of directly between functions

This repository shows how representing tools as discoverable code and executing them via a programming language (TypeScript) solves both problems.

## 📂 Project Structure

```
.
├── medium.md                          # Main article explaining the concepts
├── .env.example                       # Environment configuration template
├── requirements.txt                   # Python dependencies
├── package.json                       # Node.js dependencies for TypeScript
│
├── teams/
│   └── meeting_summary.md            # Dummy meeting summary (8KB+)
│
├── drive/                            # Dummy Google Drive folder
│
├── tools/
│   ├── ms_teams_tools.py             # 10 Teams tools (traditional)
│   ├── google_drive_tools.py         # 10 Drive tools (traditional)
│   └── typescript_shell_tool.py      # Filesystem & execution tools
│
├── agent_filesystem/
│   └── servers/
│       ├── teams/                    # 10 Teams tools as TypeScript
│       └── drive/                    # 10 Drive tools as TypeScript
│
├── agent_example_1.py                # Traditional tool calling approach
├── agent_example_2.py                # Code execution approach
└── prompt.py                         # Shared prompts
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+ (for TypeScript execution)
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/amirkiarafiei/mcp-code-mode-example.git
   cd mcp-code-mode-example
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies**
   ```bash
   npm install
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

### Running the Examples

#### Example 1: Traditional Tool Calling
```bash
python agent_example_1.py
```

This loads **all 20 tools** into the agent's context upfront, even though only 2 are needed.

#### Example 2: Code Execution Approach
```bash
python agent_example_2.py
```

This loads only **3 generic tools** (filesystem + execution), discovering specific tools on-demand.

## 📊 What Gets Demonstrated

### Scenario
An agent needs to:
1. Download a meeting summary from Teams (~8KB of text)
2. Upload it to Google Drive

### Traditional Approach (Example 1)
- ✗ All 20 tool definitions loaded into context
- ✗ Large meeting summary flows through LLM context
- ✗ LLM generates JSON tool calls
- ✗ High token usage for both input and output

### Code Execution Approach (Example 2)
- ✓ Only 3 generic tools in context
- ✓ Discovers only needed tools (2/20)
- ✓ Meeting summary flows through code, not LLM
- ✓ Lower token usage, more efficient

## 📝 The Article

Read the full explanation in [`medium.md`](./medium.md), which covers:

- How traditional tool calling works
- The two main problems (context pollution & data transfer)
- How code execution mode solves these problems
- Why LLMs might be better at writing code than JSON tool calls
- When this approach makes sense

## 🛠️ Tech Stack

- **Agent Framework**: LangChain (Python)
- **LLM**: Google Gemini (gemini-1.5-pro)
- **Code Execution**: TypeScript with ts-node
- **Tools**: 20 dummy tools simulating Teams & Drive APIs

## 🔍 Key Files

- **`medium.md`**: Complete article with technical explanations
- **`agent_example_1.py`**: Shows traditional approach with all tools loaded
- **`agent_example_2.py`**: Shows code execution with on-demand discovery
- **`tools/ms_teams_tools.py`**: Traditional LangChain tools with extensive descriptions
- **`agent_filesystem/servers/`**: Tools as TypeScript modules for code execution

## 📈 Benefits Summary

| Aspect | Traditional | Code Execution |
|--------|-------------|----------------|
| Tools in Context | 20 | 3 (generic) |
| Tool Discovery | Upfront | On-demand |
| Data Flow | Through LLM | Direct (via code) |
| Context Efficiency | Low | High |
| Token Usage | High | Lower |

## 🤝 Contributing

This is an educational example demonstrating concepts from:
- [Anthropic's Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Cloudflare's Code Mode](https://blog.cloudflare.com/code-mode/)

Feel free to open issues or PRs to improve the examples!

## 📄 License

MIT

## 🙏 Acknowledgments

- Anthropic for pioneering the code execution with MCP approach
- Cloudflare for their code mode implementation
- The LangChain team for excellent agent frameworks
