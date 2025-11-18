"""
Agent Example 2: Code Execution Approach

This example demonstrates the code execution approach where tools are discovered
from the filesystem on-demand. Only 3 generic tools (list_directory, read_file, 
execute_typescript) are loaded into the agent's context. The agent discovers and 
uses the specific tools it needs by exploring the filesystem.
"""

import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
# Import only the filesystem and execution tools (3 tools instead of 20!)
from tools.typescript_shell_tool import (
    execute_typescript,
    read_file,
    list_directory,
)

from prompt import AGENT_2_SYSTEM_PROMPT, TASK_DESCRIPTION

# Load environment variables
load_dotenv()

def main():
    """
    Run Agent Example 2 with code execution approach.
    
    This approach only loads 3 generic tools into the agent's context.
    The agent discovers specific tools by exploring the filesystem and
    executes TypeScript code to chain operations efficiently.
    """
    
    # Only 3 generic tools are registered here
    tools = [
        list_directory,
        read_file,
        execute_typescript,
    ]

    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model=os.getenv('GEMINI_MODEL'),
        temperature=0.0,
        timeout=None,
    )
    
    # Create the agent using the new create_agent API of Langchain v1.0
    # This automatically uses LangGraph under the hood
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=AGENT_2_SYSTEM_PROMPT,
        debug=True,
    )
    
    print("=" * 80)
    print("AGENT EXAMPLE 2: Code Execution Approach")
    print("=" * 80)
    print(f"Total generic tools loaded into context: {len(tools)}")
    print("Specific tools (20+) are discovered from filesystem on-demand.")
    print("Agent will explore agent_filesystem/servers/ to find what it needs.")
    print("=" * 80)
    print()
    
    # Execute the task 
    result = agent.invoke({
        "messages": [{"role": "user", "content": TASK_DESCRIPTION}]
    })
    
    print()
    print("=" * 80)
    print("RESULT:")
    print("=" * 80)
    
    # Extract the final message content
    final_message = result["messages"][-1]
    print(final_message.content if hasattr(final_message, 'content') else str(final_message))
    print()
    
    # Benefits demonstrated:
    # 1. Only 3 tool definitions in initial context vs 20
    # 2. Large meeting summary data flows through TypeScript code, not LLM context
    # 3. Agent loads only the tool definitions it actually needs
    # 4. More efficient use of context window

if __name__ == "__main__":
    main()
