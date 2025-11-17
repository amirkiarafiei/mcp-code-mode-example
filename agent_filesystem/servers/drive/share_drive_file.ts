/** Share Drive file */
export async function share_drive_file(
  fileId: string,
  userEmails: string[],
  permissionRole: string = 'reader'
): Promise<any> {
  return { file_id: fileId, shared_with: userEmails, status: 'success' };
}
