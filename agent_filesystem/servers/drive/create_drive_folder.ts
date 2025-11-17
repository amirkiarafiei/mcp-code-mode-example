/** Create folder in Drive */
export async function create_drive_folder(
  folderName: string,
  parentFolderId: string = 'root'
): Promise<any> {
  return { folder_id: '1folder_abc', folder_name: folderName, status: 'created' };
}
