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

# Load environment variables
load_dotenv()

# # Enable debug mode
# from langchain_classic.globals import set_debug
# set_debug(True)

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
    
    print("=" * 80)
    print("AGENT EXAMPLE 1: Traditional Tool Calling Approach")
    print("=" * 80)
    print(f"Total tools loaded into context: {len(tools)}")
    print("All tool schemas are in the agent's system prompt from the start.")
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
    
    # Note: In a real scenario with actual large tool descriptions,
    # you would observe significant token usage in the initial prompt
    # due to all 20 tool definitions being present.

if __name__ == "__main__":
    main()
