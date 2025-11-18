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

from langchain_core.messages import AIMessage, ToolMessage
from tokenizer import count_tokens, estimate_tools_tokens

# Load environment variables
load_dotenv()

def print_agent_overview(stage: str, tools_count: int, input_tokens: int, tool_calls: int, output_tokens: int, total_tokens: int):
    print("=" * 80) 
    print(f"AGENT CONTEXT OVERVIEW {stage}:")
    print("=" * 80) 
    print(f"Available Tools: {tools_count}")
    print(f"Input Tokens: {input_tokens}")
    print(f"Tool Calls: {tool_calls}")
    print(f"Generated Tokens: {output_tokens}" if stage == "before" else f"Output Tokens: {output_tokens}")
    print(f"Total Tokens in Context Window: {total_tokens}")
    print("=" * 80)

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
    
    # Calculate Before Stats
    system_tokens = count_tokens(AGENT_2_SYSTEM_PROMPT)
    user_tokens = count_tokens(TASK_DESCRIPTION)
    tools_tokens = estimate_tools_tokens(tools)
    initial_input_tokens = system_tokens + user_tokens + tools_tokens
    
    print("=" * 80)
    print("AGENT EXAMPLE 2: Code Execution Approach")
    print("=" * 80)
    print(f"Total generic tools loaded into context: {len(tools)}")
    print("Specific tools (20+) are discovered from filesystem on-demand.")
    print("Agent will explore agent_filesystem/servers/ to find what it needs.")
    
    print_agent_overview(
        stage="before",
        tools_count=len(tools),
        input_tokens=initial_input_tokens,
        tool_calls=0,
        output_tokens=0,
        total_tokens=initial_input_tokens
    )
    
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
    
    # Calculate After Stats
    messages = result["messages"]
    
    # Count tool calls and outputs
    tool_calls_count = 0
    generated_tokens = 0
    tool_outputs_tokens = 0
    
    for msg in messages:
        if isinstance(msg, AIMessage):
            # Content can be a string or list of blocks (e.g. text + tool_use)
            content = msg.content
            if isinstance(content, list):
                # Extract text from content blocks if it's a list
                text_content = ""
                for block in content:
                    if isinstance(block, dict) and "text" in block:
                        text_content += block["text"]
                    elif hasattr(block, "text"):
                        text_content += block.text
                generated_tokens += count_tokens(text_content)
            else:
                generated_tokens += count_tokens(str(content))
                
            tool_calls_count += len(msg.tool_calls)
        elif isinstance(msg, ToolMessage):
            tool_outputs_tokens += count_tokens(str(msg.content))
            
    final_total_tokens = initial_input_tokens + generated_tokens + tool_outputs_tokens
    
    print_agent_overview(
        stage="after",
        tools_count=len(tools),
        input_tokens=initial_input_tokens, # Base input
        tool_calls=tool_calls_count,
        output_tokens=generated_tokens,
        total_tokens=final_total_tokens
    )
    
    # Benefits demonstrated:
    # 1. Only 3 tool definitions in initial context vs 20
    # 2. Large meeting summary data flows through TypeScript code, not LLM context
    # 3. Agent loads only the tool definitions it actually needs
    # 4. More efficient use of context window

if __name__ == "__main__":
    main()
