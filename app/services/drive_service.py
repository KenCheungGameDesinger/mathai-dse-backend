from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def upload_file(file, folder_path):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    # 創建或查找目錄
    folder_id = get_or_create_folder(drive, folder_path)
    file_metadata = {'title': file.filename, 'parents': [{'id': folder_id}]}
    gfile = drive.CreateFile(file_metadata)
    gfile.SetContentFile(file.filename)
    gfile.Upload()
    gfile.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
    return gfile['alternateLink']

def get_or_create_folder(drive, folder_path):
    folder_names = folder_path.split('/')
    parent_id = 'root'

    for folder_name in folder_names:
        folder_list = drive.ListFile({
            'q': f"'{parent_id}' in parents and title = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        }).GetList()

        if folder_list:
            folder_id = folder_list[0]['id']
        else:
            folder_metadata = {'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder', 'parents': [{'id': parent_id}]}
            folder = drive.CreateFile(folder_metadata)
            folder.Upload()
            folder_id = folder['id']

        parent_id = folder_id
    return parent_id
