from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import os

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file('credentials.json', SCOPES)
            flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'  # penting!

            auth_url, _ = flow.authorization_url(prompt='consent')
            print("🔐 Silakan buka link ini di browser dan izinkan akses:")
            print(auth_url)
            code = input("🔑 Masukkan kode verifikasi dari Google: ")

            flow.fetch_token(code=code)
            creds = flow.credentials

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds
