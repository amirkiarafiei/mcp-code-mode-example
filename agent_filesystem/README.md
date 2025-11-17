# Agent Filesystem - Tool Implementations

This directory contains tool implementations organized as TypeScript modules that can be discovered and executed by AI agents using the code execution approach.

## Structure

```
agent_filesystem/
└── servers/
    ├── teams/         # Microsoft Teams tools (10 functions)
    └── drive/         # Google Drive tools (10 functions)
```

## Microsoft Teams Tools (`servers/teams/`)

1. **download_meeting_summary.ts** - Download meeting summaries
2. **list_team_meetings.ts** - List all team meetings
3. **send_teams_message.ts** - Send messages to channels
4. **schedule_team_meeting.ts** - Schedule new meetings
5. **get_team_members.ts** - Get team member information
6. **search_teams_content.ts** - Search across Teams content
7. **update_meeting_recording_settings.ts** - Configure recording settings
8. **export_team_analytics.ts** - Export team analytics data
9. **manage_team_channels.ts** - Manage team channels
10. **sync_team_calendar.ts** - Sync with external calendars

## Google Drive Tools (`servers/drive/`)

1. **upload_to_drive.ts** - Upload files to Google Drive
2. **list_drive_files.ts** - List files in Drive
3. **create_drive_folder.ts** - Create new folders
4. **share_drive_file.ts** - Share files with users
5. **download_from_drive.ts** - Download files from Drive
6. **search_drive_content.ts** - Search Drive content
7. **manage_drive_permissions.ts** - Manage file permissions
8. **sync_drive_folder.ts** - Sync folders with local filesystem
9. **export_drive_metadata.ts** - Export Drive metadata
10. **manage_drive_versions.ts** - Manage file versions

## Usage Pattern

Agents discover tools by:
1. Listing the directory structure
2. Reading specific tool implementations
3. Writing TypeScript code that imports and uses these tools
4. Executing the code with the TypeScript shell tool

This approach keeps tool definitions out of the initial agent context, loading only what's needed on-demand.
