/**
 * Download meeting summary from Microsoft Teams
 * This function retrieves the latest meeting summary file
 */

import * as fs from 'fs';
import * as path from 'path';

export async function download_meeting_summary(): Promise<string> {
  const summaryPath = path.join(__dirname, '../../../teams/meeting_summary.md');
  
  try {
    const content = fs.readFileSync(summaryPath, 'utf-8');
    return content;
  } catch (error) {
    throw new Error(`Failed to download meeting summary: ${error}`);
  }
}

// Allow direct execution
if (require.main === module) {
  download_meeting_summary()
    .then(summary => {
      console.log('Meeting summary downloaded successfully');
      console.log(`Content length: ${summary.length} characters`);
    })
    .catch(error => {
      console.error(error.message);
      process.exit(1);
    });
}
