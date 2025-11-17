"""
Microsoft Teams Tools - Native LangChain Tool Implementation
This module contains 10 dummy tools for Microsoft Teams operations.
Each tool has extensive descriptions and multiple parameters to simulate
real-world context consumption in traditional tool-calling approaches.
"""

from langchain.tools import tool
from typing import Optional, List, Dict
import os


@tool
def download_meeting_summary(
    meeting_id: Optional[str] = "latest",
    include_transcript: bool = True,
    include_attachments: bool = True,
    format: str = "markdown"
) -> str:
    """
    Download comprehensive meeting summaries from Microsoft Teams including full transcripts,
    action items, participant information, and all attachments. This tool connects to the
    Teams Graph API to retrieve meeting data and can export in multiple formats including
    markdown, JSON, PDF, or plain text. The tool handles pagination automatically for
    meetings with extensive content and supports filtering by date range, participants,
    or meeting type. Authentication is handled transparently using organizational SSO.
    
    Args:
        meeting_id: Unique identifier for the meeting. Use 'latest' for most recent meeting.
                   Format: GUID or 'latest'. Example: '19:meeting_abc123@thread.v2'
        include_transcript: Boolean flag to include full meeting transcript with timestamps
                          and speaker identification. May increase response size significantly.
        include_attachments: Boolean flag to include meeting attachments metadata and download links.
                           Actual files are not downloaded, only metadata is returned.
        format: Output format for the summary. Options: 'markdown', 'json', 'pdf', 'text'.
               Default is markdown for better readability.
    
    Returns:
        Complete meeting summary with all requested components formatted according to
        the specified format parameter. For large meetings, this can be extensive.
    """
    # Read the dummy meeting summary file
    summary_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "teams",
        "meeting_summary.md"
    )
    
    try:
        with open(summary_path, 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return "Error: Meeting summary file not found. Please check if teams/meeting_summary.md exists."


@tool
def list_team_meetings(
    team_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    include_cancelled: bool = False,
    organizer_email: Optional[str] = None,
    max_results: int = 100
) -> str:
    """
    Retrieve a comprehensive list of all meetings for a specified Microsoft Teams team,
    with advanced filtering capabilities including date ranges, organizer filtering,
    meeting status, and participant information. This tool queries the Teams Graph API
    with optimized batch requests to handle large result sets efficiently. Supports
    pagination for teams with extensive meeting histories and provides detailed metadata
    for each meeting including participant count, duration, recording availability, and
    associated channels. Results are sorted by start time in descending order by default.
    
    Args:
        team_id: The unique identifier for the Microsoft Teams team. This is the GUID
                that identifies the team in Azure AD. Format: GUID string.
        start_date: Optional ISO 8601 formatted date string to filter meetings starting
                   from this date. Example: '2024-01-01T00:00:00Z'
        end_date: Optional ISO 8601 formatted date string to filter meetings up to this date.
                 Must be after start_date if both are provided.
        include_cancelled: Boolean flag to include cancelled meetings in results. Default False.
                          Useful for audit trails and historical analysis.
        organizer_email: Optional email address to filter meetings by organizer. Supports
                        partial matching for domain-level filtering.
        max_results: Maximum number of meeting records to return. Range: 1-1000. Default 100.
                    Larger values may impact performance.
    
    Returns:
        JSON formatted string containing array of meeting objects with full metadata including
        meeting IDs, titles, organizers, participant lists, start/end times, and status.
    """
    return """[
        {
            "meeting_id": "19:meeting_abc123@thread.v2",
            "title": "Q4 Strategic Planning",
            "organizer": "sarah@company.com",
            "start_time": "2024-11-15T10:00:00Z",
            "end_time": "2024-11-15T12:30:00Z",
            "participants": 25,
            "has_recording": true,
            "status": "completed"
        }
    ]"""


@tool
def send_teams_message(
    channel_id: str,
    message: str,
    mention_users: Optional[List[str]] = None,
    priority: str = "normal",
    attachments: Optional[List[str]] = None,
    rich_text_format: bool = True
) -> str:
    """
    Send rich-formatted messages to Microsoft Teams channels with support for @mentions,
    file attachments, priority flags, and HTML formatting. This tool leverages the Teams
    messaging API to deliver messages with full formatting capabilities including bold,
    italic, lists, code blocks, and embedded images. Supports batching multiple attachments
    and automatically handles file upload orchestration. Messages can be marked as important
    or urgent to trigger special notifications. The tool validates channel permissions before
    sending and provides detailed error messages for authorization issues.
    
    Args:
        channel_id: The unique identifier for the Teams channel. Format: GUID string.
                   Must have posting permissions in the specified channel.
        message: The message content to send. Supports markdown and HTML formatting depending
                on rich_text_format flag. Maximum length: 28KB (Teams API limit).
        mention_users: Optional list of user IDs or email addresses to mention in the message.
                      Users will receive special notifications. Format: ['user@domain.com', ...]
        priority: Message priority level affecting notification behavior. Options: 'normal',
                 'important', 'urgent'. Urgent messages trigger immediate notifications.
        attachments: Optional list of file paths or URLs to attach to the message. Files are
                    uploaded asynchronously. Maximum 10 attachments per message.
        rich_text_format: Boolean flag to enable rich text formatting. When True, message
                         content is interpreted as HTML. When False, uses plain text.
    
    Returns:
        JSON string containing message ID, timestamp, and delivery status for the sent message.
    """
    return f"Message sent successfully to channel {channel_id}. Message ID: msg_xyz789"


@tool
def schedule_team_meeting(
    team_id: str,
    title: str,
    start_time: str,
    duration_minutes: int,
    attendees: List[str],
    description: Optional[str] = None,
    location: Optional[str] = None,
    is_recurring: bool = False,
    recurrence_pattern: Optional[str] = None
) -> str:
    """
    Schedule new meetings for Microsoft Teams with comprehensive configuration options
    including recurring meeting patterns, optional attendance, location details, and
    automatic calendar integration. This tool creates meeting entries in all attendees'
    Outlook calendars, sends email invitations, and configures the Teams virtual meeting
    space. Supports complex recurrence patterns (daily, weekly, monthly, custom) with
    end conditions. Automatically handles timezone conversions for international attendees
    and resolves scheduling conflicts by checking attendee availability. Integrates with
    Outlook's scheduling assistant to suggest optimal meeting times when conflicts exist.
    
    Args:
        team_id: The unique identifier for the Microsoft Teams team. Format: GUID string.
        title: Meeting title/subject. Maximum length: 255 characters. Should be descriptive.
        start_time: Meeting start time in ISO 8601 format with timezone. Example:
                   '2024-11-20T14:00:00-08:00'. System handles timezone conversions.
        duration_minutes: Meeting duration in minutes. Range: 15-1440 (24 hours max per meeting).
        attendees: List of attendee email addresses. Required attendees. Format: ['user@domain.com', ...]
        description: Optional meeting description or agenda. Supports rich text formatting.
                    Maximum length: 8KB. Appears in meeting invitation.
        location: Optional physical location or additional virtual meeting details. Format: free text
                 or structured address. Example: 'Conference Room A, Building 5'
        is_recurring: Boolean flag to create a recurring meeting series. Requires recurrence_pattern.
        recurrence_pattern: JSON string defining recurrence rules. Required if is_recurring is True.
                          Example: '{"frequency": "weekly", "days": ["Monday", "Wednesday"], "end_date": "2024-12-31"}'
    
    Returns:
        JSON string containing meeting ID, join URL, and calendar entry IDs for all attendees.
    """
    return f"""{{
        "meeting_id": "19:meeting_new456@thread.v2",
        "title": "{title}",
        "join_url": "https://teams.microsoft.com/l/meetup-join/...",
        "status": "scheduled"
    }}"""


@tool
def get_team_members(
    team_id: str,
    include_inactive: bool = False,
    include_guests: bool = True,
    role_filter: Optional[str] = None
) -> str:
    """
    Retrieve comprehensive member information for a Microsoft Teams team including roles,
    status, presence information, contact details, and activity metrics. This tool queries
    Azure AD and Teams Graph API to compile complete member profiles with real-time presence
    (available, busy, away, offline), recent activity timestamps, and permission levels.
    Supports filtering by role (owner, member, guest) and activity status. Results include
    direct contact information, organizational hierarchy, and team-specific permissions.
    Particularly useful for administrative tasks, compliance audits, and team analytics.
    
    Args:
        team_id: The unique identifier for the Microsoft Teams team. Format: GUID string.
        include_inactive: Boolean flag to include members who haven't been active recently.
                         Default False. Active threshold is 30 days.
        include_guests: Boolean flag to include guest users from external organizations.
                       Default True. Guests have limited permissions.
        role_filter: Optional role filter. Options: 'owner', 'member', 'guest', None for all.
                    Filters results to only users with specified role.
    
    Returns:
        JSON formatted string containing array of member objects with detailed information
        including user IDs, names, emails, roles, presence status, and last activity time.
    """
    return """[
        {
            "user_id": "user123",
            "name": "Sarah Johnson",
            "email": "sarah@company.com",
            "role": "owner",
            "presence": "available",
            "last_active": "2024-11-17T12:00:00Z"
        }
    ]"""


@tool
def search_teams_content(
    query: str,
    content_types: Optional[List[str]] = None,
    date_range: Optional[Dict[str, str]] = None,
    teams_filter: Optional[List[str]] = None,
    max_results: int = 50
) -> str:
    """
    Perform advanced full-text search across all Microsoft Teams content including messages,
    files, meeting notes, and channel information with sophisticated filtering and ranking.
    This tool utilizes Microsoft's search index to provide fast, relevant results with
    snippet highlighting and relevance scoring. Supports boolean operators, phrase matching,
    wildcard searches, and field-specific queries. Results can be filtered by content type
    (messages, files, meetings), date ranges, specific teams or channels, and author.
    Search index updates near real-time (typically within 5 minutes of content creation).
    Respects all Teams permissions ensuring users only see content they have access to.
    
    Args:
        query: Search query string. Supports boolean operators (AND, OR, NOT), phrase matching
              with quotes, and wildcards. Example: 'meeting AND (summary OR notes) -cancelled'
        content_types: Optional list of content types to search. Options: ['messages', 'files',
                      'meetings', 'notes']. Default searches all types.
        date_range: Optional dictionary with 'start' and 'end' ISO 8601 date strings to limit
                   search to specific time period. Example: {'start': '2024-01-01', 'end': '2024-12-31'}
        teams_filter: Optional list of team IDs to restrict search scope. Useful for focused searches
                     within specific teams. Format: ['team_id1', 'team_id2', ...]
        max_results: Maximum number of search results to return. Range: 1-200. Default 50.
                    Higher values may impact performance.
    
    Returns:
        JSON formatted string containing array of search result objects with content snippets,
        relevance scores, metadata, and direct links to original content in Teams.
    """
    return """[
        {
            "content_type": "meeting",
            "title": "Q4 Strategic Planning",
            "snippet": "...AI/ML integration roadmap, expanding enterprise...",
            "score": 0.95,
            "url": "https://teams.microsoft.com/...",
            "date": "2024-11-15T10:00:00Z"
        }
    ]"""


@tool
def update_meeting_recording_settings(
    meeting_id: str,
    enable_recording: bool = True,
    auto_transcription: bool = True,
    allow_participant_recording: bool = False,
    recording_retention_days: int = 120
) -> str:
    """
    Configure recording and transcription settings for Microsoft Teams meetings with granular
    control over recording permissions, automatic transcription, retention policies, and
    participant capabilities. This tool manages meeting recording lifecycle including automatic
    recording triggers, cloud storage allocation, transcription language settings, and
    retention compliance. Supports organizational policies and compliance requirements for
    legal hold, GDPR, and industry-specific regulations. Recording settings can be configured
    for individual meetings or applied as templates for recurring meeting series. Integrates
    with Microsoft Stream for video hosting and OneDrive for recording storage management.
    
    Args:
        meeting_id: Unique identifier for the meeting. Format: GUID or meeting URL.
        enable_recording: Boolean flag to enable automatic meeting recording. Default True.
                         Recording starts when meeting starts and stops when meeting ends.
        auto_transcription: Boolean flag to enable automatic transcription of recording with
                           speaker identification. Supports 30+ languages. Default True.
        allow_participant_recording: Boolean flag to allow non-organizer participants to
                                    start/stop recording. Default False for security.
        recording_retention_days: Number of days to retain recording before automatic deletion.
                                 Range: 30-3650 days. Default 120. Affects storage costs.
    
    Returns:
        JSON string confirming updated settings with recording policy details and storage allocation.
    """
    return f"""{{
        "meeting_id": "{meeting_id}",
        "recording_enabled": {enable_recording},
        "transcription_enabled": {auto_transcription},
        "retention_policy": "{recording_retention_days} days",
        "status": "updated"
    }}"""


@tool
def export_team_analytics(
    team_id: str,
    analytics_period: str = "30days",
    metrics: Optional[List[str]] = None,
    include_individual_stats: bool = False,
    export_format: str = "json"
) -> str:
    """
    Export comprehensive analytics and usage statistics for Microsoft Teams team including
    message volume, meeting frequency, active users, channel engagement, file sharing patterns,
    and collaboration metrics. This tool generates detailed reports using Teams analytics API
    with historical data going back up to 365 days. Metrics include daily/weekly/monthly active
    users, peak usage times, message sentiment analysis, response time statistics, and
    collaboration network graphs. Particularly valuable for team leaders monitoring engagement,
    HR tracking productivity trends, and IT departments planning resource allocation. Supports
    multiple export formats and can generate visual dashboards for executive presentations.
    
    Args:
        team_id: The unique identifier for the Microsoft Teams team. Format: GUID string.
        analytics_period: Time period for analytics. Options: '7days', '30days', '90days',
                         '365days', or custom 'YYYY-MM-DD:YYYY-MM-DD'. Default '30days'.
        metrics: Optional list of specific metrics to include. Options: ['messages', 'meetings',
                'active_users', 'files', 'engagement_score']. Default includes all metrics.
        include_individual_stats: Boolean flag to include per-user statistics in export.
                                 Default False for privacy. Requires admin permissions.
        export_format: Output format for analytics data. Options: 'json', 'csv', 'pdf', 'excel'.
                      Default 'json'. PDF includes visualizations and charts.
    
    Returns:
        Analytics data in requested format containing aggregated statistics, trend analysis,
        and insights about team collaboration patterns and productivity metrics.
    """
    return """[
        {
            "period": "30days",
            "total_messages": 2847,
            "total_meetings": 42,
            "active_users": 25,
            "avg_response_time_minutes": 23,
            "engagement_score": 8.4
        }
    ]"""


@tool
def manage_team_channels(
    team_id: str,
    action: str,
    channel_name: Optional[str] = None,
    channel_description: Optional[str] = None,
    channel_type: str = "standard",
    notification_settings: Optional[Dict[str, bool]] = None
) -> str:
    """
    Comprehensive channel management tool for Microsoft Teams supporting create, update, delete,
    and archive operations with fine-grained permission control and notification settings.
    This tool manages channel lifecycle including creation of standard or private channels,
    member assignments, notification preferences, and integration configurations. Supports
    bulk operations for channel templates and organizational standards. Private channels
    enable sensitive discussions with restricted membership while maintaining team structure.
    Channel settings include default file storage locations, tab configurations, connector
    integrations, and moderation policies. Essential for team administrators managing
    organizational collaboration spaces and ensuring proper channel governance.
    
    Args:
        team_id: The unique identifier for the Microsoft Teams team. Format: GUID string.
        action: Channel operation to perform. Options: 'create', 'update', 'delete', 'archive',
               'list'. Each action requires different additional parameters.
        channel_name: Channel display name. Required for create/update actions. Maximum length:
                     50 characters. Must be unique within team.
        channel_description: Optional detailed description of channel purpose and guidelines.
                           Maximum length: 1024 characters. Supports markdown formatting.
        channel_type: Type of channel to create. Options: 'standard', 'private'. Default 'standard'.
                     Private channels have restricted membership and separate file storage.
        notification_settings: Optional dictionary of notification preferences. Example:
                             {'banner': True, 'email': False, 'feed': True}
    
    Returns:
        JSON string containing channel operation results including channel ID, name, type,
        and configuration details for the affected channel.
    """
    return f"""{{
        "team_id": "{team_id}",
        "action": "{action}",
        "channel_name": "{channel_name}",
        "channel_id": "19:channel_abc@thread.tacv2",
        "status": "success"
    }}"""


@tool
def sync_team_calendar(
    team_id: str,
    calendar_source: str,
    sync_direction: str = "bidirectional",
    sync_interval_minutes: int = 15,
    conflict_resolution: str = "teams_priority"
) -> str:
    """
    Synchronize Microsoft Teams team calendar with external calendar systems including Google
    Calendar, Outlook, iCal, and other CalDAV-compatible services with real-time or scheduled
    sync intervals. This tool establishes and manages calendar sync connections ensuring
    meeting consistency across platforms and preventing double-booking scenarios. Supports
    multiple sync strategies including one-way import, one-way export, and bidirectional
    synchronization with configurable conflict resolution policies. Handles timezone conversion,
    recurring event propagation, attendee mapping, and meeting status updates automatically.
    Essential for organizations using multiple calendar systems or integrating with external
    partners using different platforms.
    
    Args:
        team_id: The unique identifier for the Microsoft Teams team. Format: GUID string.
        calendar_source: External calendar system identifier or URL. Supports: 'google_calendar',
                        'outlook_external', 'ical_url', or CalDAV server URLs.
        sync_direction: Synchronization direction. Options: 'import' (external to Teams),
                       'export' (Teams to external), 'bidirectional' (both ways). Default 'bidirectional'.
        sync_interval_minutes: How frequently to synchronize calendars in minutes. Range: 5-1440.
                              Default 15. Lower values increase API usage and costs.
        conflict_resolution: Strategy for handling scheduling conflicts. Options: 'teams_priority'
                           (Teams changes win), 'external_priority', 'latest_change', 'manual'.
    
    Returns:
        JSON string containing sync configuration details, connection status, and initial sync
        results including number of events synchronized and any conflicts detected.
    """
    return f"""{{
        "team_id": "{team_id}",
        "calendar_source": "{calendar_source}",
        "sync_status": "active",
        "last_sync": "2024-11-17T12:25:00Z",
        "events_synced": 42,
        "conflicts": 0
    }}"""
