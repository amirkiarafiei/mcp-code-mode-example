"""
Agent Example 1: Traditional Tool Calling Approach

This example demonstrates the traditional approach where all tools are registered
with the agent upfront. All 20 tool definitions (10 Teams + 10 Drive) are loaded
into the agent's context from the start, even though we only need 2 tools for this task.
"""

import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

# Import all the tools (this loads all 20 tool definitions into context)
from tools.ms_teams_tools import (
    download_meeting_summary,
    list_team_meetings,
    send_teams_message,
    schedule_team_meeting,
    get_team_members,
    search_teams_content,
    update_meeting_recording_settings,
    export_team_analytics,
    manage_team_channels,
    sync_team_calendar,
)

from tools.google_drive_tools import (
    upload_to_drive,
    list_drive_files,
    create_drive_folder,
    share_drive_file,
    download_from_drive,
    search_drive_content,
    manage_drive_permissions,
    sync_drive_folder,
    export_drive_metadata,
    manage_drive_versions,
)

from prompt import AGENT_1_SYSTEM_PROMPT, TASK_DESCRIPTION

from langchain_core.messages import AIMessage, ToolMessage
from tokenizer import count_tokens, estimate_tools_tokens

# Load environment variables
load_dotenv()

# # Enable debug mode
# from langchain_classic.globals import set_debug
# set_debug(True)

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
    Run Agent Example 1 with traditional tool calling.
    
    This approach loads all 20 tools into the agent's context upfront.
    The model needs to have all tool schemas in its context to decide which ones to use.
    """
    
    # All 20 tools are registered here - they all go into the system prompt
    tools = [
        # Teams tools (10)
        download_meeting_summary,
        list_team_meetings,
        send_teams_message,
        schedule_team_meeting,
        get_team_members,
        search_teams_content,
        update_meeting_recording_settings,
        export_team_analytics,
        manage_team_channels,
        sync_team_calendar,
        # Drive tools (10)
        upload_to_drive,
        list_drive_files,
        create_drive_folder,
        share_drive_file,
        download_from_drive,
        search_drive_content,
        manage_drive_permissions,
        sync_drive_folder,
        export_drive_metadata,
        manage_drive_versions,
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
        system_prompt=AGENT_1_SYSTEM_PROMPT,
        debug=True,
    )
    
    # Calculate Before Stats
    system_tokens = count_tokens(AGENT_1_SYSTEM_PROMPT)
    user_tokens = count_tokens(TASK_DESCRIPTION)
    tools_tokens = estimate_tools_tokens(tools)
    initial_input_tokens = system_tokens + user_tokens + tools_tokens
    
    print("=" * 80)
    print("AGENT EXAMPLE 1: Traditional Tool Calling Approach")
    print("=" * 80)
    print(f"Total tools loaded into context: {len(tools)}")
    print("All tool schemas are in the agent's system prompt from the start.")
    
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
    
    # Note: In a real scenario with actual large tool descriptions,
    # you would observe significant token usage in the initial prompt
    # due to all 20 tool definitions being present.

if __name__ == "__main__":
    main()
