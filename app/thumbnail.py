import db
import requests
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = "app\static\credentials.json "  # Caminho como string
DRIVE_FOLDER_ID = '1SOoxaP0T8cUBbLBIx2VqV5KTlQ3RZbXY'  # Pasta como string

print("Caminho do arquivo de credenciais:", SERVICE_ACCOUNT_FILE)

# Carrega as credenciais
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

def get_video_ids():
    connection = db.conn()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT video_id FROM comments_score")
        results = cursor.fetchall()
        return [row[0] for row in results]
    else:
        print("Erro ao db ao banco de dados.")
        return []

def download_thumbnail(video_id):
    url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        file_path = f"/tmp/{video_id}.jpg"
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return file_path
    else:
        print(f"Erro ao baixar a miniatura para o vídeo {video_id}")
        return None

def upload_to_drive(file_path, video_id):
    file_metadata = {
        'name': f'{video_id}.jpg',
        'parents': [DRIVE_FOLDER_ID]
    }
    media = MediaFileUpload(file_path, mimetype='image/jpeg')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Thumbnail {video_id}.jpg foi enviada para o Google Drive com o ID {file.get('id')}")

def main():
    video_ids = get_video_ids()
    for video_id in video_ids:
        file_path = download_thumbnail(video_id)
        if file_path:
            upload_to_drive(file_path, video_id)
            os.remove(file_path)  # Remove o arquivo temporário após o upload

if __name__ == "__main__":
    main()
