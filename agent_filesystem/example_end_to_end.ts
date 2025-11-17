/**
 * End-to-end example: Download from Teams and Upload to Drive
 * This demonstrates how operations can be chained in code without
 * the large intermediate data passing through the LLM.
 */

import { download_meeting_summary } from './servers/teams/download_meeting_summary';
import { upload_to_drive } from './servers/drive/upload_to_drive';

async function main() {
  console.log('Starting end-to-end example...\n');
  
  // Step 1: Download meeting summary from Teams
  console.log('Step 1: Downloading meeting summary from Teams...');
  const summary = await download_meeting_summary();
  console.log(`✓ Downloaded ${summary.length} characters\n`);
  
  // Step 2: Upload to Google Drive
  console.log('Step 2: Uploading to Google Drive...');
  const result = await upload_to_drive(summary, 'meeting_summary.md', 'root');
  console.log(`✓ Upload complete!`);
  console.log(`  File ID: ${result.file_id}`);
  console.log(`  Link: ${result.web_view_link}\n`);
  
  console.log('End-to-end example completed successfully!');
  console.log('\nKey benefit: The large meeting summary (8KB+) flowed directly');
  console.log('from download to upload via code, never passing through the LLM context.');
}

main().catch(error => {
  console.error('Error:', error);
  process.exit(1);
});
