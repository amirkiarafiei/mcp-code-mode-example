# Project Summary: MCP Code Mode Example

## Overview
This repository demonstrates the advantages of executing MCP (Model Context Protocol) tools as code versus traditional tool calling in LLM agents. It includes a detailed article and working code examples.

## Key Components

### 1. Documentation
- **medium.md**: Comprehensive article explaining the concepts, problems with traditional approaches, and benefits of code execution mode
- **README.md**: Project documentation with setup instructions and usage examples
- **agent_filesystem/README.md**: Documentation of the tool filesystem structure

### 2. Traditional Tool Calling (Agent Example 1)
- **agent_example_1.py**: Agent using 20 native tools loaded upfront
- **tools/ms_teams_tools.py**: 10 Teams tools with extensive descriptions
- **tools/google_drive_tools.py**: 10 Drive tools with extensive descriptions

### 3. Code Execution Approach (Agent Example 2)
- **agent_example_2.py**: Agent using only 3 generic tools (filesystem + execution)
- **tools/typescript_shell_tool.py**: Tools for filesystem access and TypeScript execution
- **agent_filesystem/servers/teams/**: 10 Teams operations as TypeScript modules
- **agent_filesystem/servers/drive/**: 10 Drive operations as TypeScript modules
- **agent_filesystem/example_end_to_end.ts**: Standalone example showing data flow

### 4. Testing & Verification
- **test_verification.py**: Comprehensive test suite verifying all components
- Can be run without an API key to validate the setup

### 5. Data Files
- **teams/meeting_summary.md**: 8KB+ dummy meeting summary for testing
- **drive/**: Folder where uploaded files appear (gitignored)

### 6. Configuration
- **.env.example**: Template for environment variables (Gemini API key)
- **requirements.txt**: Python dependencies (langchain, google-generativeai)
- **package.json**: Node.js dependencies (tsx, TypeScript)
- **tsconfig.json**: TypeScript configuration

## Key Differences Demonstrated

### Traditional Approach (Example 1)
```
Agent Context:
├── System Prompt
├── Tool 1 Schema (Teams: download_meeting_summary)
├── Tool 2 Schema (Teams: list_team_meetings)
├── ... (18 more tool schemas)
└── Tool 20 Schema (Drive: manage_drive_versions)

Data Flow:
Teams API → LLM Context (8KB) → LLM Decision → Drive API
```

### Code Execution Approach (Example 2)
```
Agent Context:
├── System Prompt
├── Tool 1 Schema (list_directory)
├── Tool 2 Schema (read_file)
└── Tool 3 Schema (execute_typescript)

Data Flow:
Teams API → TypeScript Variable → Drive API (bypasses LLM)
```

## Benefits Demonstrated

1. **Context Efficiency**
   - Traditional: 20 tool schemas in context (high token usage)
   - Code Execution: 3 generic tool schemas (low token usage)

2. **Data Flow Optimization**
   - Traditional: Large data passes through LLM context
   - Code Execution: Large data flows directly through code

3. **On-Demand Discovery**
   - Traditional: All tools loaded upfront
   - Code Execution: Tools discovered and loaded as needed

4. **Better LLM Utilization**
   - Traditional: LLM generates JSON tool calls (less training data)
   - Code Execution: LLM writes TypeScript (more training data)

## Running the Examples

### Prerequisites
- Python 3.8+
- Node.js 18+
- Google Gemini API key (for agent examples)

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt
npm install

# Verify everything works
python test_verification.py

# Run traditional approach (requires API key)
python agent_example_1.py

# Run code execution approach (requires API key)
python agent_example_2.py

# See direct TypeScript execution
npx tsx agent_filesystem/example_end_to_end.ts
```

## Technical Implementation

### Python Tools (Traditional)
- Use LangChain's `@tool` decorator
- Extensive docstrings become part of LLM context
- Direct function invocation by agent

### TypeScript Tools (Code Execution)
- Exported async functions
- Minimal overhead
- Imported and called by generated code

### Execution Flow (Code Mode)
1. Agent explores `agent_filesystem/` with `list_directory`
2. Agent reads needed tool implementations with `read_file`
3. Agent writes TypeScript code importing and chaining tools
4. Agent executes code with `execute_typescript`
5. Results flow through code, not LLM context

## Files Not Tracked
- `node_modules/`: Node.js dependencies
- `.env`: Environment variables (API keys)
- `drive/*`: Generated files from testing
- `.tmp_exec_*`: Temporary TypeScript execution files

## Future Enhancements
- Support for other languages (Python, Go)
- More realistic tool implementations
- Performance benchmarking
- Token usage comparison metrics
- Support for streaming results

## References
- [Anthropic: Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Cloudflare: Code Mode](https://blog.cloudflare.com/code-mode/)
- [LangChain Documentation](https://python.langchain.com/)
