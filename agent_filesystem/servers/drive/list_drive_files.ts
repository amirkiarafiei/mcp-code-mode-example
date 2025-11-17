/** List files in Drive */
export async function list_drive_files(folderId: string = 'root', options?: any): Promise<any[]> {
  return [{ file_id: '1xyz', name: 'document.txt', size_bytes: 1024 }];
}
