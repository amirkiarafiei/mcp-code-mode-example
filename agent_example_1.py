"""
Agent Example 1: Traditional Tool Calling Approach

This example demonstrates the traditional approach where all tools are registered
with the agent upfront. All 20 tool definitions (10 Teams + 10 Drive) are loaded
into the agent's context from the start, even though we only need 2 tools for this task.
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

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

def main():
    """
    Run Agent Example 1 with traditional tool calling.
    
    This approach loads all 20 tools into the agent's context upfront.
    The model needs to have all tool schemas in its context to decide which ones to use.
    """
    
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", "gemini-1.5-pro"),
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0,
    )
    
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
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", AGENT_1_SYSTEM_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    # Create the agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    print("=" * 80)
    print("AGENT EXAMPLE 1: Traditional Tool Calling Approach")
    print("=" * 80)
    print(f"Total tools loaded into context: {len(tools)}")
    print("All tool schemas are in the agent's system prompt from the start.")
    print("=" * 80)
    print()
    
    # Execute the task
    result = agent_executor.invoke({"input": TASK_DESCRIPTION})
    
    print()
    print("=" * 80)
    print("RESULT:")
    print("=" * 80)
    print(result["output"])
    print()
    
    # Note: In a real scenario with actual large tool descriptions,
    # you would observe significant token usage in the initial prompt
    # due to all 20 tool definitions being present.

if __name__ == "__main__":
    main()
