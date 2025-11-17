# Contributing to MCP Code Mode Example

Thank you for your interest in contributing! This document provides guidelines for extending the examples.

## How to Add New Tools

### Adding Traditional Tools (for agent_example_1.py)

1. **Add to Python tool files**
   
   Edit `tools/ms_teams_tools.py` or `tools/google_drive_tools.py`:
   
   ```python
   from langchain.tools import tool
   
   @tool
   def your_new_tool(param1: str, param2: int = 10) -> str:
       """
       Comprehensive description of what your tool does.
       This description will be part of the LLM's context.
       
       Args:
           param1: Description of param1
           param2: Description of param2
       
       Returns:
           Description of return value
       """
       # Your implementation
       return "result"
   ```

2. **Import in agent_example_1.py**
   
   Add your tool to the imports and tools list:
   
   ```python
   from tools.ms_teams_tools import your_new_tool
   
   tools = [
       # ... existing tools
       your_new_tool,
   ]
   ```

### Adding Code Execution Tools (for agent_example_2.py)

1. **Create TypeScript module**
   
   Add file to `agent_filesystem/servers/teams/` or `agent_filesystem/servers/drive/`:
   
   ```typescript
   /**
    * Brief description of what this tool does
    */
   
   export async function your_new_tool(
     param1: string,
     param2: number = 10
   ): Promise<any> {
     // Your implementation
     return { status: 'success' };
   }
   
   // Allow direct execution for testing
   if (require.main === module) {
     your_new_tool('test', 5)
       .then(result => console.log(result))
       .catch(error => console.error(error));
   }
   ```

2. **Test your tool**
   
   ```bash
   npx tsx agent_filesystem/servers/teams/your_new_tool.ts
   ```

3. **No changes needed to agent_example_2.py!**
   
   The agent will discover your tool automatically through filesystem exploration.

## Adding Tests

### Unit Tests for Traditional Tools

Add to `test_verification.py`:

```python
def test_your_new_tool():
    """Test your new tool"""
    print("=" * 60)
    print("TEST: your_new_tool")
    print("=" * 60)
    
    from tools.ms_teams_tools import your_new_tool
    result = your_new_tool.invoke({'param1': 'test', 'param2': 5})
    
    print(f"✓ Result: {result}")
    print()
```

### Integration Tests

Add TypeScript integration test:

```typescript
// agent_filesystem/test_your_tool.ts
import { your_new_tool } from './servers/teams/your_new_tool';

async function main() {
  const result = await your_new_tool('test', 5);
  console.log('Test passed:', result);
}

main().catch(console.error);
```

## Extending the Article

To add to `medium.md`:

1. **Keep the conversational tone**
   - Write like you're explaining to a colleague
   - Use concrete examples
   - Avoid jargon unless necessary

2. **Structure**
   - Problem statement first
   - Then the solution
   - End with benefits

3. **Code examples**
   - Show before/after comparisons
   - Highlight the key differences
   - Keep snippets concise

## Testing Guidelines

### Before Submitting

1. **Run verification tests**
   ```bash
   python test_verification.py
   ```

2. **Test TypeScript compilation**
   ```bash
   npx tsc --noEmit
   ```

3. **Verify both agent examples work**
   ```bash
   # Requires GEMINI_API_KEY in .env
   python agent_example_1.py
   python agent_example_2.py
   ```

### Code Quality

- Follow existing code style
- Add type hints to Python code
- Add JSDoc comments to TypeScript
- Update documentation when adding features

## Directory Structure

```
.
├── agent_filesystem/      # TypeScript tools (code execution mode)
│   ├── servers/
│   │   ├── teams/        # Teams operations
│   │   └── drive/        # Drive operations
│   └── example_*.ts      # Standalone examples
│
├── tools/                # Python tools (traditional mode)
│   ├── ms_teams_tools.py
│   ├── google_drive_tools.py
│   └── typescript_shell_tool.py
│
├── teams/                # Test data
│   └── meeting_summary.md
│
├── drive/                # Output directory (gitignored)
│
├── agent_example_1.py    # Traditional agent
├── agent_example_2.py    # Code execution agent
├── test_verification.py  # Test suite
└── medium.md            # Article
```

## Common Patterns

### Error Handling in Tools

**Python (Traditional):**
```python
@tool
def my_tool(param: str) -> str:
    try:
        # Implementation
        return "success"
    except Exception as e:
        return f"Error: {str(e)}"
```

**TypeScript (Code Execution):**
```typescript
export async function my_tool(param: string): Promise<any> {
  try {
    // Implementation
    return { status: 'success' };
  } catch (error) {
    throw new Error(`Failed: ${error}`);
  }
}
```

### Handling Large Data

The key benefit of code execution mode is handling large data:

```typescript
// This is good - data flows through code
const largeData = await download_large_file();
await upload_large_file(largeData);

// The LLM never sees the content, only writes the code
```

### Tool Discovery

For code execution mode, organize tools logically:

```
agent_filesystem/servers/
├── service_name/
│   ├── read_operations.ts
│   ├── write_operations.ts
│   └── admin_operations.ts
```

The agent explores this structure with `list_directory` and `read_file`.

## Questions?

Open an issue on GitHub with:
- Clear description of what you're trying to do
- Code examples
- Error messages if applicable

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
