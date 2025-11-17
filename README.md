# MCP Code Mode Example

**Executing MCP Tools as Code Elicits Efficient Tool-calling by LLM Agents**

This repository demonstrates the benefits of executing MCP (Model Context Protocol) tools as code versus traditional tool calling approaches. It includes a comprehensive Medium article explaining the concepts and working code examples comparing both approaches.

>NOTE: This project uses LangChain tools and a local filesystem to simulate MCP-style tools and code execution; it doesn’t implement the MCP protocol/tools itself. This code is for educational purpose only.

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

#### Verify Installation
First, verify all components work:
```bash
python test_verification.py
```

This will test all tools and TypeScript execution without requiring an API key.

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

#### Standalone TypeScript Example
See the direct code execution without an LLM:
```bash
npx tsx agent_filesystem/example_end_to_end.ts
```

This demonstrates how data flows through code efficiently.

## 📊 What Gets Demonstrated

### Visual Comparison

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRADITIONAL APPROACH                          │
│                    (agent_example_1.py)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  LLM Agent Context:                                             │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ System Prompt                                           │    │
│  │ ─────────────                                           │    │
│  │ Tool 1: download_meeting_summary(...)                  │    │
│  │   Description: Download comprehensive meeting...        │    │
│  │   Parameters: meeting_id, include_transcript...         │    │
│  │                                                          │    │
│  │ Tool 2: list_team_meetings(...)                        │    │
│  │   Description: Retrieve comprehensive list...           │    │
│  │   Parameters: team_id, start_date, end_date...         │    │
│  │                                                          │    │
│  │ ... (18 more tool schemas) ...                          │    │
│  │                                                          │    │
│  │ Tool 20: manage_drive_versions(...)                    │    │
│  │   Description: Manage file version history...           │    │
│  │   Parameters: file_id, action, revision_id...          │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Data Flow:                                                     │
│  Teams API → [8KB in LLM context] → LLM Decision → Drive API   │
│                                                                  │
│  ❌ High token usage (20 tool schemas)                         │
│  ❌ Large data through LLM context                              │
│  ❌ All tools loaded upfront                                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   CODE EXECUTION APPROACH                        │
│                    (agent_example_2.py)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  LLM Agent Context:                                             │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ System Prompt                                           │    │
│  │ ─────────────                                           │    │
│  │ Tool 1: list_directory(dir_path)                       │    │
│  │   Description: List filesystem contents                 │    │
│  │                                                          │    │
│  │ Tool 2: read_file(file_path)                           │    │
│  │   Description: Read file contents                       │    │
│  │                                                          │    │
│  │ Tool 3: execute_typescript(code)                       │    │
│  │   Description: Execute TypeScript code                  │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Agent discovers tools from filesystem:                         │
│  agent_filesystem/servers/teams/download_meeting_summary.ts     │
│  agent_filesystem/servers/drive/upload_to_drive.ts              │
│                                                                  │
│  Writes and executes:                                           │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ const summary = await download_meeting_summary();      │    │
│  │ await upload_to_drive(summary, 'file.md');            │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Data Flow:                                                     │
│  Teams API → [TypeScript variable] → Drive API                 │
│              (no LLM involvement)                                │
│                                                                  │
│  ✅ Low token usage (3 tool schemas)                            │
│  ✅ Large data bypasses LLM context                             │
│  ✅ Tools discovered on-demand                                  │
└─────────────────────────────────────────────────────────────────┘
```

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

## 📚 Additional Resources

- [SUMMARY.md](./SUMMARY.md): Technical project overview
- [CONTRIBUTING.md](./CONTRIBUTING.md): Guide for extending the examples
- [medium.md](./medium.md): Full article
