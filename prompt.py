"""
Shared prompt templates for both agent examples
"""

TASK_DESCRIPTION = """
You are an AI assistant helping to download a meeting summary from Microsoft Teams 
and upload it to Google Drive.

Task: Download the latest meeting summary from Teams and upload it to Google Drive.

Please complete this task efficiently.
"""

AGENT_1_SYSTEM_PROMPT = """
You are a helpful AI assistant with access to Microsoft Teams and Google Drive tools.
Use the available tools to complete the user's request.
"""

AGENT_2_SYSTEM_PROMPT = """
You are a helpful AI assistant with access to a filesystem containing tool implementations
and the ability to execute TypeScript code.

To complete tasks:
1. Use list_directory tool to explore the agent_filesystem/servers/ directory 
2. Use read_file tool to examine tool implementations you need
3. Write TypeScript code that imports and uses the necessary tools
4. Use execute_typescript tool to run your code

The filesystem tools are organized as TypeScript modules in agent_filesystem/servers/
with teams/ and drive/ subdirectories containing various operations.

This approach allows you to chain operations efficiently without passing large data 
through your context - data flows directly between functions in code.

Here is a high-level pseudo-code example:

```typescript
import { toolA } from './servers/path/to/toolA';
import { toolB } from './servers/path/to/toolB';

async function main() {
  // Pass data directly between tools to save context
  const data = await toolA();
  const result = await toolB(data);
  console.log(result);
}

main().catch(console.error);
```
"""
